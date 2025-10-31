from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from bookings.models import Booking
from listings.models import Listing
from reviews.models import Review

# === Inlines ===
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ("listing", "start_date", "end_date", "status", "total_price")
    fields = ("listing", "start_date", "end_date", "status", "total_price", "parking_included")
    show_change_link = True
    can_delete = False
    ordering = ("-created_at",)


class ListingInline(admin.TabularInline):
    model = Listing
    extra = 0
    readonly_fields = ("title", "city", "price_per_day", "is_active")
    fields = ("title", "city", "price_per_day", "is_active")
    show_change_link = True
    can_delete = False
    ordering = ("-created_at",)


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ("listing", "rating", "comment", "is_approved", "created_at")
    fields = ("listing", "rating", "comment", "is_approved", "created_at")
    show_change_link = True
    can_delete = False
    ordering = ("-created_at",)

# === UserAdmin с вложениями ===
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id", "email", "first_name", "last_name", "role",
        "is_active", "is_staff", "is_superuser", "date_joined"
    )
    list_filter = ("role", "is_active", "is_staff", "is_superuser", "date_joined")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    list_per_page = 25

    fieldsets = (
        ("Main Information", {"fields": ("email", "password", "first_name", "last_name", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",),
                "fields": ("email", "password1", "password2", "first_name", "last_name", "role", "is_active", "is_staff")}),
    )

    readonly_fields = ("date_joined", "last_login")

    inlines = [BookingInline, ListingInline, ReviewInline]

    actions = ["activate_users", "deactivate_users", "set_role_to_tenant", "set_role_to_landlord"]

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
        updated = queryset.update(role="tenant")
        self.message_user(request, f"{updated} users set to role 'tenant'.", messages.INFO)

    @admin.action(description="Set role to 'landlord'")
    def set_role_to_landlord(self, request, queryset):
        updated = queryset.update(role="landlord")
        self.message_user(request, f"{updated} users set to role 'landlord'.", messages.INFO)
