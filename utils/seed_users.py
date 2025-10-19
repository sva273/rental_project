import os
import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

fake = Faker()

NUM_TENANTS = 40
NUM_LANDLORDS = 20

def create_users(num, role):
    for _ in range(num):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        username = fake.user_name()
        phone_number = fake.phone_number()[:15]  # максимум 15 символов
        password = '123456'  # тестовый пароль

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone_number=phone_number
        )
        print(f"✅ Created {role}: {user.email} ({user.first_name} {user.last_name})")

# Создаем арендаторов
create_users(NUM_TENANTS, 'tenant')

# Создаем арендодателей
create_users(NUM_LANDLORDS, 'landlord')

print("🎉 All users created successfully!")
