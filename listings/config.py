import django_filters
from core.email import safe_send_mail
from listings.models import Listing


def notify_listing_created(listing: Listing) -> None:
    """
    Sends email notification to the landlord when a new listing is created.
    """
    subject = f"New Listing Created: {listing.title}"
    message = (
        f'Your listing "{listing.title}" has been successfully published.\n\n'
        f"Thank you for using our platform!"
    )
    safe_send_mail(subject, message, [listing.landlord.email])


def notify_listing_updated(listing: Listing) -> None:
    """
    Sends email notification to the landlord when an existing listing is updated.
    """
    subject = f"Listing Updated: {listing.title}"
    message = f'Your listing "{listing.title}" has been updated.'
    safe_send_mail(subject, message, [listing.landlord.email])


class ListingFilter(django_filters.FilterSet):
    min_rooms = django_filters.NumberFilter(field_name="rooms", lookup_expr="gte")
    max_rooms = django_filters.NumberFilter(field_name="rooms", lookup_expr="lte")

    class Meta:
        model = Listing
        fields = ["property_type", "country", "city", "min_rooms", "max_rooms", "is_active"]
