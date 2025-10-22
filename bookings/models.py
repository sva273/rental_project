from datetime import datetime, time, timedelta
from django.utils.timezone import now, make_aware
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from listings.models import Listing
from .choices import BookingStatusChoices
from .validators import validate_booking_dates

# Create your models here.

CHECK_IN_TIME = time(14, 0)
CHECK_OUT_TIME = time(12, 0)


class BookingQuerySet(models.QuerySet):
    """Custom queryset for Booking model with soft-delete support."""

    def active(self):
        """Return bookings that are not deleted."""
        return self.filter(is_deleted=False)

    def deleted(self):
        """Return bookings that are marked as deleted."""
        return self.filter(is_deleted=True)

    def all_with_deleted(self):
        """Return all bookings including deleted ones."""
        return self.all()


class BookingManager(models.Manager):
    """Custom manager for Booking model using BookingQuerySet."""

    def get_queryset(self):
        """Return only active (not deleted) bookings by default."""
        return BookingQuerySet(self.model, using=self._db).active()

    def all_with_deleted(self):
        """Return all bookings including deleted ones."""
        return self.get_queryset().all_with_deleted()

    def deleted(self):
        """Return only deleted bookings."""
        return self.get_queryset().deleted()


class Booking(models.Model):
    """
        Represents a booking of a Listing by a tenant.

        Attributes:
            listing (Listing): Related listing being booked.
            tenant (User): Tenant who made the booking.
            start_date (date): Booking start date.
            end_date (date): Booking end date.
            parking_included (bool): Whether parking is included.
            status (str): Booking status (Pending, Confirmed, Cancelled, Rejected).
            total_price (Decimal): Total price for the booking, including parking.
            created_at (datetime): Timestamp of creation.
            updated_at (datetime): Timestamp of last update.
            is_deleted (bool): Soft-delete flag.
        """

    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='bookings'
    )

    start_date = models.DateField()
    end_date = models.DateField()
    parking_included = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=BookingStatusChoices.CHOICES,
        default=BookingStatusChoices.PENDING
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total booking price (including parking if selected)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = BookingManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        """Return a human-readable string representation of the booking."""
        parking_info = " + Parking" if self.parking_included else ""
        return (f"Booking #{self.id} — {self.listing.title} "
                f"[{self.start_date} → {self.end_date}] ({self.status}){parking_info}")

    @property
    def start_datetime(self):
        """
        Return the aware datetime of check-in.
        Check-in time is set to 14:00.
        """
        return make_aware(datetime.combine(self.start_date, CHECK_IN_TIME))

    @property
    def end_datetime(self):
        """
        Return the aware datetime of check-out.
        Check-out time is set to 12:00.
        """
        return make_aware(datetime.combine(self.end_date, CHECK_OUT_TIME))

    @property
    def duration_days(self):
        """
        Return the total number of days for the booking.
        Returns:
                int: Number of nights (end_date - start_date).
        """
        return (self.end_date - self.start_date).days

    def clean(self):
        """
        Validate the booking before saving.
        Raises:
                ValidationError: If dates are invalid or overlapping,
                or if the listing does not support daily rental.
        """
        validate_booking_dates(self.start_date, self.end_date, instance=self)

        if not self.listing.daily_enabled:
            raise ValidationError("This listing does not support daily rental.")

        overlapping_bookings = Booking.all_objects.filter(
            listing=self.listing,
            status__in=[BookingStatusChoices.PENDING, BookingStatusChoices.CONFIRMED],
            is_deleted=False
        ).exclude(id=self.id)

        for booking in overlapping_bookings:
            if booking.start_datetime < self.end_datetime and booking.end_datetime > self.start_datetime:
                raise ValidationError("The selected dates are already booked.")

    def calculate_total_price(self):
        """
        Calculate the total price for the booking including parking.
        Returns:
            Decimal: Total booking price.
        Raises:
            ValidationError: If the listing has invalid daily price.
        """
        listing = self.listing
        days_count = self.duration_days

        if not listing.price_per_day or listing.price_per_day <= 0:
            raise ValidationError("The listing has an invalid daily price.")

        total = listing.price_per_day * days_count

        if self.parking_included and listing.parking_price_per_day:
            total += listing.parking_price_per_day * days_count

        return total

    def save(self, *args, **kwargs):
        """
        Override save to validate, calculate total price, and enforce restrictions.
        Raises:
            ValidationError: If trying to modify dates on a confirmed booking.
        """
        if self.pk:
            original = Booking.all_objects.get(pk=self.pk)
            if original.status == BookingStatusChoices.CONFIRMED:
                if original.start_date != self.start_date or original.end_date != self.end_date:
                    raise ValidationError("Dates cannot be modified after the booking is confirmed.")
        self.clean()
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def can_cancel(self, hours_before=24):
        """
        Determine if the booking can be canceled.
        Args:
            hours_before (int): Minimum hours before check-in to allow cancellation.
        Returns:
            bool: True if cancellation is allowed, False otherwise.
        """
        cancel_deadline = self.start_datetime - timedelta(hours=hours_before)
        return now() < cancel_deadline

    def cancel(self):
        """
        Cancel the booking.
        Sets status to CANCELLED and removes parking.
        Raises:
            ValidationError: If cancellation is not allowed.
        """
        if not self.can_cancel():
            raise ValidationError("Cancellation is not possible less than 24 hours before check-in.")
        self.status = BookingStatusChoices.CANCELLED
        self.parking_included = False
        self.save()

    def confirm(self):
        """
        Confirm the booking.
        Raises:
            ValidationError: If booking is not in Pending status.
        """
        if self.status != BookingStatusChoices.PENDING:
            raise ValidationError("Only bookings with status 'Pending' can be confirmed.")
        self.status = BookingStatusChoices.CONFIRMED
        self.save()

    def delete(self, *args, **kwargs):
        """
        Soft-delete the booking.
        """
        self.is_deleted = True
        self.save()

    def restore(self):
        """
        Restore a soft-deleted booking.
        """
        if self.is_deleted:
            self.is_deleted = False
            self.save()
