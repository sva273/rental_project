# 🏡 Rental Project

A full-featured property rental platform built with Django and Django REST Framework. It supports user authentication,
property listings, bookings, reviews, analytics, and admin management — all designed for scalability and clarity.

---

## 📚 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

- 🔐 User authentication (TokenAuthentication) →(landlords and tenants)
- 🏠 Property listing management → Full CRUD operations, filtering, and pagination for property listings
- 📅 Booking system with status tracking → Booking statuses include: pending, confirmed, cancelled; 
- ⭐ Review and rating system → Tenants can leave reviews and ratings after completing a booking
- 📊 Analytics module → Provides insights into bookings, revenue, and property popularity
- 🛠 Admin panel with custom actions → Extended Django Admin functionality
- 📄 Swagger/OpenAPI documentation → Auto-generated using drf-yasg for clear and interactive API reference
- 📬 Email notifications via Django signals → Automated emails sent on booking creation, status updates, and new reviews

---

## 🛠 Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** MySQL (or SQLite for local dev)
- **Auth:** Token-based authentication ('rest_framework.authentication.TokenAuthentication')
- **Docs:** Swagger/OpenAPI (`drf-yasg`)
- **Admin:** Django Admin with custom actions
- **Testing:** Pytest / Django TestCase

---
```
## 🗂 Project Structure

rental_project/
├── manage.py                  # 🖥 Main command-line utility for managing the Django project (runserver, migrate, etc.)
├── requirements.txt           # 📦 List of Python packages required to run the project
├── README.md                  # 📘 Project overview, setup instructions, and usage documentation
├── swagger.yaml               # 📄 OpenAPI/Swagger specification for documenting the REST API
├── .gitignore                 # 🚫 Specifies files and folders to be ignored by Git version control

# ── Core Django Configuration ──
├── rental_project/            # ⚙️ Main Django project configuration package
│   ├── __init__.py            # 📌 Marks this directory as a Python package
│   ├── asgi.py                # 🌐 ASGI entry point for asynchronous server deployments
│   ├── settings.py            # ⚙️ Global Django settings (apps, middleware, database, etc.)
│   ├── urls.py                # 🌐 Root URL routing for the entire project
│   ├── wsgi.py                # 🌐 WSGI entry point for traditional server deployments
│   ├── choises.py             # 📋 Shared enums/constants used across multiple apps
│   └── migrations/            # 🗄 Project-level database migrations (if any)

# ── App: Analytics ──
├── analytics/                 # 📊 App for data analysis, metrics, and reporting
│   ├── __init__.py            # 📌 Package initializer
│   ├── admin.py               # 🛠 Admin panel configuration for analytics models
│   ├── apps.py                # ⚙️ App registration and configuration
│   ├── models.py              # 🧩 Database models for analytics
│   ├── permissions.py         # 🔐 Custom permission classes for analytics endpoints
│   ├── serializers.py         # 🔄 DRF serializers for transforming analytics data
│   ├── services.py            # ⚙️ Business logic and helper functions
│   ├── tests.py               # ✅ Unit and integration tests
│   ├── urls.py                # 🌐 API routing for analytics endpoints
│   ├── views.py               # 👁 API views and logic for analytics
│   └── migrations/            # 🗄 Database schema migrations

# ── App: Bookings ──
├── bookings/                  # 📅 App for managing property bookings and reservations
│   ├── __init__.py
│   ├── admin.py               # 🛠 Admin panel configuration for bookings
│   ├── apps.py
│   ├── choices.py             # 📋 Enum definitions for booking statuses and types
│   ├── models.py              # 🧩 Booking-related database models
│   ├── permissions.py         # 🔐 Access control for booking endpoints
│   ├── serializers.py         # 🔄 DRF serializers for booking data
│   ├── signals.py             # 📬 Signal handlers (e.g. email notifications on status change)
│   ├── config.py
│   ├── validators.py
│   ├── urls.py
│   ├── views.py
│   ├── tests/
│   └── migrations/

# ── App: Listings ──
├── listings/                  # 🏠 App for managing property listings
│   ├── __init__.py
│   ├── admin.py               # 🛠 Admin panel configuration for listings
│   ├── apps.py
│   ├── models.py              # 🧩 Listing-related database models
│   ├── permissions.py         # 🔐 Access control for listing endpoints
│   ├── serializers.py         # 🔄 DRF serializers for listing data
│   ├── signals.py             # 📬 Signal handlers (e.g. auto-updates or notifications)
│   ├── urls.py
│   ├── views.py
│   ├── migrations/
│   ├── tests/
│   └── choices/               # 📋 Field choices for listings
│       ├── __init__.py
│       ├── bathroom_type.py   # 🚿 Enum for bathroom types (e.g. shared, private)
│       └── property_type.py   # 🏠 Enum for property types (e.g. apartment, house)

# ── App: Reviews ──
├── reviews/                   # ⭐ App for user reviews and ratings
│   ├── __init__.py
│   ├── admin.py               # 🛠 Admin panel configuration for reviews
│   ├── apps.py
│   ├── models.py              # 🧩 Review-related database models
│   ├── permissions.py         # 🔐 Access control for review endpoints
│   ├── serializers.py         # 🔄 DRF serializers for review data
│   ├── signals.py             # 📬 Signal handlers (e.g. notify on approval)
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/

# ── App: Users ──
├── users/                     # 👤 App for user accounts, authentication, and profiles
│   ├── __init__.py
│   ├── admin.py               # 🛠 Admin panel configuration for users
│   ├── apps.py
│   ├── models.py              # 🧩 Custom user model with roles and permissions
│   ├── choises.py             # 📋 Enum definitions for user roles/statuses
│   ├── serializers.py         # 🔄 DRF serializers for user data
│   ├── signals.py             # 📬 Signal handlers (e.g. welcome emails)
│   ├── tests.py
│   ├── urls.py
│   ├── migrations/
│   ├── serializers/           # 🔄 Modular serializers for user-related features
│   │   ├── __init__.py
│   │   └── serializers.py
│   └── views/                 # 👁 Modular views for user operations
│       ├── __init__.py
│       ├── auth_view.py       # 🔐 Authentication logic (login, register, logout)
│       └── profile_view.py    # 👤 Profile management and user settings

# ── App: Web ──
├── web/                       # 🌐 App for frontend integration and static content
│   ├── __init__.py
│   ├── admin.py               # 🛠 Admin panel configuration for web content
│   ├── apps.py
│   ├── models.py              # 🧩 Models for static or marketing content
│   ├── tests.py
│   ├── urls.py
│   ├── views.py               # 👁 Views for rendering HTML templates
│   ├── migrations/
│   └── templates/             # 🖼 HTML templates for frontend pages
│       └── index.html         # 🏠 Main landing page template

# ── Core Utilities ──
├── __init__.py                # 📌 Root package initializer
└── pagination.py              # 📄 Shared pagination logic for API responses

# ── Utilities ──
└── utils/                     # 🧰 General-purpose helper scripts and tools
    ├── __init__.py
    └── generate_swagger_yaml # 🧪 Script to auto-generate Swagger/OpenAPI spec
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/rental_project.git
cd rental_project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit http://localhost:8000/admin to access the admin panel.

### 🔐 Environment Variables
Create a .env file in the root directory and define the following:
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@localhost:5432/dbname
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@example.com

### 📘 API Documentation
nteractive API docs are available at:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

You can also regenerate the OpenAPI schema using:
```bash
python utils/generate_swagger_yaml
```

### ✅ Running Tests

```bash
python manage.py test
```


---
## 🚢 Deployment
- To deploy in production:
- Set DEBUG=False
- Use gunicorn or uvicorn with wsgi.py or asgi.py
- Configure a production-ready database (e.g., PostgreSQL)
- Set up static/media file handling (e.g., with WhiteNoise or S3)
- Use a reverse proxy (e.g., Nginx)


---
## 🤝 Contributing
- Contributions are welcome! To contribute:
- Fork the repository
- Create a new branch: git checkout -b feature/your-feature-name
- Commit your changes: git commit -m 'Add new feature'
- Push to your branch: git push origin feature/your-feature-name
- Open a pull request
- 
---

## 📄 License
This project is licensed under the MIT License.