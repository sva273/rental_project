from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Разрешает:
    - Чтение всем пользователям.
    - Изменение и удаление — только автору отзыва.
    - Одобрение — только администратору (в отдельном методе).
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # Запретить создание отзыва для LANDLORD и STAFF
        if request.method == 'POST':
            if user.is_staff or user.groups.filter(name__iexact='LANDLORD').exists():
                return False

        return True

