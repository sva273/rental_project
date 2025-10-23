import pytest
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import Group
from listings.models import Listing
from users.models import User
from listings.permissions import IsAdminOrLandlord

factory = APIRequestFactory()


@pytest.mark.django_db
def test_safe_method_allowed_for_authenticated_user():
    user = User.objects.create(email="tenant@example.com")
    request = factory.get("/listings/")
    request.user = user
    permission = IsAdminOrLandlord()
    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_unsafe_method_denied_for_tenant():
    user = User.objects.create(email="tenant@example.com")
    request = factory.post("/listings/")
    request.user = user
    permission = IsAdminOrLandlord()
    assert permission.has_permission(request, None) is False


@pytest.mark.django_db
def test_unsafe_method_allowed_for_admin():
    user = User.objects.create(email="admin@example.com", is_staff=True)
    request = factory.post("/listings/")
    request.user = user
    permission = IsAdminOrLandlord()
    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_unsafe_method_allowed_for_landlord():
    user = User.objects.create(email="landlord@example.com")
    Group.objects.create(name="LANDLORD").user_set.add(user)
    request = factory.post("/listings/")
    request.user = user
    permission = IsAdminOrLandlord()
    assert permission.has_permission(request, None) is True


@pytest.mark.django_db
def test_object_permission_for_admin():
    admin = User.objects.create(email="admin@example.com", is_staff=True)
    listing = Listing.objects.create(
        landlord=User.objects.create(email="landlord@example.com"),
        title="Test Listing",
        country="Germany",
        city="Berlin",
        street="Main",
        house_number="1",
        daily_enabled=True,
        price_per_day=100,
    )
    request = factory.delete("/listings/")
    request.user = admin
    permission = IsAdminOrLandlord()
    assert permission.has_object_permission(request, None, listing) is True


@pytest.mark.django_db
def test_object_permission_for_landlord_owner():
    landlord = User.objects.create(email="landlord@example.com")
    Group.objects.create(name="LANDLORD").user_set.add(landlord)
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
    request = factory.put("/listings/")
    request.user = landlord
    permission = IsAdminOrLandlord()
    assert permission.has_object_permission(request, None, listing) is True


@pytest.mark.django_db
def test_object_permission_for_landlord_not_owner():
    landlord = User.objects.create(email="landlord@example.com")
    other_landlord = User.objects.create(email="other@example.com")
    Group.objects.create(name="LANDLORD").user_set.add(other_landlord)
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
    request = factory.put("/listings/")
    request.user = other_landlord
    permission = IsAdminOrLandlord()
    assert permission.has_object_permission(request, None, listing) is False


@pytest.mark.django_db
def test_object_permission_for_tenant_safe_method():
    tenant = User.objects.create(email="tenant@example.com")
    listing = Listing.objects.create(
        landlord=User.objects.create(email="landlord@example.com"),
        title="Test Listing",
        country="Germany",
        city="Berlin",
        street="Main",
        house_number="1",
        daily_enabled=True,
        price_per_day=100,
    )
    request = factory.get("/listings/")
    request.user = tenant
    permission = IsAdminOrLandlord()
    assert permission.has_object_permission(request, None, listing) is True


@pytest.mark.django_db
def test_object_permission_for_tenant_unsafe_method():
    tenant = User.objects.create(email="tenant@example.com")
    listing = Listing.objects.create(
        landlord=User.objects.create(email="landlord@example.com"),
        title="Test Listing",
        country="Germany",
        city="Berlin",
        street="Main",
        house_number="1",
        daily_enabled=True,
        price_per_day=100,
    )
    request = factory.delete("/listings/")
    request.user = tenant
    permission = IsAdminOrLandlord()
    assert permission.has_object_permission(request, None, listing) is False
