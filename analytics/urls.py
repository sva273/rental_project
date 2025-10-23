from django.urls import path, include
from rest_framework.routers import DefaultRouter
from analytics.views import ViewHistoryViewSet, SearchHistoryViewSet

router = DefaultRouter()
router.register(r"view-history", ViewHistoryViewSet, basename="view-history")
router.register(r"search-history", SearchHistoryViewSet, basename="search-history")

urlpatterns = [
    path("", include(router.urls)),
]
