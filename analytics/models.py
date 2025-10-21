from django.db import models
from django.conf import settings
from listings.models import Listing

# Create your models here.

class SearchHistory(models.Model):
    """
    History of user search queries.
    Used for analytics and personalization
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='search_history'
    )
    keyword = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']
        verbose_name = "Search History"
        verbose_name_plural = "Search Histories"

    def __str__(self):
        return f"{self.user.email} searched '{self.keyword}'"


class ViewHistory(models.Model):
    """
    History of property views by the user.
    Used for analytics and ranking by popularity
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='view_history'
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        related_name='views'
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        verbose_name = "View History"
        verbose_name_plural = "View Histories"
        unique_together = ('user', 'listing', 'viewed_at')  # prevents duplication within the same timestamp

    def __str__(self):
        return f"{self.user.email} viewed '{self.listing.title}'"
