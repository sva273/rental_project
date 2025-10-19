import os
import django
import random
from faker import Faker
from datetime import timedelta, date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from listings.models import Listing
from bookings.models import Booking
from bookings.choices import BookingStatusChoices

fake = Faker('en_US')
User = get_user_model()

NUM_BOOKINGS = 100  # сколько бронирований создать

def random_date(start, end):
    """Возвращает случайную дату между start и end"""
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def create_fake_bookings(num=NUM_BOOKINGS):
    tenants = User.objects.filter(role='tenant')
    listings = Listing.objects.filter(daily_enabled=True, is_active=True)

    if not tenants.exists() or not listings.exists():
        print(" Нет арендаторов или активных объявлений!")
        return

    for i in range(num):
        tenant = random.choice(tenants)
        listing = random.choice(listings)

        # Генерируем случайные даты бронирования
        start = random_date(date.today(), date.today() + timedelta(days=30))
        end = start + timedelta(days=random.randint(1, 7))

        parking_included = listing.has_parking and random.choice([True, False])

        booking = Booking(
            tenant=tenant,
            listing=listing,
            start_date=start,
            end_date=end,
            parking_included=parking_included,
            status=BookingStatusChoices.PENDING,
        )

        try:
            booking.save()
            print(f" Создано бронирование #{booking.id} для {tenant.email} ({listing.title})")
        except Exception as e:
            print(f" Не удалось создать бронирование: {e}")

if __name__ == "__main__":
    create_fake_bookings()
