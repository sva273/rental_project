import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from listings.models import Listing
from users.models import User
from django.urls import reverse

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
        description='Nice place',
        country='Germany',
        city='Berlin',
        street='Main',
        house_number='1',
        daily_enabled=True,
        price_per_day=100,
        is_active=True
    )

@pytest.mark.django_db
def test_tenant_sees_only_active(api_client, tenant, listing):
    listing.is_active = False
    listing.save()
    api_client.force_authenticate(user=tenant)
    url = reverse('listing-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 0

@pytest.mark.django_db
def test_landlord_sees_only_own(api_client, landlord, listing):
    other_landlord = User.objects.create(email='other@example.com')
    Group.objects.get_or_create(name='LANDLORD')[0].user_set.add(other_landlord)
    Listing.objects.create(
        landlord=other_landlord,
        title='Other Listing',
        description='Other place',
        country='Germany',
        city='Berlin',
        street='Side',
        house_number='2',
        daily_enabled=True,
        price_per_day=80,
        is_active=True
    )
    api_client.force_authenticate(user=landlord)
    url = reverse('listing-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert all(item['landlord_email'] == landlord.email for item in response.data['results'])

@pytest.mark.django_db
def test_admin_sees_all(api_client, admin, listing):
    api_client.force_authenticate(user=admin)
    url = reverse('listing-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['count'] >= 1

@pytest.mark.django_db
def test_create_listing(api_client, landlord):
    api_client.force_authenticate(user=landlord)
    url = reverse('listing-list')
    data = {
        'title': 'New Listing',
        'description': 'Nice place',
        'country': 'Germany',
        'city': 'Berlin',
        'street': 'Main',
        'house_number': '1',
        'daily_enabled': True,
        'price_per_day': 120
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['title'] == 'New Listing'
    assert response.data['landlord_email'] == landlord.email

@pytest.mark.django_db
def test_toggle_active(api_client, landlord, listing):
    api_client.force_authenticate(user=landlord)
    url = reverse('listing-toggle-active', args=[listing.id])
    original_status = listing.is_active
    response = api_client.post(url)
    assert response.status_code == 200
    listing.refresh_from_db()
    assert listing.is_active != original_status
    assert response.data['is_active'] == listing.is_active

@pytest.mark.django_db
def test_filter_by_price(api_client, admin):
    Listing.objects.create(
        landlord=admin,
        title='Cheap Listing',
        description='Budget stay',
        country='Germany',
        city='Berlin',
        street='Cheap',
        house_number='3',
        daily_enabled=True,
        price_per_day=50,
        is_active=True
    )
    api_client.force_authenticate(user=admin)
    url = reverse('listing-list') + '?min_price=60'
    response = api_client.get(url)
    assert response.status_code == 200
    assert all(item['price_per_day'] >= 60 for item in response.data['results'])
