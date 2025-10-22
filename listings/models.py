from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.db.models import Avg

from listings.choices.property_type import PropertyTypeChoices
from listings.choices.bathroom_type import BathroomTypeChoices

# Create your models here.

class Listing(models.Model):
    """
    Represents a rental property posted by landlord.

    The Listing model stores detailed information about a property including:
    - Ownership (landlord reference)
    - Location and address details
    - Physical characteristics (rooms, floor, balcony, etc.)
    - Rental pricing (currently daily only)
    - Optional parking price
    - Visibility and soft delete control flags
    - View statistics (views_count)
    - Media previews (main image)
    - Creation and update timestamps

    Additional features:
    - Soft delete instead of hard delete
    - Custom validation through `clean()` before save
    - Computed properties for average rating and total number of reviews
    - Helper for full formatted address
    """

    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='listings',
        help_text="User who owns/published the listing"
    )

    title = models.CharField(max_length=255, help_text="Title of the listing")
    description = models.TextField(help_text="Detailed description of the property")

    # Address
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, db_index=True)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)

    # Geolocation (optional)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Property details
    property_type = models.CharField(
        max_length=50,
        choices=PropertyTypeChoices.CHOICES,
        default=PropertyTypeChoices.APARTMENT,
        help_text="Type of the property (e.g., Apartment, Studio, House)"
    )
    rooms = models.PositiveIntegerField(null=True, blank=True, help_text="Number of rooms")
    floor = models.PositiveIntegerField(null=True, blank=True, help_text="Floor number")
    has_elevator = models.BooleanField(default=False, help_text="Whether the building has an elevator")
    has_terrace = models.BooleanField(default=False, help_text="Whether the listing has a terrace")
    has_balcony = models.BooleanField(default=False, help_text="Whether the listing has a balcony")
    bathroom_type = models.CharField(
        max_length=20,
        choices=BathroomTypeChoices.CHOICES,
        default=BathroomTypeChoices.SHOWER,
        help_text="Type of bathroom (e.g., Shower or Bathtub)"
    )

    has_internet = models.BooleanField(default=False, help_text="Internet availability")
    has_parking = models.BooleanField(default=False, help_text="Parking availability")

    # Stats
    views_count = models.PositiveIntegerField(default=0, help_text="Number of views for this listing")

    # Rental price (daily only)
    daily_enabled = models.BooleanField(default=True, help_text="Whether daily renting is allowed")
    price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Price per day (must be positive if daily rental is enabled)"
    )

    # Optional parking pricing
    parking_price_per_day = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Daily price for parking (optional)"
    )

    # Status flags
    is_active = models.BooleanField(default=True, db_index=True, help_text="Visibility status of the listing")
    is_deleted = models.BooleanField(default=False, help_text="Soft delete flag")

    # Image + timestamps
    main_image = models.ImageField(upload_to='listing_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of creation")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp of last update")

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
        """
        Validates model constraints before saving.

        Business logic:
        - If `daily_enabled` is True, a positive `price_per_day` is required.
        - If daily renting is disabled, price is cleared automatically.
        """
        if self.daily_enabled:
            if not self.price_per_day or self.price_per_day <= 0:
                raise ValidationError("If daily rental is enabled, please specify a positive price per day.")
        else:
            self.price_per_day = None

    def save(self, *args, **kwargs):
        """
        Ensures validation is executed before saving the listing.
        """
        self.clean()
        super().save(*args, **kwargs)

    def soft_delete(self):
        """
        Performs a soft delete instead of removing the record from the database.

        Behavior:
        - Hides the listing by marking it as inactive.
        - Keeps the record for analytics / recovery purposes.
        """
        self.is_deleted = True
        self.is_active = False
        self.save()

    def toggle_active(self):
        """
        Toggles the active state of the listing and returns the new value.
        """
        self.is_active = not self.is_active
        self.save()
        return self.is_active

    @property
    def full_address(self):
        """
        Returns a human-readable formatted full address.
        """
        return f"{self.street}, {self.house_number}, {self.city}, {self.country}"

    @property
    def average_rating(self):
        """
        Returns the average rating for this listing, based on related reviews.
        Rounded to 2 decimals. Returns 0 if no reviews are present.
        """
        avg = self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 2) if avg else 0

    @property
    def reviews_count(self):
        """
        Returns the total number of reviews linked to this listing.
        """
        return self.reviews.count()

    def __str__(self):
        return f"{self.title} — {self.full_address}"
