from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Booking, BookingStatusChoices


def send_console_mail(subject, message, recipient_list):
    """
    Sends an email with proper UTF-8 encoding so that the Subject displays correctly in the console.
    """
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    email.encoding = 'utf-8'
    email.send()


@receiver(post_save, sender=Booking)
def booking_created_or_updated(sender, instance, created, **kwargs):
    landlord_email = instance.listing.landlord.email
    tenant_email = instance.tenant.email

    if created:
        subject = f'New Booking: {instance.listing.title}'
        message_tenant = f'You have booked "{instance.listing.title}". Please wait for confirmation.'
        message_landlord = f'Your listing "{instance.listing.title}" has been booked.'
        send_console_mail(subject, message_tenant, [tenant_email])
        send_console_mail(subject, message_landlord, [landlord_email])
    else:
        if instance.status == BookingStatusChoices.CONFIRMED:
            subject = f'Booking Confirmed: {instance.listing.title}'
            message = f'The booking for "{instance.listing.title}" has been confirmed.'
            send_console_mail(subject, message, [tenant_email, landlord_email])
        elif instance.status == BookingStatusChoices.REJECTED:
            subject = f'Booking Rejected: {instance.listing.title}'
            message = f'The booking for "{instance.listing.title}" has been rejected.'
            send_console_mail(subject, message, [tenant_email, landlord_email])


@receiver(post_delete, sender=Booking)
def booking_deleted(sender, instance, **kwargs):
    landlord_email = instance.listing.landlord.email
    tenant_email = instance.tenant.email
    subject = f'Booking Deleted: {instance.listing.title}'
    message = f'The booking for "{instance.listing.title}" has been deleted.'
    send_console_mail(subject, message, [tenant_email, landlord_email])
