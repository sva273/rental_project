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
    User authentication:
    - register: user registration
    - login: user login
    - logout: user logout
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="User registration",
        operation_description="Creates a new user and returns an authentication token.",
        request_body=UserSerializer,
        responses={201: openapi.Response('User created', UserSerializer)}
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
                return Response({'detail': 'A user with this email already exists.'}, status=400)
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="User login",
        operation_description="Validates email and password and returns an authentication token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password')
            }
        ),
        responses={200: openapi.Response('Login successful', UserSerializer)}
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
        operation_summary="User logout",
        operation_description="Deletes the current user's token, logging them out of the system.",
        responses={204: 'Token deleted, logout successful'}
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        token = getattr(request, 'auth', None)
        if token:
            token.delete()
            return Response({'detail': 'You have been logged out'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Token not found'}, status=status.HTTP_400_BAD_REQUEST)


