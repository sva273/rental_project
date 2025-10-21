from django.db.models import F
from analytics.models import ViewHistory
from listings.models import Listing

MAX_HISTORY = 50

def record_listing_view(user, listing: Listing):
    """
    Records a listing view by a user:
    - Checks whether it differs from the last viewed listing.
    - Creates a new ViewHistory record.
    - Increments the listing `views_count` field.
    - Removes the oldest records if the limit is exceeded.
    """
    last = ViewHistory.objects.filter(user=user).order_by('-viewed_at').first()
    if not last or last.listing != listing:
        ViewHistory.objects.create(user=user, listing=listing)
        listing.views_count = F('views_count') + 1
        listing.save(update_fields=['views_count'])
        excess = ViewHistory.objects.filter(user=user).count() - MAX_HISTORY
        if excess > 0:
            ViewHistory.objects.filter(user=user).order_by('viewed_at')[:excess].delete()
