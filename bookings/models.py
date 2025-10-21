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
    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)

    def all_with_deleted(self):
        return self.all()


class BookingManager(models.Manager):
    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db).active()

    def all_with_deleted(self):
        return self.get_queryset().all_with_deleted()

    def deleted(self):
        return self.get_queryset().deleted()


class Booking(models.Model):
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
        parking_info = " + Parking" if self.parking_included else ""
        return (f"Booking #{self.id} — {self.listing.title} "
                f"[{self.start_date} → {self.end_date}] ({self.status}){parking_info}")

    @property
    def start_datetime(self):
        return make_aware(datetime.combine(self.start_date, CHECK_IN_TIME))

    @property
    def end_datetime(self):
        return make_aware(datetime.combine(self.end_date, CHECK_OUT_TIME))

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    def clean(self):
        validate_booking_dates(self.start_date, self.end_date)

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
        listing = self.listing
        days_count = self.duration_days

        if not listing.price_per_day or listing.price_per_day <= 0:
            raise ValidationError("The listing has an invalid daily price.")

        total = listing.price_per_day * days_count

        if self.parking_included and listing.parking_price_per_day:
            total += listing.parking_price_per_day * days_count

        return total

    def save(self, *args, **kwargs):
        if self.pk:
            original = Booking.all_objects.get(pk=self.pk)
            if original.status == BookingStatusChoices.CONFIRMED:
                if original.start_date != self.start_date or original.end_date != self.end_date:
                    raise ValidationError("Dates cannot be modified after the booking is confirmed.")
        self.clean()
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def can_cancel(self, hours_before=24):
        cancel_deadline = self.start_datetime - timedelta(hours=hours_before)
        return now() < cancel_deadline

    def cancel(self):
        if not self.can_cancel():
            raise ValidationError("Cancellation is not possible less than 24 hours before check-in.")
        self.status = BookingStatusChoices.CANCELLED
        self.parking_included = False
        self.save()

    def confirm(self):
        if self.status != BookingStatusChoices.PENDING:
            raise ValidationError("Only bookings with status 'Pending' can be confirmed.")
        self.status = BookingStatusChoices.CONFIRMED
        self.save()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def restore(self):
        if self.is_deleted:
            self.is_deleted = False
            self.save()
