from django.contrib import admin, messages
from .models import Booking, BookingStatusChoices
from django.utils.timezone import localtime, make_aware
from datetime import datetime, time


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin interface for the Booking model.

    Displays booking information, allows filtering, searching,
    and bulk actions like confirming, cancelling bookings or removing parking.
    """

    list_display = (
        "id",
        "listing",
        "tenant",
        "formatted_start_datetime",
        "formatted_end_datetime",
        "duration_days",
        "status",
        "total_price",
        "parking_included",
        "created_at",
    )

    list_filter = (
        "status",
        "parking_included",
        "created_at",
        "listing__city",
    )

    search_fields = (
        "listing__title",
        "tenant__email",
        "tenant__username",
        "listing__city",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "total_price",
        "duration_days",
        "formatted_start_datetime",
        "formatted_end_datetime",
    )

    ordering = ("-created_at",)

    fieldsets = (
        ("Main Info", {"fields": ("listing", "tenant", "status")}),
        (
            "Dates & Conditions",
            {"fields": ("start_date", "end_date", "parking_included")},
        ),
        ("Financials", {"fields": ("total_price",)}),
        ("System Fields", {"fields": ("created_at", "updated_at", "is_deleted")}),
    )

    list_editable = ("status",)
    list_per_page = 25

    actions = ["mark_as_confirmed", "mark_as_cancelled", "remove_parking"]

    def duration_days(self, obj):
        """Number of rental days"""
        return (obj.end_date - obj.start_date).days

    duration_days.short_description = "Days"

    def formatted_start_datetime(self, obj):
        """Check-in time at 14:00, formatted"""
        check_in_time = time(hour=14, minute=0)
        dt = make_aware(datetime.combine(obj.start_date, check_in_time))
        return localtime(dt).strftime("%b %d, %Y, %I:%M %p")

    formatted_start_datetime.admin_order_field = "start_date"
    formatted_start_datetime.short_description = "Check-in"

    def formatted_end_datetime(self, obj):
        """Check-out time at 12:00, formatted"""
        check_out_time = time(hour=12, minute=0)
        dt = make_aware(datetime.combine(obj.end_date, check_out_time))
        return localtime(dt).strftime("%b %d, %Y, %I:%M %p")

    formatted_end_datetime.admin_order_field = "end_date"
    formatted_end_datetime.short_description = "Check-out"

    @admin.action(description="Mark selected bookings as Confirmed")
    def mark_as_confirmed(self, request, queryset):
        """
        Bulk action to mark selected bookings as Confirmed.

        Args:
            request: HttpRequest object.
            queryset: Queryset of selected Booking instances.

        Sends a success message after completion.
        """
        from django.core.cache import cache
        
        bookings_to_update = list(queryset)
        for booking in bookings_to_update:
            booking.status = BookingStatusChoices.CONFIRMED
        
        if bookings_to_update:
            Booking.objects.bulk_update(bookings_to_update, ['status'])
            # Clear cache for related listings
            listing_ids = {booking.listing_id for booking in bookings_to_update}
            for listing_id in listing_ids:
                cache.delete(f"listing_{listing_id}")
        
        self.message_user(
            request, f"{len(bookings_to_update)} bookings marked as confirmed.", messages.SUCCESS
        )

    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_as_cancelled(self, request, queryset):
        """
        Bulk action to mark selected bookings as Cancelled (Rejected).

        Args:
            request: HttpRequest object.
            queryset: Queryset of selected Booking instances.

        Sends a warning message after completion.
        """
        from django.core.cache import cache
        
        bookings_to_update = list(queryset)
        for booking in bookings_to_update:
            booking.status = BookingStatusChoices.REJECTED
        
        if bookings_to_update:
            Booking.objects.bulk_update(bookings_to_update, ['status'])
            # Clear cache for related listings
            listing_ids = {booking.listing_id for booking in bookings_to_update}
            for listing_id in listing_ids:
                cache.delete(f"listing_{listing_id}")
        
        self.message_user(
            request, f"{len(bookings_to_update)} bookings marked as cancelled.", messages.WARNING
        )

    @admin.action(description="Remove parking from selected bookings")
    def remove_parking(self, request, queryset):
        """
        Bulk action to remove parking from selected bookings.

        Args:
            request: HttpRequest object.
            queryset: Queryset of selected Booking instances.

        Sends an info message after completion.
        """
        bookings_to_update = list(queryset)
        for booking in bookings_to_update:
            booking.parking_included = False
        
        if bookings_to_update:
            Booking.objects.bulk_update(bookings_to_update, ['parking_included'])
        
        self.message_user(
            request, f"Parking removed from {len(bookings_to_update)} bookings.", messages.INFO
        )
