from django.contrib import admin, messages
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
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
        self.message_user(request, f"Daily booking toggled for {updated} listings.", messages.INFO)
