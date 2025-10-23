from django.db import models
from django.conf import settings
from listings.models import Listing

# Create your models here.


class SearchHistory(models.Model):
    """
    Model representing a history of user search queries.

    Purpose:
        - Tracks keywords that users search for.
        - Supports analytics, personalization, and recommendation features.

    Fields:
        user (ForeignKey): The user who performed the search.
        keyword (CharField): The search query string.
        searched_at (DateTimeField): Timestamp when the search was performed.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="search_history",
    )
    keyword = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders the searches by most recent first
        ordering = ["-searched_at"]
        verbose_name = "Search History"
        verbose_name_plural = "Search Histories"

    def __str__(self):
        """
        Returns a readable string representation of the search history.
        """
        return f"{self.user.email} searched '{self.keyword}'"


class ViewHistory(models.Model):
    """
    Model representing a history of property views by users.

    Purpose:
        - Tracks which listings users view.
        - Supports analytics, popularity ranking, and recommendation features.
    Fields:
        user (ForeignKey): The user who viewed the listing.
        listing (ForeignKey): The listing that was viewed.
        viewed_at (DateTimeField): Timestamp when the listing was viewed.
    Constraints:
        unique_together: Ensures no duplicate entries for the same user, listing, and timestamp.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="view_history"
    )
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="views")
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Orders the views by most recent first
        ordering = ["-viewed_at"]
        verbose_name = "View History"
        verbose_name_plural = "View Histories"
        unique_together = (
            "user",
            "listing",
            "viewed_at",
        )  # prevents duplication within the same timestamp

    def __str__(self):
        """
        Returns a readable string representation of the view history.
        """
        return f"{self.user.email} viewed '{self.listing.title}'"
