from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Django Admin configuration for the custom User model.

    Displays and manages users in the admin panel with role and status control.

    Fields:
    - id: User ID.
    - email: User email (used as login identifier).
    - first_name / last_name: User's personal information.
    - role: Custom role field ('tenant' or 'landlord').
    - is_active: Whether the user account is active.
    - is_staff: Admin site access permission.
    - is_superuser: Superuser status.
    - date_joined / last_login: Timestamps.

    Filters:
    - role, is_active, is_staff, is_superuser, date_joined.

    Search:
    - email, first_name, last_name.

    Ordering:
    - Default ordering by '-date_joined'.

    Actions:
    - activate_users: Bulk activate selected users.
    - deactivate_users: Bulk deactivate selected users.
    - set_role_to_tenant: Set selected users' role to 'tenant'.
    - set_role_to_landlord: Set selected users' role to 'landlord'.
    """

    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    list_filter = ("role", "is_active", "is_staff", "is_superuser", "date_joined")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    list_per_page = 25

    fieldsets = (
        (
            "Main Information",
            {"fields": ("email", "password", "first_name", "last_name", "role")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "role",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    readonly_fields = ("date_joined", "last_login")

    actions = [
        "activate_users",
        "deactivate_users",
        "set_role_to_tenant",
        "set_role_to_landlord",
    ]

    @admin.action(description="Activate selected users")
    def activate_users(self, request, queryset):
        """
        Bulk action to activate selected users.
        Sets is_active=True.
        """
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} users activated.", messages.SUCCESS)

    @admin.action(description="Deactivate selected users")
    def deactivate_users(self, request, queryset):
        """
        Bulk action to deactivate selected users.
        Sets is_active=False.
        """
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} users deactivated.", messages.WARNING)

    @admin.action(description="Set role to 'tenant'")
    def set_role_to_tenant(self, request, queryset):
        """
        Bulk action to set role of selected users to 'tenant'.
        """
        updated = queryset.update(role="tenant")
        self.message_user(
            request, f"{updated} users set to role 'tenant'.", messages.INFO
        )

    @admin.action(description="Set role to 'landlord'")
    def set_role_to_landlord(self, request, queryset):
        """
        Bulk action to set role of selected users to 'landlord'.
        """
        updated = queryset.update(role="landlord")
        self.message_user(
            request, f"{updated} users set to role 'landlord'.", messages.INFO
        )
