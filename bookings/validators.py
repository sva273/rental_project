from datetime import date
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from .config import get_max_booking_end_date

def validate_booking_dates(start_date, end_date, use_drf=False):
    if not start_date or not end_date:
        return

    error = DRFValidationError if use_drf else DjangoValidationError
    today = date.today()

    if start_date > end_date:
        raise error("Start date cannot be later than end date.")

    if start_date == end_date:
        raise error("The booking must be at least 1 night.")

    if start_date < today:
        raise error("Start date cannot be in the past.")

    max_end_date = get_max_booking_end_date(start_date)

    if end_date > max_end_date:
        raise error(
            "The booking cannot exceed 3 months. "
            "For a longer stay, please contact the administration directly."
        )
