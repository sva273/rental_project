from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from users.serializers.serializer import UserSerializer

User = get_user_model()

class ProfileViewSet(viewsets.ModelViewSet):
    """
    Просмотр и редактирование профиля текущего пользователя.
    Поддерживаются только методы GET, PUT и PATCH.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()

        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def perform_update(self, serializer):
        password = self.request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()

    @swagger_auto_schema(
        operation_summary="Получить профиль",
        operation_description="Возвращает данные текущего пользователя.",
        responses={200: openapi.Response('Success', UserSerializer(many=False))}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить профиль",
        operation_description="Полностью обновляет данные профиля текущего пользователя.",
        request_body=UserSerializer,
        responses={200: openapi.Response('Success', UserSerializer(many=False))}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить профиль",
        operation_description="Частично обновляет данные профиля текущего пользователя.",
        request_body=UserSerializer,
        responses={200: openapi.Response('Success', UserSerializer(many=False))}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
