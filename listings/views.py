from django.db.models import Avg
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from listings.models import Listing
from listings.serializers import ListingSerializer
from listings.permissions import IsAdminOrLandlord

from analytics.services import record_listing_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ListingViewSet(viewsets.ModelViewSet):
    """
     Rental Listing Management:
    - TENANT can only view active listings.
    - LANDLORD and admin can create, edit, delete, and toggle active status.
    """
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsAdminOrLandlord]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'city', 'country']
    ordering_fields = ['price_per_day', 'created_at', 'avg_rating']
    ordering = ['-created_at']
    filterset_fields = ['property_type', 'country', 'city', 'is_active']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Listing.objects.none()

        queryset = Listing.objects.filter(is_deleted=False)

        # Filter by price
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        try:
            if min_price:
                queryset = queryset.filter(price_per_day__gte=float(min_price))
            if max_price:
                queryset = queryset.filter(price_per_day__lte=float(max_price))
        except ValueError:
            pass

        # LANDLORD — only their own listings
        if user.groups.filter(name__iexact='LANDLORD').exists() and not user.is_staff:
            queryset = queryset.filter(landlord=user)

        # TENANT — only active listings
        elif not user.is_staff:
            queryset = queryset.filter(is_active=True)

        # Annotate average rating
        return queryset.annotate(avg_rating=Avg('reviews__rating'))

    def get_ordering(self):
        ordering = self.request.query_params.get('ordering')
        if ordering:
            # Support ordering by average_rating → avg_rating
            if 'average_rating' in ordering:
                return [ordering.replace('average_rating', 'avg_rating')]
            return [ordering]
        return super().get_ordering()

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

    @swagger_auto_schema(
        operation_summary="List Listings",
        operation_description="""
            Returns a list of listings:
            - Admin sees all listings.
            - LANDLORD sees only their own listings.
            - TENANT sees only active listings.
            """,
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by title, description, city, country",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Ordering by price_per_day, created_at",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
            openapi.Parameter('city', openapi.IN_QUERY, description="City", type=openapi.TYPE_STRING),
            openapi.Parameter('country', openapi.IN_QUERY, description="Country", type=openapi.TYPE_STRING),
            openapi.Parameter('property_type', openapi.IN_QUERY, description="Property type", type=openapi.TYPE_STRING),
        ],
        responses={200: ListingSerializer(many=True)}
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Listing",
        operation_description="Create a new listing. Only available to LANDLORD or admin.",
        responses={201: ListingSerializer}
    )

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Listing",
        operation_description="Get a listing by ID. TENANT sees only active listings. Also records view history.",
        responses={200: ListingSerializer, 403: "Forbidden"}
    )

    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        user = request.user

        # Record view for TENANT
        if not user.is_staff and not user.groups.filter(name__iexact='LANDLORD').exists():
            record_listing_view(user, listing)

        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Listing",
        operation_description="Update a listing. Only the owner or admin can update.",
        responses={200: ListingSerializer, 403: "Forbidden"}
    )

    def update(self, request, *args, **kwargs):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Listing",
        operation_description="Marks the listing as deleted (is_deleted=True). Only the owner or admin.",
        responses={204: "Deleted", 403: "Forbidden"}
    )

    def destroy(self, request, *args, **kwargs):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        listing.is_deleted = True
        listing.save()
        return Response({'detail': 'Listing marked as deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Toggle Listing Active Status",
        operation_description="Toggle the active status of a listing (is_active). Only the owner or admin.",
        responses={200: "OK", 403: "Forbidden"}
    )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrLandlord])
    def toggle_active(self, request, pk=None):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        listing.is_active = not listing.is_active
        listing.save()
        return Response({'is_active': listing.is_active})
