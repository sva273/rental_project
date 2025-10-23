import pytest
from listings.models import Listing
from users.models import User
from reviews.models import Review


@pytest.mark.django_db
def test_listing_clean_valid_price():
    landlord = User.objects.create(email="landlord@example.com")
    listing = Listing(
        landlord=landlord,
        title="Test Listing",
        country="Germany",
        city="Berlin",
        street="Main",
        house_number="1",
        daily_enabled=True,
        price_per_day=100,
    )
    listing.clean()  # не должно выбросить ошибку


@pytest.mark.django_db
def test_listing_clean_invalid_price():
    landlord = User.objects.create(email="landlord@example.com")
    listing = Listing(
        landlord=landlord,
        title="Test Listing",
        country="Germany",
        city="Berlin",
        street="Main",
        house_number="1",
        daily_enabled=True,
        price_per_day=0,
    )
    with pytest.raises(Exception):
        listing.clean()


@pytest.mark.django_db
def test_listing_soft_delete():
    landlord = User.objects.create(email="landlord@example.com")
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
    listing.soft_delete()
    assert listing.is_deleted is True
    assert listing.is_active is False


@pytest.mark.django_db
def test_listing_toggle_active():
    landlord = User.objects.create(email="landlord@example.com")
    listing = Listing.objects.create(
        landlord=landlord,
        title="Test Listing",
        country="Germany",
        city="Berlin",
        street="Main",
        house_number="1",
        daily_enabled=True,
        price_per_day=100,
        is_active=True,
    )
    listing.toggle_active()
    assert listing.is_active is False
    listing.toggle_active()
    assert listing.is_active is True


@pytest.mark.django_db
def test_listing_full_address():
    landlord = User.objects.create(email="landlord@example.com")
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
    assert listing.full_address == "Main, 1, Berlin, Germany"


@pytest.mark.django_db
def test_listing_average_rating_and_count():
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
    Review.objects.create(
        listing=listing, tenant=tenant2, rating=5, comment="Excellent"
    )

    assert listing.reviews_count == 2
    assert listing.average_rating == 4.5
