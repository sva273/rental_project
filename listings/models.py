from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.db.models import Avg

from listings.choices.property_type import PropertyTypeChoices
from listings.choices.bathroom_type import BathroomTypeChoices

# Create your models here.

class Listing(models.Model):
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='listings'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    # Адрес
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, db_index=True)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)

    # Геолокация (опционально)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Характеристики жилья
    property_type = models.CharField(
        max_length=50,
        choices=PropertyTypeChoices.CHOICES,
        default=PropertyTypeChoices.APARTMENT
    )
    rooms = models.PositiveIntegerField(null=True, blank=True)
    floor = models.PositiveIntegerField(null=True, blank=True)
    has_elevator = models.BooleanField(default=False)
    has_terrace = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    bathroom_type = models.CharField(
        max_length=20,
        choices=BathroomTypeChoices.CHOICES,
        default=BathroomTypeChoices.SHOWER
    )

    has_internet = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)

    views_count = models.PositiveIntegerField(default=0, help_text="Количество просмотров объявления")

    # Стоимость аренды (только суточная)
    daily_enabled = models.BooleanField(default=True)
    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Цена за сутки (минимум 1 день)"
    )

    # Стоимость парковки (опционально)
    parking_price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Цена за парковку в сутки (если платная)"
    )

    # Статусы
    is_active = models.BooleanField(default=True, db_index=True)
    is_deleted = models.BooleanField(default=False)

    # Фото и даты
    main_image = models.ImageField(upload_to='listing_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'listings'
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['price_per_day']),
            models.Index(fields=['city']),
            models.Index(fields=['is_active']),
        ]

    def clean(self):
        """Валидация логики объявления"""
        if self.daily_enabled:
            if not self.price_per_day or self.price_per_day <= 0:
                raise ValidationError("Если включена суточная аренда, укажите положительную цену за день.")
        else:
            self.price_per_day = None

    def save(self, *args, **kwargs):
        """Вызов clean() при каждом сохранении"""
        self.clean()
        super().save(*args, **kwargs)

    def soft_delete(self):
        """Мягкое удаление"""
        self.is_deleted = True
        self.is_active = False
        self.save()

    def toggle_active(self):
        """Активировать/деактивировать объявление"""
        self.is_active = not self.is_active
        self.save()
        return self.is_active

    @property
    def full_address(self):
        return f"{self.street}, {self.house_number}, {self.city}, {self.country}"

    def __str__(self):
        return f"{self.title} — {self.full_address}"

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 2) if avg else 0

    @property
    def reviews_count(self):
        return self.reviews.count()
