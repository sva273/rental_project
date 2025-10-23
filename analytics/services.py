from django.db.models import F
from analytics.models import ViewHistory
from listings.models import Listing

MAX_HISTORY = 50


def record_listing_view(user, listing: Listing):
    """
    Records a user's view of a listing with proper analytics tracking.

    Steps:
        1. Checks the last listing viewed by the user.
        2. Creates a new ViewHistory entry if the listing is different from the last one.
        3. Increments the listing's `views_count` field using F expressions to avoid race conditions.
        4. Enforces a maximum history length per user, deleting the oldest entries if necessary.

    Args:
        user: The user who viewed the listing.
        listing (Listing): The listing being viewed.

    Notes:
        - This ensures repeated views of the same listing in a row are not double-counted.
        - Maintains a fixed-size history (MAX_HISTORY) per user.
    """
    # Retrieve the most recent view by this user
    last = ViewHistory.objects.filter(user=user).order_by("-viewed_at").first()

    # If no previous view exists or the last viewed listing is different from the current listing
    if not last or last.listing != listing:
        # Record a new view in the ViewHistory table
        ViewHistory.objects.create(user=user, listing=listing)

        # Increment the listing's views_count atomically
        listing.views_count = F("views_count") + 1
        listing.save(update_fields=["views_count"])

        # Calculate how many old entries exceed the MAX_HISTORY limit
        excess = ViewHistory.objects.filter(user=user).count() - MAX_HISTORY

        # Delete the oldest entries to maintain the history size limit
        if excess > 0:
            ViewHistory.objects.filter(user=user).order_by("viewed_at")[
                :excess
            ].delete()
