from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrLandlord(BasePermission):
    """
    Permission for Listing objects:
    - Read-only methods (GET, HEAD, OPTIONS) are allowed for any authenticated user.
    - Write methods (POST, PUT, PATCH, DELETE) are allowed only for admin or the listing owner (LANDLORD).
    """

    def has_permission(self, request, view):
        user = request.user
        # Allow safe methods for any authenticated user
        if request.method in SAFE_METHODS:
            return user.is_authenticated
        # For unsafe methods — only admin or LANDLORD
        return user.is_authenticated and (
            user.is_staff or user.groups.filter(name__iexact="LANDLORD").exists()
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin always has full access
        if user.is_staff:
            return True

        # LANDLORD — access only to their own listings
        if user.groups.filter(name__iexact="LANDLORD").exists():
            return obj.landlord == user

        # TENANT — only safe methods
        return request.method in SAFE_METHODS
