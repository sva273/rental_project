import pytest
from datetime import date, timedelta
from rest_framework.test import APIClient
from django.urls import reverse
from bookings.models import Booking, BookingStatusChoices
from listings.models import Listing
from users.models import User
from django.contrib.auth.models import Group

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def landlord():
    user = User.objects.create(email='landlord@example.com')
    Group.objects.get_or_create(name='LANDLORD')[0].user_set.add(user)
    return user

@pytest.fixture
def tenant():
    return User.objects.create(email='tenant@example.com')

@pytest.fixture
def admin():
    return User.objects.create(email='admin@example.com', is_staff=True)

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
        price_per_day=100
    )

@pytest.fixture
def booking(listing, tenant):
    return Booking.objects.create(
        listing=listing,
        tenant=tenant,
        start_date=date.today() + timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
        status=BookingStatusChoices.PENDING
    )

@pytest.mark.django_db
def test_tenant_can_create_booking(api_client, tenant, listing):
    api_client.force_authenticate(user=tenant)
    url = reverse('booking-list')
    data = {
        'listing': listing.id,
        'start_date': date.today() + timedelta(days=2),
        'end_date': date.today() + timedelta(days=4),
        'parking_included': True
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['status'] == BookingStatusChoices.PENDING

@pytest.mark.django_db
def test_admin_sees_all_bookings(api_client, admin, booking):
    api_client.force_authenticate(user=admin)
    url = reverse('booking-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['count'] >= 1

@pytest.mark.django_db
def test_tenant_can_cancel_own_booking(api_client, tenant, booking):
    api_client.force_authenticate(user=tenant)
    url = reverse('booking-cancel', args=[booking.id])
    response = api_client.post(url)
    assert response.status_code == 200
    booking.refresh_from_db()
    assert booking.status == BookingStatusChoices.CANCELLED

@pytest.mark.django_db
def test_landlord_can_confirm_booking(api_client, landlord, booking):
    api_client.force_authenticate(user=landlord)
    url = reverse('booking-confirm', args=[booking.id])
    response = api_client.post(url)
    assert response.status_code == 200
    booking.refresh_from_db()
    assert booking.status == BookingStatusChoices.CONFIRMED

@pytest.mark.django_db
def test_landlord_can_reject_booking(api_client, landlord, booking):
    api_client.force_authenticate(user=landlord)
    url = reverse('booking-reject', args=[booking.id])
    response = api_client.post(url)
    assert response.status_code == 200
    booking.refresh_from_db()
    assert booking.status == BookingStatusChoices.REJECTED
