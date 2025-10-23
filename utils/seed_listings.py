import os
import django
import random
import requests
from faker import Faker
from decimal import Decimal
from django.core.files import File
from io import BytesIO

# Инициализация Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rental_project.settings")
django.setup()

from django.contrib.auth import get_user_model
from listings.models import Listing
from listings.choices.property_type import PropertyTypeChoices
from listings.choices.bathroom_type import BathroomTypeChoices

fake = Faker("en_US")
User = get_user_model()

NUM_LISTINGS = 80  # количество объявлений
NUM_IMAGES = 50  # сколько фото загрузить с picsum.photos
MEDIA_PATH = os.path.join("media", "listing_images")


def download_images(num_images=NUM_IMAGES):
    """Скачивает случайные фото с picsum.photos и сохраняет в media/listing_images/"""
    os.makedirs(MEDIA_PATH, exist_ok=True)
    existing = len(
        [
            f
            for f in os.listdir(MEDIA_PATH)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
    )

    if existing >= num_images:
        print(f"Уже есть {existing} изображений, скачивание не требуется.")
        return

    print(f"Скачиваем {num_images} изображений с picsum.photos...")

    for i in range(1, num_images + 1):
        img_name = f"IMG_{i:03}.jpg"
        img_path = os.path.join(MEDIA_PATH, img_name)

        if os.path.exists(img_path):
            continue

        url = f"https://picsum.photos/800/600"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(img_path, "wb") as f:
                f.write(response.content)
            print(f" Saved: {img_name}")
        else:
            print(f" Не удалось загрузить {img_name}")

    print(" Все изображения скачаны и сохранены!")


def get_local_images():
    """Возвращает список путей к локальным изображениям в media/listing_images/"""
    images = sorted(
        [
            os.path.join(MEDIA_PATH, f)
            for f in os.listdir(MEDIA_PATH)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
    )
    return images


def create_fake_listings(num=NUM_LISTINGS):
    landlords = User.objects.filter(role="landlord")
    if not landlords.exists():
        print(" Нет арендодателей! Сначала создай пользователей через fake_users.py")
        return

    images = get_local_images()
    if not images:
        print(" Нет изображений в папке media/listing_images/.")
        return

    print(f" Найдено {len(images)} изображений. Используем по очереди для объявлений.")

    for i in range(num):
        landlord = random.choice(landlords)

        title = fake.catch_phrase()
        description = fake.paragraph(nb_sentences=5)
        country = "Germany"
        city = fake.city()
        street = fake.street_name()
        house_number = str(fake.building_number())

        latitude = round(random.uniform(45.0, 55.0), 6)
        longitude = round(random.uniform(10.0, 30.0), 6)

        property_type = random.choice(
            [choice[0] for choice in PropertyTypeChoices.CHOICES]
        )
        bathroom_type = random.choice(
            [choice[0] for choice in BathroomTypeChoices.CHOICES]
        )

        rooms = random.randint(1, 5)
        floor = random.randint(1, 15)
        has_elevator = random.choice([True, False])
        has_terrace = random.choice([True, False])
        has_balcony = random.choice([True, False])
        has_internet = random.choice([True, False])
        has_parking = random.choice([True, False])

        daily_enabled = True
        price_per_day = Decimal(random.uniform(30, 200)).quantize(Decimal("0.01"))
        parking_price_per_day = (
            Decimal(random.uniform(5, 20)).quantize(Decimal("0.01"))
            if has_parking
            else None
        )

        listing = Listing.objects.create(
            landlord=landlord,
            title=title,
            description=description,
            country=country,
            city=city,
            street=street,
            house_number=house_number,
            latitude=latitude,
            longitude=longitude,
            property_type=property_type,
            rooms=rooms,
            floor=floor,
            has_elevator=has_elevator,
            has_terrace=has_terrace,
            has_balcony=has_balcony,
            bathroom_type=bathroom_type,
            has_internet=has_internet,
            has_parking=has_parking,
            daily_enabled=daily_enabled,
            price_per_day=price_per_day,
            parking_price_per_day=parking_price_per_day,
            is_active=True,
            is_deleted=False,
        )

        # Назначаем изображение по порядку
        image_index = i % len(images)
        image_path = images[image_index]
        with open(image_path, "rb") as img_file:
            file_name = os.path.basename(image_path)
            listing.main_image.save(file_name, File(img_file), save=True)

        print(f" {i+1}/{num} — {listing.title} ({listing.city}) → {file_name}")

    print(f"\n Успешно создано {num} объявлений!")


if __name__ == "__main__":
    download_images()
    create_fake_listings()
