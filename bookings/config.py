from datetime import date
from calendar import monthrange

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