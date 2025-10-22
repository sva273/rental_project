import pytest
from datetime import date, timedelta
from bookings.serializers import BookingSerializer
from bookings.models import Booking
from listings.models import Listing
from users.models import User

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
def test_serializer_valid_dates(listing, tenant):
    data = {
        'listing': listing.id,
        'tenant': tenant.id,
        'start_date': date.today() + timedelta(days=1),
        'end_date': date.today() + timedelta(days=3),
        'parking_included': True
    }
    serializer = BookingSerializer(data=data, context={'request': None})
    assert serializer.is_valid()

@pytest.mark.django_db
def test_serializer_invalid_dates(listing, tenant):
    data = {
        'listing': listing.id,
        'tenant': tenant.id,
        'start_date': date.today() - timedelta(days=1),
        'end_date': date.today() + timedelta(days=1),
        'parking_included': False
    }
    serializer = BookingSerializer(data=data, context={'request': None})
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors or 'start_date' in serializer.errors

@pytest.mark.django_db
def test_readonly_fields(listing, tenant):
    booking = Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=3),
        parking_included=True
    )
    serializer = BookingSerializer(instance=booking)
    data = serializer.data
    assert data['tenant_email'] == tenant.email
    assert data['listing_title'] == listing.title
    assert float(data['total_price']) == (100 + 20) * 2
