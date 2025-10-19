import os
import django
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rental_project.settings")
django.setup()

from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi
import yaml

# Генерация схемы
generator = OpenAPISchemaGenerator(
    info=openapi.Info(
        title="Rental API",
        default_version='v1',
        description="API для управления сервисом аренды",
        contact=openapi.Contact(email="youremail@example.com"),
    )
)
schema = generator.get_schema(request=None, public=True)

# Путь в корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
output_file = BASE_DIR / "swagger.yaml"

with open(output_file, "w", encoding="utf-8") as f:
    yaml.dump(schema, f, allow_unicode=True)

print(f"swagger.yaml создан в {output_file}")
