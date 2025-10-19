from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrBookingParticipant(BasePermission):
    """
    Доступ к бронированию:
    - Админ имеет полный доступ.
    - LANDLORD может управлять бронированиями своих объектов.
    - TENANT может управлять своими бронированиями.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        if view.action == 'cancel':
            return obj.tenant == user
        if view.action in ['confirm', 'reject']:
            return obj.listing.landlord == user
        return obj.tenant == user or obj.listing.landlord == user
