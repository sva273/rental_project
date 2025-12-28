"""
Email utility functions for the rental project.
"""
import logging
from typing import List
from django.core.mail import EmailMessage
from django.conf import settings

logger = logging.getLogger(__name__)


def safe_send_mail(subject: str, message: str, recipients: List[str]) -> None:
    """
    Safely sends an email with UTF-8 encoding.
    Ensures the application does not crash if email sending fails.
    Errors are logged using Django's logging system.

    Args:
        subject (str): Email subject.
        message (str): Email body content.
        recipients (List[str]): List of recipient email addresses.

    Returns:
        None
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
        logger.error(
            f"Failed to send email '{subject}' to {recipients}: {e}",
            exc_info=True
        )

