from django.db.models import Avg
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
    - Supports filters: property_type, country, city, is_active, min_price, max_price.
    """

    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsAdminOrLandlord]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title", "description", "city", "country"]
    ordering_fields = ["price_per_day", "created_at", "average_rating"]
    ordering = ["-created_at"]
    filterset_fields = ["property_type", "country", "city", "is_active"]

    def get_queryset(self):
        """
        Returns listings based on the user's role and optional filters.
        Adds annotation 'average_rating' for sorting.
        """
        user = self.request.user
        queryset = Listing.objects.filter(is_deleted=False)

        queryset = queryset.annotate(average_rating_value=Avg("reviews__rating"))

        # Price filtering
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        try:
            if min_price:
                queryset = queryset.filter(price_per_day__gte=float(min_price))
            if max_price:
                queryset = queryset.filter(price_per_day__lte=float(max_price))
        except ValueError:
            pass

        # Role-based filtering
        if user.groups.filter(name__iexact="LANDLORD").exists() and not user.is_staff:
            queryset = queryset.filter(landlord=user)
        elif not user.is_staff:
            queryset = queryset.filter(is_active=True)

        return queryset

    def get_ordering(self):
        ordering = self.request.query_params.get("ordering")
        if ordering:
            if "average_rating" in ordering:
                return [ordering.replace("average_rating", "average_rating")]
            return [ordering]
        return super().get_ordering()

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

    @swagger_auto_schema(
        operation_summary="List Listings",
        operation_description="Returns listings based on user role and filters.",
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Search by title, description, city, country",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "ordering",
                openapi.IN_QUERY,
                description="Order by price_per_day, created_at, average_rating",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "min_price",
                openapi.IN_QUERY,
                description="Minimum price",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "max_price",
                openapi.IN_QUERY,
                description="Maximum price",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "city", openapi.IN_QUERY, description="City", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "country",
                openapi.IN_QUERY,
                description="Country",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "property_type",
                openapi.IN_QUERY,
                description="Property type",
                type=openapi.TYPE_STRING,
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
        responses={
            201: openapi.Response(description="Created", schema=ListingSerializer)
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Listing",
        operation_description="TENANT sees only active listings. View is recorded.",
        responses={
            200: openapi.Response(description="OK", schema=ListingSerializer),
            403: "Forbidden",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        user = request.user
        if (
            not user.is_staff
            and not user.groups.filter(name__iexact="LANDLORD").exists()
        ):
            record_listing_view(user, listing)
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Listing",
        operation_description="Only the owner or ADMIN can update the listing.",
        request_body=ListingSerializer,
        responses={
            200: openapi.Response(description="Updated", schema=ListingSerializer),
            403: "Forbidden",
        },
    )
    def update(self, request, *args, **kwargs):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Listing",
        operation_description="Only the owner or ADMIN can partially update the listing.",
        request_body=ListingSerializer,
        responses={
            200: openapi.Response(description="Updated", schema=ListingSerializer),
            403: "Forbidden",
        },
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
        return Response(
            {"detail": "Listing marked as deleted."}, status=status.HTTP_204_NO_CONTENT
        )

    @swagger_auto_schema(
        operation_summary="Toggle Listing Active Status",
        operation_description="Toggles the listing's active status. Only the owner or ADMIN.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={}),
        responses={
            200: openapi.Response(
                description="OK", schema=ToggleActiveResponseSerializer
            ),
            403: "Forbidden",
        },
    )
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated, IsAdminOrLandlord],
    )
    def toggle_active(self, request, pk=None):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        listing.is_active = not listing.is_active
        listing.save()
        return Response({"is_active": listing.is_active})
