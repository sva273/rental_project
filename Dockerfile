FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# --- Собираем статические файлы при старте и запускаем Gunicorn ---
CMD python manage.py collectstatic --noinput && \
    python manage.py migrate && \
    gunicorn rental_project.wsgi:application --bind 0.0.0.0:8000
