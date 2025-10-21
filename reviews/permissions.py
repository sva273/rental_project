from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission:
    - Read-only access for all users.
    - Update and delete allowed only for the review author.
    - Approval allowed only for admin (handled in a separate method).
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Prevent LANDLORD and STAFF from creating a review
        if request.method == 'POST':
            if user.is_staff or user.groups.filter(name__iexact='LANDLORD').exists():
                return False

        return True

