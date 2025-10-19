from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views.auth_view import AuthViewSet
from users.views.profile_view import ProfileViewSet

router = DefaultRouter()

# Регистрация и логин — через кастомный ViewSet
router.register(r'auth', AuthViewSet, basename='auth')

# Профиль пользователя (просмотр/редактирование своего профиля)
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
