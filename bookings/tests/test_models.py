import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from bookings.models import Booking
from listings.models import Listing
from users.models import User
from bookings.choices import BookingStatusChoices

# Create your tests here.

@pytest.fixture
def landlord():
    return User.objects.create(email='landlord@example.com')

@pytest.fixture
def tenant():
    return User.objects.create(email='tenant@example.com')

@pytest.fixture
def listing(landlord):
    return Listing.objects.create(
        landlord=landlord,
        title='Test Listing',
        country='Germany',
        city='Berlin',
        street='Main',
        house_number='1',
        daily_enabled=True,
        price_per_day=100,
        parking_price_per_day=20
    )

@pytest.mark.django_db
def test_booking_clean_valid(listing, tenant):
    booking = Booking(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2)
    )
    booking.clean()  # Should not raise

@pytest.mark.django_db
def test_booking_clean_invalid_overlap(listing, tenant):
    Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2),
        status=BookingStatusChoices.CONFIRMED
    )
    overlapping = Booking(
        listing=listing,
        tenant=tenant,
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=3)
    )
    with pytest.raises(ValidationError):
        overlapping.clean()

@pytest.mark.django_db
def test_total_price_with_parking(listing, tenant):
    booking = Booking(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2),
        parking_included=True
    )
    total = booking.calculate_total_price()
    assert total == (100 + 20) * 3

@pytest.mark.django_db
def test_total_price_without_parking(listing, tenant):
    booking = Booking(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2),
        parking_included=False
    )
    total = booking.calculate_total_price()
    assert total == 100 * 3

@pytest.mark.django_db
def test_confirm_booking(listing, tenant):
    booking = Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2)
    )
    booking.confirm()
    assert booking.status == BookingStatusChoices.CONFIRMED

@pytest.mark.django_db
def test_confirm_invalid_status(listing, tenant):
    booking = Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2),
        status=BookingStatusChoices.CANCELLED
    )
    with pytest.raises(ValidationError):
        booking.confirm()

@pytest.mark.django_db
def test_cancel_booking_success(listing, tenant):
    booking = Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today() + timedelta(days=2),
        end_date=date.today() + timedelta(days=3),
        parking_included=True
    )
    booking.cancel()
    assert booking.status == BookingStatusChoices.CANCELLED
    assert booking.parking_included is False

@pytest.mark.django_db
def test_cancel_booking_too_late(listing, tenant):
    booking = Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1)
    )
    with pytest.raises(ValidationError):
        booking.cancel()

@pytest.mark.django_db
def test_soft_delete_and_restore(listing, tenant):
    booking = Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2)
    )
    booking.delete()
    assert booking.is_deleted is True
    booking.restore()
    assert booking.is_deleted is False

@pytest.mark.django_db
def test_save_blocks_date_change_after_confirmation(listing, tenant):
    booking = Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=2),
        status=BookingStatusChoices.CONFIRMED
    )
    booking.start_date = date.today() + timedelta(days=1)
    with pytest.raises(ValidationError):
        booking.save()
