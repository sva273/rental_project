from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Разрешает доступ:
    - Владелец записи (user == request.user)
    - Администратор (user.is_staff)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Безопасные методы — разрешены владельцу или админу
        if request.method in SAFE_METHODS:
            return request.user.is_staff or obj.user == request.user
        # Создание — разрешено владельцу
        return obj.user == request.user
