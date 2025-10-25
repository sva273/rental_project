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
├── manage.py                  # 🖥 Django’s main CLI utility (runserver, migrations, etc.)
├── requirements.txt           # 📦 List of Python dependencies for the project
├── README.md                  # 📘 Project overview, setup instructions, and usage guide
├── swagger.yaml               # 📄 OpenAPI/Swagger specification for the REST API
├── .gitignore                 # 🚫 Specifies files/folders excluded from Git version control
├── logs/                      # 📁 Application log files (not tracked in Git)
├── docker-compose.yml         # 🐳 Docker Compose configuration (orchestrates web/db services)
├── Dockerfile                 # 🏗 Docker image build instructions for the Django app
├── pytest.ini                 # ✅ Configuration for pytest-based test suite                  

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
├── bookings/                  # 📅 Application for managing property bookings and reservations
│   ├── __init__.py
│   ├── admin.py               # 🛠 Django Admin panel configuration for booking models
│   ├── apps.py                # ⚙️ Application configuration class
│   ├── choices.py             # 📋 Enum-style constants for booking statuses and types
│   ├── models.py              # 🧩 Database models representing bookings and related entities
│   ├── permissions.py         # 🔐 Custom DRF permission classes for booking access control
│   ├── serializers.py         # 🔄 Serializers for converting booking models to/from JSON
│   ├── signals.py             # 📬 Logic triggered on model events (e.g. email after status change)
│   ├── config.py              # ⚙️ App-specific configuration and constants
│   ├── validators.py          # ✅ Business rule validators for booking creation/update
│   ├── urls.py                # 🌐 API routes/endpoints for bookings
│   ├── views.py               # 📥 Request handlers / DRF ViewSets for bookings API
│   ├── tests/                 # 🧪 Unit and integration tests for the app
│   └── migrations/            # 📜 Database schema migrations for bookings

# ── App: Listings ──
├── listings/                  # 🏠 Application for managing property listings
│   ├── __init__.py
│   ├── admin.py               # 🛠 Django Admin panel configuration for listing models
│   ├── apps.py                # ⚙️ Application configuration class
│   ├── models.py              # 🧩 Database models representing properties and related metadata
│   ├── permissions.py         # 🔐 Custom DRF permission classes controlling access to listings
│   ├── serializers.py         # 🔄 Converters between Listing models and REST API JSON responses
│   ├── signals.py             # 📬 Signal handlers (e.g., post-save automation or side effects)
│   ├── urls.py                # 🌐 API routes/endpoints for listings
│   ├── views.py               # 📥 API views and viewsets handling CRUD operations for listings
│   ├── migrations/            # 📜 Database schema changes for listings
│   ├── tests/                 # 🧪 Unit and integration tests for listing features
│   └── choices/               # 📋 Enum-style constants for field options used in listings
│       ├── __init__.py
│       ├── bathroom_type.py   # 🚿 Available bathroom types (shared/private)
│       └── property_type.py   # 🏢 Housing types (apartment, studio, house, etc.)

# ── App: Reviews ──
├── reviews/                   # ⭐ Application for user-generated property reviews and ratings
│   ├── __init__.py
│   ├── admin.py               # 🛠 Django Admin configuration for managing reviews
│   ├── apps.py               # ⚙️ Application configuration class
│   ├── models.py              # 🧩 ORM models representing reviews and rating metadata
│   ├── permissions.py         # 🔐 Custom permission classes controlling who can post/edit reviews
│   ├── serializers.py         # 🔄 Serializers converting review models to/from API responses
│   ├── signals.py             # 📬 Signal handlers (e.g., on review creation or moderation events)
│   ├── tests.py               # 🧪 Unit and integration tests for reviews functionality
│   ├── urls.py                # 🌐 API routes for creating, listing, and managing reviews
│   ├── views.py               # 📥 API endpoints and viewsets for review CRUD operations
│   └── migrations/            # 📜 Database schema migrations for the reviews app

# ── App: Users ──
├── users/                     # 👤 Application for managing user accounts, authentication, and profiles
│   ├── __init__.py
│   ├── admin.py               # 🛠 Django Admin configuration for custom user model
│   ├── apps.py               # ⚙️ Application configuration
│   ├── models.py              # 🧩 Custom user model with roles, permissions, and profile fields
│   ├── choices.py             # 📋 Enum-like constants for user roles and status types
│   ├── serializers.py         # 🔄 Core serializers for base user operations
│   ├── signals.py             # 📬 Signal handlers (e.g., welcome email on signup)
│   ├── tests.py               # 🧪 Tests for user authentication and profile logic
│   ├── urls.py                # 🌐 Public API routes for user endpoints
│   ├── migrations/            # 📜 Database schema migrations for user models
│   ├── serializers/           # 🔄 Modular serializers for advanced user-related logic
│   │   ├── __init__.py
│   │   └── serializers.py
│   └── views/                 # 👁 Modular viewsets and API endpoints
│       ├── __init__.py
│       ├── auth_view.py       # 🔐 Authentication: register, login, refresh, logout
│       └── profile_view.py    # 👤 Profile retrieval & editing

# ── App: Web ──
├── web/                       # 🌐 Application for frontend integration and rendering static pages
│   ├── __init__.py
│   ├── admin.py               # 🛠 Django Admin configuration for marketing/static content
│   ├── apps.py                # ⚙️ Application configuration
│   ├── models.py              # 🧩 Models for static pages, banners, landing content, etc.
│   ├── tests.py               # 🧪 Tests for frontend views or static content features
│   ├── urls.py                # 🌐 Public routes for landing pages
│   ├── views.py               # 👁 Views for rendering HTML templates
│   ├── migrations/            # 📜 Database schema changes for web models (if any)
│   └── templates/             # 🖼 HTML templates used by this app
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
interactive API docs are available at:

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

---

MIT License

Copyright (c) 2025 Wjatscheslaw Schwab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
