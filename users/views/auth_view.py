from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers.serializer import UserSerializer

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    """
    Аутентификация пользователей:
    - register: регистрация нового пользователя
    - login: вход в систему
    - logout: выход из системы
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создаёт нового пользователя и возвращает токен для аутентификации.",
        request_body=UserSerializer,
        responses={201: openapi.Response('Пользователь создан', UserSerializer)}
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            data = UserSerializer(user).data
            data['token'] = token.key
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            if 'email' in serializer.errors:
                return Response({'detail': 'Пользователь с таким email уже существует.'}, status=400)
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="Вход пользователя",
        operation_description="Проверяет email и пароль, возвращает токен для аутентификации.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль пользователя')
            }
        ),
        responses={200: openapi.Response('Успешный вход', UserSerializer)}
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user).data
        data['token'] = token.key
        return Response(data)

    @swagger_auto_schema(
        operation_summary="Выход пользователя",
        operation_description="Удаляет текущий токен пользователя, тем самым разлогинивая его.",
        responses={204: 'Токен удалён, выход выполнен'}
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        token = getattr(request, 'auth', None)
        if token:
            token.delete()
            return Response({'detail': 'Вы вышли из системы'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Токен не найден'}, status=status.HTTP_400_BAD_REQUEST)


