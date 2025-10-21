from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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
    http_method_names = ['get', 'put', 'patch']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()

        # Admin can access all users
        if user.is_staff:
            return User.objects.all()

        # Normal user can only access their own profile
        return User.objects.filter(id=user.id)

    def perform_update(self, serializer):
        password = self.request.data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()

    @swagger_auto_schema(
        operation_summary="Retrieve profile",
        operation_description="Returns the profile data of the currently authenticated user.",
        responses={
            200: openapi.Response(description="Success", schema=UserSerializer),
            403: openapi.Response(description="Forbidden")
        }
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
            403: openapi.Response(description="Forbidden")
        }
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
            403: openapi.Response(description="Forbidden")
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
