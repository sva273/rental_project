from django.contrib import admin, messages
from .models import Listing
from bookings.models import Booking
from reviews.models import Review


# === Inline for Review  ===
class ReviewInline(admin.TabularInline):
    """Inline reviews inside the Booking inline."""
    model = Review
    extra = 0
    readonly_fields = ("tenant", "rating", "comment", "created_at")
    fields = ("tenant", "rating", "comment", "is_approved", "created_at")
    ordering = ("-created_at",)
    show_change_link = True
    can_delete = False


# === Inline for Booking ===
class BookingInline(admin.TabularInline):
    """Inline bookings inside the Listing admin page, with nested reviews."""
    model = Booking
    extra = 0
    readonly_fields = ("tenant", "start_date", "end_date", "status", "total_price")
    fields = ("tenant", "start_date", "end_date", "status", "total_price", "parking_included")
    show_change_link = True
    ordering = ("-created_at",)
    can_delete = False
    inlines = [ReviewInline]


# === ListingAdmin ===
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title", "landlord", "city", "price_per_day", "daily_enabled",
        "average_rating", "is_active", "created_at",
    ]
    list_filter = ["city", "daily_enabled", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["title", "description", "city", "country", "street"]
    ordering = ["-created_at"]
    list_per_page = 25
    readonly_fields = ["average_rating", "reviews_count", "created_at", "updated_at"]

    inlines = [BookingInline]  # Показываем бронирования с вложенными отзывами

    # === Bulk actions ===
    actions = ["activate_listings", "deactivate_listings", "toggle_daily_enabled"]

    @admin.action(description="Activate selected listings")
    def activate_listings(self, request, queryset):
        updated = 0
        for listing in queryset:
            if not listing.is_active:
                listing.is_active = True
                listing.save()
                updated += 1
        self.message_user(request, f"{updated} listings activated.", messages.SUCCESS)

    @admin.action(description="Deactivate selected listings")
    def deactivate_listings(self, request, queryset):
        updated = 0
        for listing in queryset:
            if listing.is_active:
                listing.is_active = False
                listing.save()
                updated += 1
        self.message_user(request, f"{updated} listings deactivated.", messages.WARNING)

    @admin.action(description="Toggle daily booking availability")
    def toggle_daily_enabled(self, request, queryset):
        updated = 0
        for listing in queryset:
            listing.daily_enabled = not listing.daily_enabled
            listing.save()
            updated += 1
        self.message_user(
            request, f"Daily booking toggled for {updated} listings.", messages.INFO
        )
