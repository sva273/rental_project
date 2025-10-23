from django.contrib.auth.models import AbstractUser
from django.db import models
from .choises import RoleChoices

# Create your models here.


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Fields:
    - username: Optional username (not unique). Mainly kept for compatibility.
    - email: Unique email address, used as the login identifier (USERNAME_FIELD).
    - role: User role, choices defined in RoleChoices (tenant, landlord, etc.).
    - date_joined: Timestamp of account creation.
    - phone_number: Optional phone number (digits only).

    Authentication:
    - USERNAME_FIELD is set to 'email'.
    - REQUIRED_FIELDS includes 'username'.

    Methods:
    - __str__: Returns the user's email.
    """

    username = models.CharField(max_length=30, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, choices=RoleChoices.CHOICES, default=RoleChoices.TENANT
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    phone_number = models.CharField(
        max_length=15, blank=True, null=True, help_text="Phone number digits only"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        """Return email as string representation of the user"""
        return self.email
