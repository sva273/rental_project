from django.contrib import admin, messages
from .models import Booking, BookingStatusChoices
from django.utils.timezone import localtime, make_aware
from datetime import datetime, time

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'listing',
        'tenant',
        'formatted_start_datetime',
        'formatted_end_datetime',
        'duration_days',
        'status',
        'total_price',
        'parking_included',
        'created_at',
    )

    list_filter = (
        'status',
        'parking_included',
        'created_at',
        'listing__city',
    )

    search_fields = (
        'listing__title',
        'tenant__email',
        'tenant__username',
        'listing__city',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'total_price',
        'duration_days',
        'formatted_start_datetime',
        'formatted_end_datetime',
    )

    ordering = ('-created_at',)

    fieldsets = (
        ('Main Info', {
            'fields': ('listing', 'tenant', 'status')
        }),
        ('Dates & Conditions', {
            'fields': ('start_date', 'end_date', 'parking_included')
        }),
        ('Financials', {
            'fields': ('total_price',)
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at', 'is_deleted')
        }),
    )

    list_editable = ('status',)
    list_per_page = 25

    actions = ['mark_as_confirmed', 'mark_as_cancelled', 'remove_parking']

    def duration_days(self, obj):
        """Number of rental days"""
        return (obj.end_date - obj.start_date).days + 1
    duration_days.short_description = 'Days'

    def formatted_start_datetime(self, obj):
        """Check-in time at 14:00, formatted"""
        check_in_time = time(hour=14, minute=0)
        dt = make_aware(datetime.combine(obj.start_date, check_in_time))
        return localtime(dt).strftime("%b %d, %Y, %I:%M %p")
    formatted_start_datetime.admin_order_field = 'start_date'
    formatted_start_datetime.short_description = 'Check-in'

    def formatted_end_datetime(self, obj):
        """Check-out time at 12:00, formatted"""
        check_out_time = time(hour=12, minute=0)
        dt = make_aware(datetime.combine(obj.end_date, check_out_time))
        return localtime(dt).strftime("%b %d, %Y, %I:%M %p")
    formatted_end_datetime.admin_order_field = 'end_date'
    formatted_end_datetime.short_description = 'Check-out'

    @admin.action(description="Mark selected bookings as Confirmed")
    def mark_as_confirmed(self, request, queryset):
        updated = 0
        for booking in queryset:
            booking.status = BookingStatusChoices.CONFIRMED
            booking.save()
            updated += 1
        self.message_user(request, f"{updated} bookings marked as confirmed.", messages.SUCCESS)

    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_as_cancelled(self, request, queryset):
        updated = 0
        for booking in queryset:
            booking.status = BookingStatusChoices.REJECTED
            booking.save()
            updated += 1
        self.message_user(request, f"{updated} bookings marked as cancelled.", messages.WARNING)

    @admin.action(description="Remove parking from selected bookings")
    def remove_parking(self, request, queryset):
        updated = 0
        for booking in queryset:
            booking.parking_included = False
            booking.save()
            updated += 1
        self.message_user(request, f"Parking removed from {updated} bookings.", messages.INFO)
