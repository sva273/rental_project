from django.contrib import admin, messages
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    """
    Admin interface for Listing model:

    Features:
    - Displays main fields in list view.
    - Supports filtering by city, daily_enabled, and is_active.
    - Allows searching by title, description, city, country, and street.
    - Supports inline editing for is_active field.
    - Includes bulk actions: activate, deactivate, toggle daily booking availability.
    """

    list_display = [
        'id',
        'title',
        'landlord',
        'city',
        'price_per_day',
        'daily_enabled',
        'average_rating',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'city',
        'daily_enabled',
        'is_active',
    ]
    list_editable = [
        'is_active',
    ]
    search_fields = ['title', 'description', 'city', 'country', 'street']
    ordering = ['-created_at']
    list_per_page = 25

    actions = ['activate_listings', 'deactivate_listings', 'toggle_daily_enabled']

    @admin.action(description="Activate selected listings")
    def activate_listings(self, request, queryset):
        """
        Bulk action to activate listings:
        - Iterates over the selected listings.
        - If a listing is not active, sets is_active=True and saves.
        - Updates a counter to show how many listings were activated.
        """
        updated = 0
        for listing in queryset:
            # Only activate if the listing is currently inactive
            if not listing.is_active:
                listing.is_active = True
                listing.save()
                updated += 1
        self.message_user(request, f"{updated} listings activated.", messages.SUCCESS)

    @admin.action(description="Deactivate selected listings")
    def deactivate_listings(self, request, queryset):
        """
        Bulk action to deactivate listings:
        - Iterates over the selected listings.
        - If a listing is active, sets is_active=False and saves.
        - Updates a counter to show how many listings were deactivated.
        """
        updated = 0
        for listing in queryset:
            # Only deactivate if the listing is currently active
            if listing.is_active:
                listing.is_active = False
                listing.save()
                updated += 1
        self.message_user(request, f"{updated} listings deactivated.", messages.WARNING)

    @admin.action(description="Toggle daily booking availability")
    def toggle_daily_enabled(self, request, queryset):
        """
        Bulk action to toggle daily booking availability:
        - Iterates over selected listings.
        - Flips the daily_enabled boolean for each listing.
        - Updates a counter to show how many listings were updated.
        """
        updated = 0
        for listing in queryset:
            listing.daily_enabled = not listing.daily_enabled
            listing.save()
            updated += 1
        self.message_user(request, f"Daily booking toggled for {updated} listings.", messages.INFO)
