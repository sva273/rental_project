from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from users.serializers.serializer import UserSerializer

User = get_user_model()


class ProfileViewSet(viewsets.ModelViewSet):
    """
    View and edit the current user's profile.
    Only GET, PUT, and PATCH methods are supported.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "patch"]

    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()
        
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()

        # Admin can access all users
        if user.is_staff:
            return User.objects.all().order_by('id')

        # Normal user can only access their own profile
        return User.objects.filter(id=user.id).order_by('id')

    def get_object(self):
        """
        Override to return current user instead of requiring ID in URL.
        This allows PUT/PATCH to work on /profile/ without ID.
        """
        return self.request.user

    def perform_update(self, serializer):
        password = self.request.data.get("password")
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()

    @swagger_auto_schema(
        operation_summary="Retrieve profile",
        operation_description="Returns the profile data of the currently authenticated user.",
        responses={
            200: openapi.Response(description="Success", schema=UserSerializer),
            403: openapi.Response(description="Forbidden"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update profile",
        operation_description="Completely updates the current user's profile data.",
        request_body=UserSerializer,
        responses={
            200: openapi.Response(description="Success", schema=UserSerializer),
            400: openapi.Response(description="Validation Error"),
            403: openapi.Response(description="Forbidden"),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update profile",
        operation_description="Partially updates the current user's profile data.",
        request_body=UserSerializer,
        responses={
            200: openapi.Response(description="Success", schema=UserSerializer),
            400: openapi.Response(description="Validation Error"),
            403: openapi.Response(description="Forbidden"),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Override list to return current user's profile when accessing /profile/
        """
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update current user profile",
        operation_description="Update the current user's profile. Supports both PUT and PATCH methods.",
        request_body=UserSerializer,
        responses={
            200: openapi.Response(description="Success", schema=UserSerializer),
            400: openapi.Response(description="Validation Error"),
            403: openapi.Response(description="Forbidden"),
        },
        methods=['put', 'patch'],
    )
    @action(detail=False, methods=['put', 'patch'], url_path='me', url_name='update-me')
    def update_me(self, request):
        """
        Update current user's profile without requiring ID in URL.
        Works with both PUT and PATCH methods.
        Access via: PUT/PATCH /api/v1/profile/me/
        """
        instance = request.user
        partial = request.method == 'PATCH'
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Handle password separately if provided
        password = request.data.get("password")
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
