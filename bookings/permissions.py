from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrBookingParticipant(BasePermission):
    """
    Booking access rules:
    - Admins (staff / superuser) have full access.
    - LANDLORD can manage bookings for their own listings.
    - TENANT can manage (and cancel) their own bookings.
    """
    def has_permission(self, request, view):
        # The user must be authenticated to access any booking-related action.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admins always have full access to any booking
        if user.is_staff or user.is_superuser:
            return True

        # Tenants can cancel ONLY their own bookings
        if view.action == 'cancel':
            return obj.tenant == user

        # Landlords can confirm or reject bookings for their own listings
        if view.action in ['confirm', 'reject']:
            return obj.listing.landlord == user

        # In all other actions (retrieve, update, etc.)
        # access is allowed if the user is either the tenant
        # or the landlord of the related listing
        return obj.tenant == user or obj.listing.landlord == user
