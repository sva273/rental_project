from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Review
from core.models import Notification, NotificationType


@receiver(pre_save, sender=Review)
def cache_original_is_approved(sender, instance, **kwargs):
    """
    Cache original is_approved value before saving.
    This allows us to detect when is_approved changes.
    """
    if instance.pk:
        try:
            original = Review.objects.get(pk=instance.pk)
            instance._original_is_approved = original.is_approved
        except Review.DoesNotExist:
            instance._original_is_approved = False
    else:
        instance._original_is_approved = False


@receiver(post_save, sender=Review)
def clear_cache_on_review_change(sender, instance, created, **kwargs):
    """
    Clear cache when a review is created or when is_approved status changes.
    This ensures all users see updated review data.
    Also creates in-app notifications.
    """
    # Create notifications
    if created:
        # Notify landlord about new review
        Notification.objects.create(
            user=instance.listing.landlord,
            notification_type=NotificationType.REVIEW_CREATED,
            title="New Review",
            message=f'You have received a new review for "{instance.listing.title}" from {instance.tenant.email}',
            related_review=instance,
        )
    else:
        # Check if review was approved
        original_is_approved = getattr(instance, "_original_is_approved", False)
        if not original_is_approved and instance.is_approved:
            # Notify tenant that their review was approved
            Notification.objects.create(
                user=instance.tenant,
                notification_type=NotificationType.REVIEW_APPROVED,
                title="Review Approved",
                message=f'Your review for "{instance.listing.title}" has been approved and is now visible!',
                related_review=instance,
            )
    
    # Always clear cache for tenant
    cache.delete(f"reviews_queryset_{instance.tenant_id}")
    
    # Clear cache for landlord and listing
    if instance.listing_id:
        try:
            # Use select_related to avoid additional query if listing is already loaded
            listing = instance.listing
            if listing.landlord_id:
                cache.delete(f"reviews_queryset_{listing.landlord_id}")
        except Exception:
            # If listing is not loaded, fetch it
            try:
                from listings.models import Listing
                listing = Listing.objects.select_related('landlord').get(id=instance.listing_id)
                if listing.landlord_id:
                    cache.delete(f"reviews_queryset_{listing.landlord_id}")
            except Exception:
                pass
        
        # Clear cache for listing
        cache.delete(f"listing_{instance.listing_id}")
    
    # If is_approved status changed, clear all reviews cache patterns
    # This ensures all users see the updated review immediately
    if hasattr(instance, '_original_is_approved'):
        if instance._original_is_approved != instance.is_approved:
            # Try to clear all reviews cache patterns (works with django-redis)
            try:
                if hasattr(cache, 'delete_pattern'):
                    cache.delete_pattern("reviews_queryset_*")
            except (AttributeError, NotImplementedError):
                # Fallback for LocMemCache - cache will expire naturally
                pass
    elif created:
        # For new reviews, also try to clear all cache patterns
        try:
            if hasattr(cache, 'delete_pattern'):
                cache.delete_pattern("reviews_queryset_*")
        except (AttributeError, NotImplementedError):
            pass

