from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from listings.models import Listing

# Create your models here.

class Review(models.Model):
    """
    Model representing a review left by a tenant for a listing.

    Fields:
    - listing: ForeignKey to the Listing being reviewed.
    - tenant: ForeignKey to the User who wrote the review.
    - rating: Integer between 1 and 5 representing the review score.
    - comment: Text content of the review.
    - created_at: Timestamp of review creation (auto-generated).
    - is_approved: Boolean indicating whether the review is approved by admin.

    Meta options:
    - Ordering: latest reviews first ('-created_at').
    - Constraints: a tenant can leave only one review per listing.
    """

    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating score between 1 and 5"
    )
    comment = models.TextField(help_text="Content of the review")
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval status")

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['listing', 'tenant'],
                name='unique_review_per_listing_tenant'
            )
        ]

    def __str__(self):
        """
        String representation of the review.
        Example: "Review 12 by tenant@example.com"
        """
        return f"Review {self.id} by {self.tenant.email}"

