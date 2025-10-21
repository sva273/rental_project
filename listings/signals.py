from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Listing


def send_console_mail(subject, message, recipient_list):
    """
    Send an email with correct UTF-8 encoding so that the Subject displays correctly in the console.
    """
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    email.encoding = 'utf-8'
    email.send()


@receiver(post_save, sender=Listing)
def listing_created_or_updated(sender, instance, created, **kwargs):
    update_fields = kwargs.get('update_fields')

    # If created — always send notification
    if created:
        subject = f'New Listing Created: {instance.title}'
        message = f'Your listing "{instance.title}" has been successfully published.'
        send_console_mail(subject, message, [instance.landlord.email])
        return

    # If only the views_count field was updated — do not send notification
    if update_fields is not None and update_fields == {'views_count'}:
        return

    # Otherwise — consider it a significant update
    subject = f'Listing Updated: {instance.title}'
    message = f'Your listing "{instance.title}" has been updated.'
    send_console_mail(subject, message, [instance.landlord.email])








