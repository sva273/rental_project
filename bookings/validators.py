from datetime import date
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from .config import get_max_booking_end_date


def validate_booking_dates(start_date, end_date, use_drf=False, instance=None):
    """
    Validate the start and end dates of a booking.

    Rules enforced:
        1. Start date must not be later than end date.
        2. Booking must be at least one night.
        3. For new bookings, start date cannot be in the past.
        4. Booking duration cannot exceed the maximum allowed period (3 months).
    Args:
        start_date (date): The booking start date.
        end_date (date): The booking end date.
        use_drf (bool): If True, raises DRF ValidationError; otherwise, Django ValidationError.
        instance (Booking, optional): Existing booking instance. Past dates are allowed for existing bookings.
    Raises:
        DjangoValidationError or DRFValidationError: If any validation rule is violated.
    """
    if not start_date or not end_date:
        return

    error = DRFValidationError if use_drf else DjangoValidationError
    today = date.today()

    # Ensure start_date is not later than end_date
    if start_date > end_date:
        raise error("Start date cannot be later than end date.")

    # Ensure booking duration is at least one night
    if start_date == end_date:
        raise error("The booking must be at least 1 night.")

    # For new bookings, prevent start dates in the past
    if (not instance or not instance.pk) and start_date < today:
        raise error("Start date cannot be in the past.")

    max_end_date = get_max_booking_end_date(start_date)

    # Ensure booking does not exceed the maximum allowed duration
    if end_date > max_end_date:
        raise error(
            "The booking cannot exceed 3 months. "
            "For a longer stay, please contact the administration directly."
        )
