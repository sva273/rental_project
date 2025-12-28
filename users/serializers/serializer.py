from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import re

User = get_user_model()


def validate_phone_number(value):
    if value and not re.fullmatch(r"\d{10,15}", value):
        raise serializers.ValidationError(
            "Phone number must contain digits only (10–15 characters)."
        )
    return value


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password], allow_blank=True
    )
    password2 = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )  # для подтверждения пароля
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # При создании (POST) пароли обязательны
        if self.instance is None:  # Creating new instance
            self.fields['password'].required = True
            self.fields['password2'].required = True

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "password",
            "password2",
        )
        extra_kwargs = {
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
    
    def to_representation(self, instance):
        """Remove password fields from response"""
        data = super().to_representation(instance)
        data.pop('password', None)
        data.pop('password2', None)
        return data

    def validate(self, attrs):
        """Validate that both passwords match."""
        # Only validate passwords if they are provided (during creation or password change)
        if attrs.get("password") and attrs.get("password2"):
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        """Create a new user with a hashed password."""
        validated_data.pop("password2", None)
        password = validated_data.pop("password", None)
        if not password:
            raise serializers.ValidationError({"password": "Password is required for registration."})
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update user instance (including optional password change)."""
        password = validated_data.pop("password", None)
        validated_data.pop("password2", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()
        return instance
