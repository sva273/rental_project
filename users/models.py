from django.contrib.auth.models import AbstractUser
from django.db import models
from .choises import RoleChoices

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=RoleChoices.CHOICES, default=RoleChoices.TENANT)
    date_joined = models.DateTimeField(auto_now_add=True)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Phone number digits only"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
