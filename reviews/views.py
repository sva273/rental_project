from django.utils import timezone
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from bookings.choices import BookingStatusChoices
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from bookings.models import Booking
from reviews.permissions import IsAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Review Management ViewSet

    Roles and Permissions:
    - TENANT: can create reviews for listings they stayed in and edit their own reviews.
    - LANDLORD: can view reviews for their own listings (approved only).
    - ADMIN: can view, approve, and manage all reviews.

    Serializer:
    - Uses ReviewSerializer for all operations.
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Returns reviews according to user role:
        - Admin sees all reviews.
        - LANDLORD sees only reviews on their listings (approved only).
        - TENANT sees only their own approved reviews.
        Uses cache for frequently accessed data.
        """
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        
        user = self.request.user
        
        # Build cache key
        cache_key = f"reviews_queryset_{user.id if user.is_authenticated else 'anon'}"
        
        # Try to get from cache
        cached_queryset = cache.get(cache_key)
        if cached_queryset is not None:
            return cached_queryset
        
        queryset = Review.objects.select_related("tenant", "listing", "listing__landlord")
        if user.is_staff:
            result_queryset = queryset.all()
        elif user.is_landlord():
            result_queryset = queryset.filter(listing__landlord=user, is_approved=True)
        else:
            # TENANT
            result_queryset = queryset.filter(tenant=user, is_approved=True)
        
        # Cache for 5 minutes (only for GET requests)
        if self.request.method == 'GET':
            cache.set(cache_key, result_queryset, 300)
        
        return result_queryset

    def perform_create(self, serializer):
        """
        Creates a new review if the user is a TENANT and has a completed booking.

        Logic:
        1. If user is STAFF or LANDLORD → raise ValidationError.
        2. Check for a confirmed booking with an end date in the past.
           - If none exists → raise ValidationError.
        3. Save review with tenant=user and is_approved=False.
        """
        listing = serializer.validated_data["listing"]
        user = self.request.user

        # --- Prevent non-tenants from creating reviews ---
        if user.is_staff or user.is_landlord():
            raise ValidationError("Only a tenant can submit a review.")

        # --- Check if review already exists ---
        if Review.objects.filter(listing=listing, tenant=user).exists():
            raise ValidationError("You have already reviewed this listing.")

        # --- Ensure tenant has completed a confirmed booking ---
        has_completed_booking = Booking.objects.filter(
            listing=listing,
            tenant=user,
            status=BookingStatusChoices.CONFIRMED,
            end_date__lt=timezone.now(),
        ).exists()

        if not has_completed_booking:
            raise ValidationError(
                "You can leave a review only after completing your stay."
            )

        serializer.save(tenant=user, is_approved=False)
        
        # Clear cache when new review is created
        cache.delete(f"reviews_queryset_{user.id}")
        cache.delete(f"listing_{listing.id}")

    # --- CRUD and list methods with Swagger documentation ---
    @swagger_auto_schema(
        operation_summary="List reviews",
        operation_description="Returns a list of reviews depending on the user's role: admin — all, "
        "tenant — their own approved, landlord — reviews for their listings",
        responses={200: openapi.Response("Success", ReviewSerializer(many=True))},
    )
    def list(self, request, *args, **kwargs):
        """Get a list of reviews respecting user role."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create review",
        operation_description="Creates a review after a completed stay",
        request_body=ReviewSerializer,
        responses={201: openapi.Response("Created", ReviewSerializer())},
    )
    def create(self, request, *args, **kwargs):
        """Create a new review (only after completing a booking)."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve review",
        responses={200: openapi.Response("Success", ReviewSerializer())},
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific review by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update review",
        request_body=ReviewSerializer,
        responses={200: openapi.Response("Updated", ReviewSerializer())},
    )
    def update(self, request, *args, **kwargs):
        """Fully update a review (author only)."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update review",
        request_body=ReviewSerializer,
        responses={200: openapi.Response("Updated", ReviewSerializer())},
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a review (author only)."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete review",
        responses={204: openapi.Response("No Content")},
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a review (author only)."""
        return super().destroy(request, *args, **kwargs)

    # --- Custom action for approving reviews ---
    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    @swagger_auto_schema(
        operation_summary="Approve review",
        operation_description="Admin can approve a review to make it publicly visible.",
        responses={200: openapi.Response("Review approved", ReviewSerializer())},
    )
    def approve(self, request, pk=None):
        """
        Approves a review (sets is_approved=True).
        Available only to admins.
        Steps:
        1. Retrieve the review object.
        2. Set is_approved=True.
        3. Save the review.
        4. Return the serialized review.
        """
        review = self.get_object()
        review.is_approved = True
        review.save()
        
        # Clear cache for tenant
        cache.delete(f"reviews_queryset_{review.tenant.id}")
        
        # Clear cache for landlord
        if review.listing.landlord_id:
            cache.delete(f"reviews_queryset_{review.listing.landlord_id}")
        
        # Clear cache for listing
        cache.delete(f"listing_{review.listing.id}")
        
        # Try to clear all reviews cache patterns (works with django-redis)
        # This ensures all users see the updated review
        try:
            if hasattr(cache, 'delete_pattern'):
                cache.delete_pattern("reviews_queryset_*")
        except (AttributeError, NotImplementedError):
            # Fallback for LocMemCache - cache will expire naturally
            pass
        
        serializer = self.get_serializer(review)
        return Response(serializer.data)
