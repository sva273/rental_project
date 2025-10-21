from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from listings.models import Listing

# Create your models here.

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name='reviews')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['listing', 'tenant'], name='unique_review_per_listing_tenant')
        ]

    def __str__(self):
        return f"Review {self.id} by {self.tenant.email}"
