from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrLandlord(BasePermission):
    """
    Разрешает:
    - Чтение (GET, HEAD, OPTIONS) — всем авторизованным пользователям.
    - Запись (POST, PUT, PATCH, DELETE) — только администратору или владельцу объявления (LANDLORD).
    """
    def has_permission(self, request, view):
        user = request.user
        # Разрешить безопасные методы всем авторизованным
        if request.method in SAFE_METHODS:
            return user.is_authenticated
        # Для небезопасных — только админ или LANDLORD
        return user.is_authenticated and (
            user.is_staff or user.groups.filter(name__iexact='LANDLORD').exists()
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Администратор — всегда имеет доступ
        if user.is_staff:
            return True

        # LANDLORD — доступ только к своим объявлениям
        if user.groups.filter(name__iexact='LANDLORD').exists():
            return obj.landlord == user

        # TENANT — только безопасные методы
        return request.method in SAFE_METHODS

