from django.core.mail import EmailMessage
from django.conf import settings


def safe_send_mail(subject, message, recipients):
    """
    Safely sends an email with UTF-8 encoding.
    Ensures the app will not crash if email sending fails.
    Logs the error to console for debugging.
    """
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        email.encoding = "utf-8"
        email.send()
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email '{subject}' to {recipients}: {e}")


def notify_listing_created(listing):
    """
    Sends email notification to the landlord when a new listing is created.
    """
    subject = f"New Listing Created: {listing.title}"
    message = (
        f'Your listing "{listing.title}" has been successfully published.\n\n'
        f"Thank you for using our platform!"
    )
    safe_send_mail(subject, message, [listing.landlord.email])


def notify_listing_updated(listing):
    """
    Sends email notification to the landlord when an existing listing is updated.
    """
    subject = f"Listing Updated: {listing.title}"
    message = f'Your listing "{listing.title}" has been updated.'
    safe_send_mail(subject, message, [listing.landlord.email])
