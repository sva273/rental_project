from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Listing
from .config import notify_listing_created, notify_listing_updated


@receiver(post_save, sender=Listing)
def listing_created_or_updated(sender, instance, created, **kwargs):
    """
    Signal handler that triggers notifications when a Listing is created or updated.

    Args:
        sender: The model class (Listing)
        instance: The instance of Listing that was saved
        created (bool): True if a new instance was created
        **kwargs: Additional arguments passed by Django, e.g., 'update_fields'

    Behavior:
    - If a new Listing is created, sends a creation notification via `notify_listing_created`.
    - If an existing Listing is updated:
        - If only the 'views_count' field was updated, no notification is sent.
        - Otherwise, sends an update notification via `notify_listing_updated`.
    """
    update_fields = kwargs.get("update_fields")

    if created:
        notify_listing_created(instance)
    else:
        # If only the views_count field was updated, skip notification
        if update_fields is not None and update_fields == {"views_count"}:
            return
        notify_listing_updated(instance)
