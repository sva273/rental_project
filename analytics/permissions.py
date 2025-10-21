from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Grants access to:
    - The owner of the object (obj.user == request.user)
    - Administrators (user.is_staff)
    """
    def has_permission(self, request, view):
        # Only authenticated users are allowed to proceed
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Safe methods (GET, HEAD, OPTIONS) are allowed for the owner or admin
        if request.method in SAFE_METHODS:
            return request.user.is_staff or obj.user == request.user
        # Write operations are allowed only to the owner
        return obj.user == request.user
