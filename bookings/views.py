from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError

from .models import Booking, BookingStatusChoices
from .serializers import BookingSerializer
from .permissions import IsAdminOrBookingParticipant


def with_booking(func):
    """
    Decorator to retrieve a Booking instance and check object permissions.
    Args:
        func: The view method to wrap.
    Returns:
        The wrapped view function with `booking` argument.
    """

    def wrapper(self, request, pk=None, *args, **kwargs):
        booking = self.get_object()
        self.check_object_permissions(request, booking)
        return func(self, request, booking, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing bookings.

    Permissions:
        - TENANT: Can create, cancel, and view their own bookings.
        - LANDLORD: Can confirm or reject bookings for their listings.
        - ADMIN/STAFF: Can view and manage all bookings.
    Features:
        - CRUD operations for bookings.
        - Custom actions: cancel, confirm, reject.
        - Role-based queryset filtering.
        - Swagger documentation for all endpoints.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsAdminOrBookingParticipant]

    def get_queryset(self):
        """
        Return the queryset of bookings depending on the user's role.

        Returns:
            QuerySet: Bookings visible to the current user.
        """
        user = self.request.user

        # If the user is not authenticated, return an empty queryset
        if not user.is_authenticated:
            return Booking.objects.none()

        # If the user is admin or staff, return all bookings
        if user.is_staff or user.is_superuser:
            return Booking.objects.all()

        # If the user is a landlord, return bookings for their listings only
        if user.groups.filter(name__iexact='LANDLORD').exists():
            return Booking.objects.filter(listing__landlord=user)

        ## Otherwise, the user is a tenant; return their own bookings
        return Booking.objects.filter(tenant=user)

    def perform_create(self, serializer):
        """
        Set tenant and default status before saving a new booking.

        Args:
            serializer (BookingSerializer): The serializer instance for creating a booking.
        """

        # Set tenant as current user and status as PENDING for new bookings
        serializer.save(tenant=self.request.user, status=BookingStatusChoices.PENDING)

    # --- Swagger аннотации ---
    swagger_docs = {
        'list': swagger_auto_schema(
            operation_summary="List Bookings",
            operation_description="Returns a list of bookings depending on the user's role",
            responses={200: openapi.Response(description="OK", schema=BookingSerializer(many=True))}
        ),
        'create': swagger_auto_schema(
            operation_summary="Create Booking",
            operation_description="TENANT creates a new booking. Status is set to PENDING.",
            request_body=BookingSerializer,
            responses={201: openapi.Response(description="Created", schema=BookingSerializer())}
        ),
        'retrieve': swagger_auto_schema(
            operation_summary="Retrieve Booking",
            responses={200: openapi.Response(description="OK", schema=BookingSerializer())}
        ),
        'update': swagger_auto_schema(
            operation_summary="Update Booking",
            request_body=BookingSerializer,
            responses={200: openapi.Response(description="Updated", schema=BookingSerializer())}
        ),
        'partial_update': swagger_auto_schema(
            operation_summary="Partial Update Booking",
            request_body=BookingSerializer,
            responses={200: openapi.Response(description="Updated", schema=BookingSerializer())}
        ),
        'destroy': swagger_auto_schema(
            operation_summary="Delete Booking",
            responses={204: openapi.Response(description="Deleted")}
        ),
        'cancel': swagger_auto_schema(
            operation_summary="Cancel Booking",
            operation_description="TENANT can cancel their booking if more than 24 hours remain before check-in.",
            responses={200: openapi.Response(description="Booking cancelled")}
        ),
        'confirm': swagger_auto_schema(
            operation_summary="Confirm Booking",
            operation_description="LANDLORD or ADMIN confirms the booking. Status → CONFIRMED.",
            responses={200: openapi.Response(description="Booking confirmed")}
        ),
        'reject': swagger_auto_schema(
            operation_summary="Reject Booking",
            operation_description="LANDLORD or ADMIN rejects the booking. Status → REJECTED.",
            responses={200: openapi.Response(description="Booking rejected")}
        ),
    }

    # --- CRUD methods ---
    @swagger_docs['list']
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.user.groups.filter(name__iexact='LANDLORD').exists() and not request.user.is_staff:
            queryset = queryset.filter(listing__landlord=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_docs['create']
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_docs['retrieve']
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_docs['update']
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_docs['partial_update']
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_docs['destroy']
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # --- Custom actions ---
    @swagger_auto_schema(
        operation_summary="Cancel Booking",
        operation_description="TENANT can cancel their booking if more than 24 hours remain before check-in.",
        responses={200: openapi.Response(description="Booking cancelled")}
    )
    @action(detail=True, methods=['post'])
    @with_booking
    def cancel(self, request, booking):
        """
        Cancel a booking if allowed.

        Args:
            request: The HTTP request object.
            booking (Booking): The booking instance to cancel.

        Returns:
            Response: Success or error message.
        """
        try:
            # Attempt to cancel the booking (checks 24h rule internally)
            booking.cancel()
        except ValidationError as e:
            # Return 400 if cancellation is not allowed
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Booking successfully cancelled.'})

    @swagger_auto_schema(
        operation_summary="Confirm Booking",
        operation_description="LANDLORD or ADMIN confirms the booking. Status → CONFIRMED.",
        responses={200: openapi.Response(description="Booking confirmed")}
    )
    @action(detail=True, methods=['post'])
    @with_booking
    def confirm(self, request, booking):
        """
        Confirm a booking if its status is PENDING.

        Args:
            request: The HTTP request object.
            booking (Booking): The booking instance to confirm.
        Returns:
            Response: Success or error message.
        """
        # Only allow confirmation if booking is still PENDING
        if booking.status != BookingStatusChoices.PENDING:
            return Response({'detail': 'This booking has already been processed.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update status to CONFIRMED and save
        booking.status = BookingStatusChoices.CONFIRMED
        booking.save()
        return Response({'detail': 'Booking confirmed.'})

    @swagger_auto_schema(
        operation_summary="Reject Booking",
        operation_description="LANDLORD or ADMIN rejects the booking. Status → REJECTED.",
        responses={200: openapi.Response(description="Booking rejected")}
    )
    @action(detail=True, methods=['post'])
    @with_booking
    def reject(self, request, booking):
        """
        Reject a booking if its status is PENDING.

        Args:
            request: The HTTP request object.
            booking (Booking): The booking instance to reject.
        Returns:
            Response: Success or error message.
        """
        # Only allow rejection if booking is still PENDING
        if booking.status != BookingStatusChoices.PENDING:
            return Response({'detail': 'This booking has already been processed.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update status to REJECTED and save
        booking.status = BookingStatusChoices.REJECTED
        booking.save()
        return Response({'detail': 'Booking rejected.'})