from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Booking, BookingStatusChoices
from .config import (
    notify_new_booking,
    notify_status_change,
    notify_booking_dates_changed,
    notify_booking_deleted,
)


@receiver(pre_save, sender=Booking)
def cache_original_data(sender, instance, **kwargs):
    """
    Cache original start_date, end_date, status and is_deleted before saving.
    """
    if instance.pk:
        try:
            original = Booking.all_objects.get(pk=instance.pk)
            instance._original_start_date = original.start_date
            instance._original_end_date = original.end_date
            instance._original_status = original.status
            instance._original_is_deleted = original.is_deleted
        except Booking.DoesNotExist:
            instance._original_start_date = None
            instance._original_end_date = None
            instance._original_status = None
            instance._original_is_deleted = False
    else:
        instance._original_start_date = None
        instance._original_end_date = None
        instance._original_status = None
        instance._original_is_deleted = False


@receiver(post_save, sender=Booking)
def booking_created_or_updated(sender, instance, created, **kwargs):
    """
    Handles Booking creation, update, status change, and soft-delete events.
    """
    landlord_email = instance.listing.landlord.email
    tenant_email = instance.tenant.email

    if created:
        notify_new_booking(instance.listing.title, landlord_email, tenant_email)
        return

    # Check if dates changed
    original_start = getattr(instance, "_original_start_date", None)
    original_end = getattr(instance, "_original_end_date", None)
    if original_start and original_end:
        if original_start != instance.start_date or original_end != instance.end_date:
            notify_booking_dates_changed(instance, original_start, original_end)

    # Check status changes
    original_status = getattr(instance, "_original_status", None)
    if instance.status != original_status:
        if instance.status == BookingStatusChoices.CONFIRMED:
            notify_status_change(instance.listing.title, "confirmed", landlord_email, tenant_email)
        elif instance.status == BookingStatusChoices.REJECTED:
            notify_status_change(instance.listing.title, "rejected", landlord_email, tenant_email)
        elif instance.status == BookingStatusChoices.CANCELLED:
            notify_status_change(instance.listing.title, "cancelled", landlord_email, tenant_email)

    # Check soft-delete
    original_is_deleted = getattr(instance, "_original_is_deleted", False)
    if not original_is_deleted and instance.is_deleted:
        notify_booking_deleted(instance.listing.title, landlord_email, tenant_email)
