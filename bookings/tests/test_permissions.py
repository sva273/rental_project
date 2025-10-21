import pytest
from datetime import date, timedelta
from rest_framework.test import APIRequestFactory
from bookings.permissions import IsAdminOrBookingParticipant
from bookings.models import Booking
from listings.models import Listing
from users.models import User
from django.contrib.auth.models import Group
from bookings.choices import BookingStatusChoices

factory = APIRequestFactory()

@pytest.fixture
def landlord():
    user = User.objects.create(email='landlord@example.com')
    Group.objects.get_or_create(name='LANDLORD')[0].user_set.add(user)
    return user

@pytest.fixture
def tenant():
    return User.objects.create(email='tenant@example.com')

@pytest.fixture
def other_tenant():
    return User.objects.create(email='other@example.com')

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
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=3),
        status=BookingStatusChoices.PENDING
    )

@pytest.mark.django_db
def test_admin_has_access(admin, booking):
    request = factory.get('/')
    request.user = admin
    permission = IsAdminOrBookingParticipant()
    view = type('View', (), {'action': 'retrieve'})()
    assert permission.has_object_permission(request, view=view, obj=booking)

@pytest.mark.django_db
def test_tenant_can_cancel_own_booking(tenant, booking):
    request = factory.post('/')
    request.user = tenant
    permission = IsAdminOrBookingParticipant()
    view = type('View', (), {'action': 'cancel'})()
    assert permission.has_object_permission(request, view=view, obj=booking)

@pytest.mark.django_db
def test_tenant_cannot_cancel_others_booking(other_tenant, booking):
    request = factory.post('/')
    request.user = other_tenant
    permission = IsAdminOrBookingParticipant()
    view = type('View', (), {'action': 'cancel'})()
    assert not permission.has_object_permission(request, view=view, obj=booking)

@pytest.mark.django_db
def test_landlord_can_confirm_own_listing_booking(landlord, booking):
    request = factory.post('/')
    request.user = landlord
    permission = IsAdminOrBookingParticipant()
    view = type('View', (), {'action': 'confirm'})()
    assert permission.has_object_permission(request, view=view, obj=booking)

@pytest.mark.django_db
def test_landlord_cannot_confirm_others_listing_booking(other_tenant, booking):
    request = factory.post('/')
    request.user = other_tenant
    permission = IsAdminOrBookingParticipant()
    view = type('View', (), {'action': 'confirm'})()
    assert not permission.has_object_permission(request, view=view, obj=booking)

@pytest.mark.django_db
def test_tenant_can_retrieve_own_booking(tenant, booking):
    request = factory.get('/')
    request.user = tenant
    permission = IsAdminOrBookingParticipant()
    view = type('View', (), {'action': 'retrieve'})()
    assert permission.has_object_permission(request, view=view, obj=booking)

@pytest.mark.django_db
def test_landlord_can_retrieve_booking_for_own_listing(landlord, booking):
    request = factory.get('/')
    request.user = landlord
    permission = IsAdminOrBookingParticipant()
    view = type('View', (), {'action': 'retrieve'})()
    assert permission.has_object_permission(request, view=view, obj=booking)

@pytest.mark.django_db
def test_tenant_cannot_retrieve_others_booking(other_tenant, booking):
    request = factory.get('/')
    request.user = other_tenant
    permission = IsAdminOrBookingParticipant()
    view = type('View', (), {'action': 'retrieve'})()
    assert not permission.has_object_permission(request, view=view, obj=booking)
