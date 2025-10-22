from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import Booking, BookingStatusChoices
from .config import (
    notify_new_booking,
    notify_status_change,
    notify_booking_dates_changed
)


@receiver(pre_save, sender=Booking)
def cache_original_dates(sender, instance, **kwargs):
    """
    Cache original start_date and end_date before saving.
    """
    if instance.pk:
        try:
            original = Booking.all_objects.get(pk=instance.pk)
            instance._original_start_date = original.start_date
            instance._original_end_date = original.end_date
        except Booking.DoesNotExist:
            instance._original_start_date = None
            instance._original_end_date = None


@receiver(post_save, sender=Booking)
def booking_created_or_updated(sender, instance, created, **kwargs):
    """
    Handles Booking creation and update events.

    - On creation: sends notifications for a new booking.
    - On update:
        - Sends notifications if booking dates have changed.
        - Sends notifications if booking status changed to confirmed or rejected.
    """
    landlord_email = instance.listing.landlord.email
    tenant_email = instance.tenant.email

    if created:
        # New booking
        notify_new_booking(instance.listing.title, landlord_email, tenant_email)
    else:
        # Check if dates changed
        original_start = getattr(instance, "_original_start_date", None)
        original_end = getattr(instance, "_original_end_date", None)
        if original_start and original_end:
            if original_start != instance.start_date or original_end != instance.end_date:
                notify_booking_dates_changed(instance, original_start, original_end)

        # Check status changes
        if instance.status == BookingStatusChoices.CONFIRMED:
            notify_status_change(instance.listing.title, "confirmed", landlord_email, tenant_email)
        elif instance.status == BookingStatusChoices.REJECTED:
            notify_status_change(instance.listing.title, "rejected", landlord_email, tenant_email)


@receiver(post_delete, sender=Booking)
def booking_deleted(sender, instance, **kwargs):
    """
    Handles Booking deletion events.
    """
    landlord_email = instance.listing.landlord.email
    tenant_email = instance.tenant.email
    notify_status_change(instance.listing.title, "deleted", landlord_email, tenant_email)
