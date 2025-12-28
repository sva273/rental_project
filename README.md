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

- 🔐 **User Authentication** → Token-based authentication with role-based access control (Admin, Landlord, Tenant)
- 🏠 **Property Listing Management** → Full CRUD operations with advanced filtering, pagination, and image optimization
- 📅 **Booking System** → Complete booking workflow with status tracking (pending, confirmed, rejected, cancelled)
- ⭐ **Review & Rating System** → Tenants can leave reviews after completing stays, with admin approval workflow
- 📊 **Analytics Module** → Track user behavior, search history, and property views
- 🔔 **In-App Notifications** → Real-time notifications for bookings, reviews, and status changes
- 🛠 **Admin Panel** → Extended Django Admin with bulk actions and custom management tools
- 📄 **API Documentation** → Auto-generated Swagger/OpenAPI documentation using drf-yasg
- 📬 **Email Notifications** → Automated emails via Django signals for booking and review events
- ⚡ **Performance Optimizations** → Redis caching, image optimization, bulk operations, and query optimization
- 🎨 **Modern Frontend** → React + TypeScript + Vite with luxury UI design, animations, and responsive layout

---

## 🛠 Tech Stack

### Backend
- **Framework:** Django 5.x, Django REST Framework
- **Database:** MySQL (production) / SQLite (development)
- **Authentication:** Token-based authentication (DRF TokenAuthentication)
- **Caching:** Redis (production) / LocMemCache (development)
- **Image Processing:** Pillow for automatic image optimization
- **API Documentation:** drf-yasg (Swagger/OpenAPI)
- **Testing:** Pytest / Django TestCase

### Frontend
- **Framework:** React 18+ with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS with custom luxury theme
- **State Management:** Zustand
- **Data Fetching:** TanStack Query (React Query)
- **Routing:** React Router
- **Animations:** Framer Motion
- **HTTP Client:** Axios

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

# ── App: Core ──
├── core/                      # 🔧 Core utilities and shared functionality
│   ├── __init__.py            # 📌 Package initializer
│   ├── models.py              # 🧩 Notification model for in-app notifications
│   ├── serializers.py         # 🔄 Notification serializers
│   ├── views.py               # 👁 Notification API endpoints
│   ├── urls.py                # 🌐 Notification routes
│   ├── admin.py               # 🛠 Admin configuration for notifications
│   ├── pagination.py          # 📄 Shared pagination logic for API responses
│   └── email.py               # 📧 Centralized email sending utilities

# ── Frontend ──
├── frontend/                  # 🎨 React frontend application
│   ├── src/
│   │   ├── components/        # 🧩 React components
│   │   │   ├── layout/        # 📐 Layout components (Header, Footer, Layout)
│   │   │   ├── listings/      # 🏠 Listing-related components
│   │   │   ├── bookings/      # 📅 Booking components
│   │   │   ├── reviews/       # ⭐ Review components
│   │   │   ├── notifications/ # 🔔 Notification components
│   │   │   └── common/        # 🔧 Shared UI components
│   │   ├── pages/             # 📄 Page components (Home, Profile, Bookings, etc.)
│   │   ├── services/           # 🔌 API service layer
│   │   ├── store/             # 🗄 State management (Zustand)
│   │   └── types/             # 📝 TypeScript type definitions
│   ├── package.json           # 📦 Frontend dependencies
│   ├── vite.config.ts         # ⚙️ Vite configuration
│   ├── tailwind.config.js     # 🎨 Tailwind CSS configuration
│   └── tsconfig.json          # 📝 TypeScript configuration

# ── Utilities ──
└── utils/                     # 🧰 General-purpose helper scripts and tools
    ├── __init__.py
    ├── generate_swagger_yaml.py  # 🧪 Script to auto-generate Swagger/OpenAPI spec
    ├── seed_users.py          # 🌱 Database seeding scripts
    ├── seed_listings.py
    └── seed_booking.py
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

#### Install Python dependencies

```bash
pip install -r requirements.txt
```

#### Create environment file

```bash
cp ENV_EXAMPLE.txt .env
# Edit .env and set your SECRET_KEY_DJANGO
```

#### Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

**Note:** If you're adding the `core` app for the first time, make sure to run:
```bash
python manage.py makemigrations core
python manage.py migrate
```

#### Create a superuser

```bash
python manage.py createsuperuser
```

#### Run the development server

```bash
python manage.py runserver
```

Visit http://localhost:8000/admin to access the admin panel.

### 3. Frontend Setup

#### Navigate to frontend directory

```bash
cd frontend
```

#### Install dependencies

```bash
npm install
```

#### Configure API URL (Optional)

If your backend runs on a different port, update `frontend/src/services/api.ts`:
```typescript
baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'
```

Or set in `.env`:
```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

#### Run development server

```bash
npm run dev
```

Frontend will be available at http://localhost:5173 (Vite default port)

#### Build for production

```bash
npm run build
```

The built files will be in `frontend/dist/`

### 🔐 Environment Variables
Create a `.env` file in the root directory (copy from `ENV_EXAMPLE.txt`):

```bash
cp ENV_EXAMPLE.txt .env
```

Then edit `.env` and define the following:

**Required:**
```env
DEBUG=True
SECRET_KEY_DJANGO=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Database (SQLite by default):**
```env
MYSQL=False  # Set to True for MySQL
# If MYSQL=True, also set:
# DB_NAME=rental_db
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=3306
```

**Email:**
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@example.com
```

**Caching (Optional - for Redis):**
```env
USE_REDIS=False  # Set to True to use Redis
REDIS_URL=redis://127.0.0.1:6379/1
```

**Frontend (for CORS):**
```env
# VITE_API_URL=http://127.0.0.1:8000/api/v1
```

See `ENV_EXAMPLE.txt` for all available configuration options.

### 📘 API Documentation
Interactive API docs are available at:

- **Swagger UI:** http://localhost:8000/api/docs/swagger/
- **ReDoc:** http://localhost:8000/api/docs/redoc/

**Note:** All API endpoints require authentication by default (`IsAuthenticated`). Public endpoints (auth, swagger) have explicit permission overrides.

You can also regenerate the OpenAPI schema using:
```bash
python utils/generate_swagger_yaml.py
```

### ✅ Running Tests

Run all tests:
```bash
python manage.py test
```

Or use pytest:
```bash
pytest
```

Run tests for a specific app:
```bash
python manage.py test bookings
pytest bookings/tests/
```


---
## 🚢 Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure a production-ready database (PostgreSQL recommended)
3. Set up Redis for caching (recommended for production)
4. Use Gunicorn or Uvicorn with `wsgi.py` or `asgi.py`
5. Configure static/media file handling (WhiteNoise, S3, or CDN)
6. Set up a reverse proxy (Nginx)
7. Configure proper CORS settings for your frontend domain
8. Set secure `SECRET_KEY_DJANGO` and `ALLOWED_HOSTS`

### Frontend Deployment
1. Build the frontend: `npm run build`
2. Serve `dist/` folder with a web server (Nginx, Apache, or CDN)
3. Configure API URL to point to your backend
4. Set up proper routing (SPA fallback to `index.html`)

### Docker Deployment
Use the provided `Dockerfile` and `docker-compose.yml`:
```bash
docker-compose up -d
```


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
