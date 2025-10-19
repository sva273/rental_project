from datetime import datetime, time, timedelta
from django.utils.timezone import now, make_aware
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from listings.models import Listing
from .choices import BookingStatusChoices

# Create your models here.

CHECK_IN_TIME = time(14, 0)   # Время заезда: 14:00
CHECK_OUT_TIME = time(12, 0)  # Время выезда: 12:00


class Booking(models.Model):
    """
    Модель бронирования жилья:
    - Связана с объектом Listing и пользователем (tenant).
    - Поддерживает посуточную аренду с учётом времени заезда/выезда.
    - Рассчитывает стоимость с учётом парковки.
    - Поддерживает soft delete и статусную логику.
    """

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
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
        help_text="Общая сумма бронирования (включая парковку, если есть)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        parking_info = " + Парковка" if self.parking_included else ""
        return (f"Бронь #{self.id} — {self.listing.title} "
                f"[{self.start_date} → {self.end_date}] ({self.status}){parking_info}")

    @property
    def start_datetime(self):
        """Дата и время заезда (14:00 в день начала)"""
        return make_aware(datetime.combine(self.start_date, CHECK_IN_TIME))

    @property
    def end_datetime(self):
        """Дата и время выезда (12:00 в день окончания)"""
        return make_aware(datetime.combine(self.end_date, CHECK_OUT_TIME))

    @property
    def duration_days(self):
        """Количество дней аренды (включая последний день)"""
        return (self.end_date - self.start_date).days + 1

    def clean(self):
        """
        Валидация:
        - Дата начала не может быть позже даты окончания.
        - Объект должен поддерживать суточную аренду.
        - Проверка пересечения с другими активными бронированиями с учётом времени.
        """
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Дата начала бронирования не может быть позже даты окончания.")

        if not self.listing.daily_enabled:
            raise ValidationError("Это объявление не поддерживает посуточную аренду.")

        active_bookings = Booking.objects.filter(
            listing=self.listing,
            status__in=[BookingStatusChoices.PENDING, BookingStatusChoices.CONFIRMED]
        ).exclude(id=self.id)

        for booking in active_bookings:
            if booking.start_datetime < self.end_datetime and booking.end_datetime > self.start_datetime:
                raise ValidationError("Это жильё уже забронировано на указанные даты/время.")

    def calculate_total_price(self):
        """
        Расчёт общей стоимости:
        - Учитывает цену за сутки.
        - Добавляет стоимость парковки, если включена.
        """
        listing = self.listing
        days_count = self.duration_days

        if not listing.price_per_day or listing.price_per_day <= 0:
            raise ValidationError("У объявления не указана корректная цена за сутки.")

        total = listing.price_per_day * days_count

        if self.parking_included and listing.parking_price_per_day:
            total += listing.parking_price_per_day * days_count

        return total

    def save(self, *args, **kwargs):
        """
        Сохранение:
        - Выполняет валидацию.
        - Пересчитывает `total_price` перед сохранением.
        """
        self.clean()
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def can_cancel(self, hours_before=24):
        """
        Проверка возможности отмены:
        - Отменить можно не позднее чем за `hours_before` часов до начала.
        """
        cancel_deadline = self.start_datetime - timedelta(hours=hours_before)
        return now() < cancel_deadline

    def cancel(self):
        """
        Отмена бронирования:
        - Проверяет возможность отмены.
        - Меняет статус на CANCELLED.
        - Убирает парковку.
        """
        if not self.can_cancel():
            raise ValidationError("Отмена невозможна менее чем за 24 часа до начала бронирования.")
        self.status = BookingStatusChoices.CANCELLED
        self.parking_included = False
        self.save()

    def confirm(self):
        """
        Подтверждение бронирования:
        - Доступно только для ожидающих заявок.
        """
        if self.status != BookingStatusChoices.PENDING:
            raise ValidationError("Можно подтвердить только ожидающее бронирование.")
        self.status = BookingStatusChoices.CONFIRMED
        self.save()

    def delete(self, *args, **kwargs):
        """
        Soft delete:
        - Не удаляет запись физически, только помечает как удалённую.
        """
        self.is_deleted = True
        self.save()
