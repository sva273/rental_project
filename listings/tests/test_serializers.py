import pytest
from listings.models import Listing
from listings.serializers import ListingSerializer
from users.models import User
from reviews.models import Review


@pytest.mark.django_db
def test_validate_positive_price_required():
    landlord = User.objects.create(email="landlord@example.com")
    data = {
        "title": "Test Listing",
        "description": "Nice place",
        "country": "Germany",
        "city": "Berlin",
        "street": "Main",
        "house_number": "1",
        "daily_enabled": True,
        "price_per_day": 0,
    }
    serializer = ListingSerializer(data=data)
    serializer.initial_data["landlord"] = landlord.id
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_validate_passes_with_valid_price():
    landlord = User.objects.create(email="landlord@example.com")
    data = {
        "title": "Test Listing",
        "description": "Nice place",
        "country": "Germany",
        "city": "Berlin",
        "street": "Main",
        "house_number": "1",
        "daily_enabled": True,
        "price_per_day": 100,
    }
    serializer = ListingSerializer(data=data)
    serializer.initial_data["landlord"] = landlord.id
    assert serializer.is_valid()


@pytest.mark.django_db
def test_average_rating_and_reviews_count():
    landlord = User.objects.create(email="landlord@example.com")
    tenant1 = User.objects.create(email="tenant1@example.com")
    tenant2 = User.objects.create(email="tenant2@example.com")
    listing = Listing.objects.create(
        landlord=landlord,
        title="Test Listing",
        country="Germany",
        city="Berlin",
        street="Main",
        house_number="1",
        daily_enabled=True,
        price_per_day=100,
    )
    Review.objects.create(listing=listing, tenant=tenant1, rating=4, comment="Good")
    Review.objects.create(listing=listing, tenant=tenant2, rating=5, comment="Great")

    serializer = ListingSerializer(instance=listing)
    assert serializer.data["average_rating"] == 4.5
    assert serializer.data["reviews_count"] == 2


@pytest.mark.django_db
def test_landlord_email_and_full_address():
    landlord = User.objects.create(email="landlord@example.com")
    listing = Listing.objects.create(
        landlord=landlord,
        title="Test Listing",
        description="Nice place",
        country="Germany",
        city="Berlin",
        street="Main",
        house_number="1",
        daily_enabled=True,
        price_per_day=100,
    )
    serializer = ListingSerializer(instance=listing)
    assert serializer.data["landlord_email"] == "landlord@example.com"
    assert serializer.data["full_address"] == "Main, 1, Berlin, Germany"
