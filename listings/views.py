import logging
from django.db.models import Avg
from django.core.cache import cache
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from listings.models import Listing
from listings.serializers import ListingSerializer, ToggleActiveResponseSerializer
from listings.permissions import IsAdminOrLandlord
from analytics.services import record_listing_view
from analytics.models import SearchHistory
from listings.config import ListingFilter

logger = logging.getLogger(__name__)


class ListingViewSet(viewsets.ModelViewSet):
    """
    Rental Listing Management:

    Roles and permissions:
    - TENANT:
        - Can only view active listings.
        - Listing views are recorded for analytics.
    - LANDLORD:
        - Can create, update, delete their own listings.
        - Can toggle the active status of their listings.
    - ADMIN:
        - Full access to all listings.

    Query filtering and ordering:
    - Supports search by title, description, city, country.
    - Supports ordering by price_per_day, created_at, average_rating.
    - Supports filters: property_type, country, city, is_active, min/max price, min/max rooms.
    """

    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsAdminOrLandlord]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title", "description", "city", "country"]
    ordering_fields = ["price_per_day", "created_at", "average_rating_value"]
    ordering = ["-created_at"]
    filterset_class = ListingFilter

    def get_queryset(self):
        """
        Returns listings based on the user's role and optional filters.
        Adds annotation 'average_rating_value' for sorting.
        Uses cache for frequently accessed data.
        """
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Listing.objects.none()
        
        user = self.request.user
        
        # Build cache key based on user role and filters
        cache_key = f"listings_queryset_{user.id if user.is_authenticated else 'anon'}"
        filter_params = dict(self.request.query_params)
        if filter_params:
            # Convert all values to strings and sort for consistent hashing
            sorted_params = sorted(
                (k, tuple(v) if isinstance(v, list) else v)
                for k, v in filter_params.items()
            )
            cache_key += f"_{hash(tuple(sorted_params))}"
        
        # Try to get from cache
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset
        
        queryset = Listing.objects.filter(is_deleted=False)\
            .select_related("landlord")\
            .prefetch_related("reviews")\
            .annotate(average_rating_value=Avg("reviews__rating"))

        # Price filtering
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        try:
            if min_price:
                queryset = queryset.filter(price_per_day__gte=float(min_price))
            if max_price:
                queryset = queryset.filter(price_per_day__lte=float(max_price))
        except ValueError as e:
            logger.warning(f"Invalid price filter: min_price={min_price}, max_price={max_price}, error={e}")

        # Role-based filtering
        if user.is_staff or user.is_superuser:
            # Admin/Staff: see all listings
            result_queryset = queryset
        elif user.is_landlord():
            # Landlord: see all own listings (active or inactive)
            result_queryset = queryset.filter(landlord=user)
        else:
            # Tenant: see only active listings
            result_queryset = queryset.filter(is_active=True)
        
        # Cache the queryset for 5 minutes (only for GET requests without complex filters)
        if self.request.method == 'GET' and not filter_params.get('search'):
            cache.set(cache_key, result_queryset, 300)  # 5 minutes
        
        return result_queryset
        
        # Cache the queryset for 5 minutes (only for GET requests without complex filters)
        if self.request.method == 'GET' and not filter_params.get('search'):
            cache.set(cache_key, result_queryset, 300)  # 5 minutes
        
        return result_queryset

    def get_ordering(self):
        ordering = self.request.query_params.get("ordering")
        if ordering:
            return [ordering]
        return super().get_ordering()

    @swagger_auto_schema(
        operation_summary="List Listings",
        operation_description="Returns listings based on user role and filters.",
        manual_parameters=[
            openapi.Parameter(
                "search", openapi.IN_QUERY,
                description="Search by title, description, city, country",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "ordering", openapi.IN_QUERY,
                description="Order by price_per_day, created_at, average_rating",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "min_price", openapi.IN_QUERY,
                description="Minimum price",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "max_price", openapi.IN_QUERY,
                description="Maximum price",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "min_rooms", openapi.IN_QUERY,
                description="Minimum number of rooms",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "max_rooms", openapi.IN_QUERY,
                description="Maximum number of rooms",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "city", openapi.IN_QUERY, description="City", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "country", openapi.IN_QUERY, description="Country", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "property_type", openapi.IN_QUERY,
                description="Property type", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(description="OK", schema=ListingSerializer(many=True))
        },
    )
    def list(self, request, *args, **kwargs):
        # --- saving the search keyword ---
        keyword = request.query_params.get("search")
        user = request.user

        if keyword and user.is_authenticated:
            normalized = keyword.strip().lower()
            last = (
                SearchHistory.objects.filter(user=user)
                .order_by("-searched_at")
                .first()
            )
            if not last or last.keyword != normalized:
                SearchHistory.objects.create(user=user, keyword=normalized)

        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Listing",
        operation_description="LANDLORD or ADMIN creates a new listing.",
        request_body=ListingSerializer,
        responses={201: openapi.Response(description="Created", schema=ListingSerializer)},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Set landlord to current user when creating a new listing.
        """
        serializer.save(landlord=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve Listing",
        operation_description="TENANT sees only active listings. View is recorded.",
        responses={200: openapi.Response(description="OK", schema=ListingSerializer), 403: "Forbidden"},
    )
    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        user = request.user
        
        # Try to get from cache
        cache_key = f"listing_{listing.id}"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        
        if not user.is_staff and not user.is_landlord():
            record_listing_view(user, listing)
        
        response = super().retrieve(request, *args, **kwargs)
        
        # Cache the response for 5 minutes
        if response.status_code == 200:
            cache.set(cache_key, response.data, 300)
        
        return response

    @swagger_auto_schema(
        operation_summary="Update Listing",
        operation_description="Only the owner or ADMIN can update the listing.",
        request_body=ListingSerializer,
        responses={200: openapi.Response(description="Updated", schema=ListingSerializer), 403: "Forbidden"},
    )
    def update(self, request, *args, **kwargs):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Listing",
        operation_description="Only the owner or ADMIN can partially update the listing.",
        request_body=ListingSerializer,
        responses={200: openapi.Response(description="Updated", schema=ListingSerializer), 403: "Forbidden"},
    )
    def partial_update(self, request, *args, **kwargs):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Listing",
        operation_description="Marks the listing as deleted. Only the owner or ADMIN.",
        responses={204: openapi.Response(description="Deleted"), 403: "Forbidden"},
    )
    def destroy(self, request, *args, **kwargs):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        listing.is_deleted = True
        listing.save()
        return Response({"detail": "Listing marked as deleted."}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Toggle Listing Active Status",
        operation_description="Toggles the listing's active status. Only the owner or ADMIN.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
        responses={200: openapi.Response(description="OK", schema=ToggleActiveResponseSerializer), 403: "Forbidden"},
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAdminOrLandlord])
    def toggle_active(self, request, pk=None):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        listing.is_active = not listing.is_active
        listing.save()
        return Response({"is_active": listing.is_active})
