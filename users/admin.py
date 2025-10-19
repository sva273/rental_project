from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_per_page = 25

    fieldsets = (
        ('Main Information', {
            'fields': ('email', 'password', 'first_name', 'last_name', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_active', 'is_staff'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')

    actions = ['activate_users', 'deactivate_users', 'set_role_to_tenant', 'set_role_to_landlord']

    @admin.action(description="Activate selected users")
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} users activated.", messages.SUCCESS)

    @admin.action(description="Deactivate selected users")
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} users deactivated.", messages.WARNING)

    @admin.action(description="Set role to 'tenant'")
    def set_role_to_tenant(self, request, queryset):
        updated = queryset.update(role='tenant')
        self.message_user(request, f"{updated} users set to role 'tenant'.", messages.INFO)

    @admin.action(description="Set role to 'landlord'")
    def set_role_to_landlord(self, request, queryset):
        updated = queryset.update(role='landlord')
        self.message_user(request, f"{updated} users set to role 'landlord'.", messages.INFO)
