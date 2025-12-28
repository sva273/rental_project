from django.contrib import admin, messages
from django.core.cache import cache
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for Review model:

    Features:
    - Displays main review fields in list view.
    - Supports filtering by rating, approval status, created date, and listing city.
    - Allows searching by listing title, tenant email/username, and comment content.
    - Read-only fields: created_at.
    - Supports bulk actions: approve reviews.
    """

    list_display = (
        "id",
        "listing",
        "tenant",
        "rating",
        "short_comment",
        "is_approved",
        "created_at",
    )

    list_filter = (
        "rating",
        "is_approved",
        "created_at",
        "listing__city",
    )

    search_fields = (
        "listing__title",
        "tenant__email",
        "tenant__username",
        "comment",
    )

    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 25

    fieldsets = (
        (
            "Main Information",
            {"fields": ("listing", "tenant", "rating", "is_approved")},
        ),
        ("Comment", {"fields": ("comment",)}),
        ("System Fields", {"fields": ("created_at",)}),
    )

    actions = ["approve_reviews"]

    def short_comment(self, obj):
        """
        Returns a short version of the comment for list display.
        If the comment is longer than 50 characters, it truncates and adds '...'.
        """
        return (obj.comment[:50] + "...") if len(obj.comment) > 50 else obj.comment

    short_comment.short_description = "Comment"

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        """
        Bulk action to approve reviews:
        - Iterates over selected reviews.
        - Only approves reviews that are currently not approved.
        - Updates a counter to show how many reviews were approved.
        - Clears cache for affected users and listings.
        """
        from django.core.cache import cache
        from listings.models import Listing
        
        updated = 0
        affected_tenants = set()
        affected_listings = set()
        affected_landlords = set()
        
        # Pre-fetch listings to get landlord IDs
        listing_ids = queryset.values_list('listing_id', flat=True).distinct()
        listings = {l.id: l for l in Listing.objects.filter(id__in=listing_ids).select_related('landlord')}
        
        for review in queryset:
            # Only approve if review is not already approved
            if not review.is_approved:
                review.is_approved = True
                review.save()
                updated += 1
                affected_tenants.add(review.tenant_id)
                affected_listings.add(review.listing_id)
                # Get landlord ID from pre-fetched listing
                listing = listings.get(review.listing_id)
                if listing and listing.landlord_id:
                    affected_landlords.add(listing.landlord_id)
        
        # Clear cache for all affected users and listings
        for tenant_id in affected_tenants:
            cache.delete(f"reviews_queryset_{tenant_id}")
        for landlord_id in affected_landlords:
            cache.delete(f"reviews_queryset_{landlord_id}")
        for listing_id in affected_listings:
            cache.delete(f"listing_{listing_id}")
        
        # Try to clear all reviews cache patterns (works with django-redis)
        try:
            if hasattr(cache, 'delete_pattern'):
                cache.delete_pattern("reviews_queryset_*")
        except (AttributeError, NotImplementedError):
            # Fallback: clear cache for all known users (limited approach for LocMemCache)
            pass
        
        self.message_user(request, f"{updated} review(s) approved.", messages.SUCCESS)
