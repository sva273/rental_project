from django.utils import timezone
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
    Review management:
    - TENANT can create and edit their own reviews.
    - LANDLORD can see reviews for their own listings.
    - Admin can view and approve all reviews.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Returns reviews depending on user role:
        - Admin sees all reviews.
        - LANDLORD sees only reviews on their listings.
        - TENANT sees only their approved reviews.
        """
        user = self.request.user
        if user.is_staff:
            return Review.objects.all()
        if user.groups.filter(name__iexact='LANDLORD').exists():
            return Review.objects.filter(listing__landlord=user, is_approved=True)
        return Review.objects.filter(tenant=user, is_approved=True)

    def perform_create(self, serializer):
        """
        Creates a review if the current user is a TENANT and has a confirmed, completed booking.
        Review is created as unapproved (awaiting approval).
        """
        listing = serializer.validated_data['listing']
        user = self.request.user

        # Prevent review creation for LANDLORD or STAFF
        if user.is_staff or user.groups.filter(name__iexact='LANDLORD').exists():
            raise ValidationError("Only a tenant can submit a review.")

        # Check for completed confirmed booking
        has_completed_booking = Booking.objects.filter(
            listing=listing,
            tenant=user,
            status=BookingStatusChoices.CONFIRMED,
            end_date__lt=timezone.now()
        ).exists()

        if not has_completed_booking:
            raise ValidationError("You can leave a review only after completing your stay.")

        serializer.save(tenant=user, is_approved=False)

    @swagger_auto_schema(
        operation_summary="List reviews",
        operation_description="Returns a list of reviews depending on the user's role: admin — all, "
                              "tenant — their own approved, landlord — reviews for their listings",
        responses={200: openapi.Response('Success', ReviewSerializer(many=True))}
    )

    def list(self, request, *args, **kwargs):
        """Get a list of reviews respecting user role."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create review",
        operation_description="Creates a review after a completed stay",
        request_body=ReviewSerializer,
        responses={201: openapi.Response('Created', ReviewSerializer())}
    )
    def create(self, request, *args, **kwargs):
        """Create a new review (only after completing a booking)."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve review",
        responses={200: openapi.Response('Success', ReviewSerializer())}
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific review by ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update review",
        request_body=ReviewSerializer,
        responses={200: openapi.Response('Updated', ReviewSerializer())}
    )
    def update(self, request, *args, **kwargs):
        """Fully update a review (author only)."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update review",
        request_body=ReviewSerializer,
        responses={200: openapi.Response('Updated', ReviewSerializer())}
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a review (author only)."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete review",
        responses={204: openapi.Response('No Content')}
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a review (author only)."""
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    @swagger_auto_schema(
        operation_summary="Approve review",
        operation_description="Admin can approve a review to make it publicly visible.",
        responses={200: openapi.Response('Review approved', ReviewSerializer())}
    )
    def approve(self, request, pk=None):
        """
        Approves a review (sets is_approved=True).
        Available only to admins.
        """
        review = self.get_object()
        review.is_approved = True
        review.save()
        serializer = self.get_serializer(review)
        return Response(serializer.data)
