from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission for Review objects.

    Rules:
    - SAFE_METHODS (GET, HEAD, OPTIONS) are allowed for all authenticated users.
    - POST (create) is only allowed for regular tenants; LANDLORD and STAFF cannot create reviews.
    - Update (PUT/PATCH) and delete (DELETE) permissions should be further restricted to the review author.
    - Approval of reviews is handled separately (not in this permission class).

    Methods:
    - has_permission(request, view): checks general access based on HTTP method and user role.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False  # Reject unauthenticated users

        # Restrict review creation for STAFF and LANDLORD
        if request.method == 'POST':
            if user.is_staff or user.groups.filter(name__iexact='LANDLORD').exists():
                return False

        # All other methods (GET, HEAD, OPTIONS, PUT, PATCH, DELETE) are allowed
        return True


