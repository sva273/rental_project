from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from bookings.choices import BookingStatusChoices
from reviews.models import Review
from reviews.serializers import ReviewSerializer
from bookings.models import Booking
from reviews.permissions import IsAuthorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Управление отзывами:
    - TENANT может создавать и редактировать свои отзывы.
    - LANDLORD видит отзывы на свои объекты.
    - Администратор видит и может одобрять все отзывы.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Возвращает список отзывов в зависимости от роли пользователя:
        - Администратор видит все отзывы.
        - LANDLORD — только отзывы на свои объекты.
        - TENANT — только свои одобренные отзывы.
        """
        # Защита от генерации схемы Swagger
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()

        user = self.request.user
        if user.is_staff:
            return Review.objects.all()
        if user.groups.filter(name__iexact='LANDLORD').exists():
            return Review.objects.filter(listing__landlord=user, is_approved=True)
        return Review.objects.filter(tenant=user, is_approved=True)

    def perform_create(self, serializer):
        """
        Создаёт отзыв, если текущий пользователь — TENANT и у него было подтверждённое и завершённое бронирование.
        Отзыв создаётся неактивным (ожидает одобрения).
        """
        listing = serializer.validated_data['listing']
        user = self.request.user

        # Запретить создание отзыва для LANDLORD и STAFF
        if user.is_staff or user.groups.filter(name__iexact='LANDLORD').exists():
            raise ValidationError("Только арендатор может оставить отзыв.")

        # Проверка завершённого подтверждённого бронирования
        has_completed_booking = Booking.objects.filter(
            listing=listing,
            tenant=user,
            status=BookingStatusChoices.CONFIRMED,
            end_date__lt=timezone.now()
        ).exists()

        if not has_completed_booking:
            raise ValidationError("Вы можете оставить отзыв только после завершения проживания.")

        serializer.save(tenant=user, is_approved=False)

    @swagger_auto_schema(
        operation_summary="Список отзывов",
        operation_description="Возвращает отзывы в зависимости от роли: админ — все,"
                              " арендатор — свои, арендодатель — на свои объекты",
        responses={200: openapi.Response('Success', ReviewSerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        """Получить список отзывов с учётом роли пользователя."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать отзыв",
        operation_description="Создаёт отзыв после завершённого проживания",
        request_body=ReviewSerializer,
        responses={201: openapi.Response('Created', ReviewSerializer())}
    )
    def create(self, request, *args, **kwargs):
        """Создать новый отзыв (только после завершения бронирования)."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить отзыв",
        responses={200: openapi.Response('Success', ReviewSerializer())}
    )
    def retrieve(self, request, *args, **kwargs):
        """Получить конкретный отзыв по ID."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить отзыв",
        request_body=ReviewSerializer,
        responses={200: openapi.Response('Updated', ReviewSerializer())}
    )
    def update(self, request, *args, **kwargs):
        """Полностью обновить отзыв (только автор)."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить отзыв",
        request_body=ReviewSerializer,
        responses={200: openapi.Response('Updated', ReviewSerializer())}
    )
    def partial_update(self, request, *args, **kwargs):
        """Частично обновить отзыв (только автор)."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить отзыв",
        responses={204: openapi.Response('No Content')}
    )
    def destroy(self, request, *args, **kwargs):
        """Удалить отзыв (только автор)."""
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    @swagger_auto_schema(
        operation_summary="Одобрить отзыв",
        operation_description="Администратор может одобрить отзыв, чтобы он стал публичным",
        responses={200: openapi.Response('Review approved', ReviewSerializer())}
    )
    def approve(self, request, pk=None):
        """
        Одобряет отзыв (is_approved=True).
        Доступно только администратору.
        """
        review = self.get_object()
        review.is_approved = True
        review.save()
        serializer = self.get_serializer(review)
        return Response(serializer.data)
