from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from listings.views import ListingViewSet
from bookings.views import BookingViewSet
from reviews.views import ReviewViewSet
from analytics.views import ViewHistoryViewSet, SearchHistoryViewSet
from users.views.auth_view import AuthViewSet
from users.views.profile_view import ProfileViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

from web.views import index

# Router
router = DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"reviews", ReviewViewSet, basename="review")
router.register(r"view-history", ViewHistoryViewSet, basename="view-history")
router.register(r"search-history", SearchHistoryViewSet, basename="search-history")
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"profile", ProfileViewSet, basename="profile")

# Swagger с TokenAuthentication
schema_view = get_schema_view(
    openapi.Info(
        title="Rental API",
        default_version="v1",
        description="API для управления сервисом аренды",
        contact=openapi.Contact(email="youremail@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly],
    authentication_classes=[],
)

# Основные маршруты
urlpatterns = [
    path("grappelli/", include("grappelli.urls")),
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("api/v1/", include(router.urls)),
    # Swagger / Redoc
    path(
        "api/docs/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/docs/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # Raw JSON/YAML
    re_path(
        r"^api/docs/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json-yaml",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
