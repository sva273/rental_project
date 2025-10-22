from datetime import date
from calendar import monthrange
from django.core.mail import EmailMessage
from django.conf import settings

MAX_BOOKING_MONTHS = 3

def get_max_booking_end_date(start_date: date) -> date:
    """
    Returns the maximum allowed end date for a booking,
    based on MAX_BOOKING_MONTHS after the start_date.
    """
    month = start_date.month + MAX_BOOKING_MONTHS
    year = start_date.year + (month - 1) // 12
    month = (month - 1) % 12 + 1

    try:
        return start_date.replace(year=year, month=month)
    except ValueError:
        day = min(start_date.day, monthrange(year, month)[1])
        return start_date.replace(year=year, month=month, day=day)

def safe_send_mail(subject: str, message: str, recipients: list):
    """
    Safely sends an email with UTF-8 encoding.
    Ensures the application does not crash if email sending fails.
    Errors are logged to the console.

    Args:
        subject (str): Email subject.
        message (str): Email body content.
        recipients (list): List of recipient email addresses.
    """
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        email.encoding = 'utf-8'
        email.send()
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send email '{subject}' to {recipients}: {e}")


def notify_new_booking(listing_title: str, landlord_email: str, tenant_email: str):
    """
    Sends notification emails for a newly created booking.

    Args:
        listing_title (str): Title of the listing.
        landlord_email (str): Email address of the listing owner.
        tenant_email (str): Email address of the tenant.
    """
    subject = f'New Booking: {listing_title}'
    safe_send_mail(subject, f'You have booked "{listing_title}". '
                            f'Please wait for confirmation.', [tenant_email])
    safe_send_mail(subject, f'Your listing "{listing_title}" has been booked.', [landlord_email])


def notify_status_change(listing_title: str, status: str, landlord_email: str, tenant_email: str):
    """
    Sends notification emails when a booking status changes.

    Args:
        listing_title (str): Title of the listing.
        status (str): New booking status ('confirmed', 'rejected', 'deleted').
        landlord_email (str): Email address of the listing owner.
        tenant_email (str): Email address of the tenant.
    """
    subject_map = {
        "confirmed": "Booking Confirmed",
        "rejected": "Booking Rejected",
        "deleted": "Booking Deleted",
    }
    subject = f"{subject_map.get(status, 'Booking Update')}: {listing_title}"
    message = f'The booking for "{listing_title}" has been {status}.'
    safe_send_mail(subject, message, [tenant_email, landlord_email])


def notify_booking_dates_changed(booking, old_start, old_end):
    """
    Sends notification emails when booking dates are updated.

    Args:
        booking (Booking): Booking instance with new dates.
        old_start (date): Original start date.
        old_end (date): Original end date.
    """
    subject = f'Booking Dates Updated: {booking.listing.title}'
    message = (
        f'The booking for "{booking.listing.title}" has been updated.\n'
        f'Previous dates: {old_start} → {old_end}\n'
        f'New dates: {booking.start_date} → {booking.end_date}'
    )
    recipients = [booking.tenant.email, booking.listing.landlord.email]
    safe_send_mail(subject, message, recipients)
