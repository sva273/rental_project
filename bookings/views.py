from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError

from .models import Booking, BookingStatusChoices
from .serializers import BookingSerializer
from .permissions import IsAdminOrBookingParticipant


# --- Кастомный декоратор для извлечения и проверки объекта ---
def with_booking(func):
    def wrapper(self, request, pk=None, *args, **kwargs):
        booking = self.get_object()
        self.check_object_permissions(request, booking)
        return func(self, request, booking, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


class BookingViewSet(viewsets.ModelViewSet):
    """
    Управление бронированиями:
    - TENANT может создавать, отменять и просматривать свои бронирования.
    - LANDLORD может подтверждать и отклонять бронирования своих объектов.
    - ADMIN видит и управляет всеми бронированиями.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsAdminOrBookingParticipant]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Booking.objects.none()

        if user.is_staff or user.is_superuser:
            return Booking.objects.all()

        if user.groups.filter(name__iexact='LANDLORD').exists():
            return Booking.objects.filter(listing__landlord=user)

        # TENANT
        return Booking.objects.filter(tenant=user)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user, status=BookingStatusChoices.PENDING)

    # --- Swagger аннотации ---
    swagger_docs = {
        'list': swagger_auto_schema(
            operation_summary="Список бронирований",
            operation_description="Возвращает список бронирований в зависимости от роли пользователя",
            responses={200: openapi.Response(description="OK", schema=BookingSerializer(many=True))}
        ),
        'create': swagger_auto_schema(
            operation_summary="Создать бронирование",
            operation_description="TENANT создаёт новое бронирование. Статус — PENDING.",
            request_body=BookingSerializer,
            responses={201: openapi.Response(description="Создано", schema=BookingSerializer())}
        ),
        'retrieve': swagger_auto_schema(
            operation_summary="Получить бронирование",
            responses={200: openapi.Response(description="OK", schema=BookingSerializer())}
        ),
        'update': swagger_auto_schema(
            operation_summary="Обновить бронирование",
            request_body=BookingSerializer,
            responses={200: openapi.Response(description="Обновлено", schema=BookingSerializer())}
        ),
        'partial_update': swagger_auto_schema(
            operation_summary="Частично обновить бронирование",
            request_body=BookingSerializer,
            responses={200: openapi.Response(description="Обновлено", schema=BookingSerializer())}
        ),
        'destroy': swagger_auto_schema(
            operation_summary="Удалить бронирование",
            responses={204: openapi.Response(description="Удалено")}
        ),
        'cancel': swagger_auto_schema(
            operation_summary="Отменить бронирование",
            operation_description="TENANT может отменить своё бронирование, если до начала осталось более 24 часов.",
            responses={200: openapi.Response(description="Бронирование отменено")}
        ),
        'confirm': swagger_auto_schema(
            operation_summary="Подтвердить бронирование",
            operation_description="LANDLORD или ADMIN подтверждает бронирование. Статус → CONFIRMED.",
            responses={200: openapi.Response(description="Бронирование подтверждено")}
        ),
        'reject': swagger_auto_schema(
            operation_summary="Отклонить бронирование",
            operation_description="LANDLORD или ADMIN отклоняет бронирование. Статус → REJECTED.",
            responses={200: openapi.Response(description="Бронирование отклонено")}
        ),
    }

    # --- CRUD методы ---
    @swagger_docs['list']
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.user.groups.filter(name__iexact='LANDLORD').exists() and not request.user.is_staff:
            queryset = queryset.filter(listing__landlord=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_docs['create']
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_docs['retrieve']
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_docs['update']
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_docs['partial_update']
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_docs['destroy']
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # --- Кастомные действия ---
    @swagger_docs['cancel']
    @action(detail=True, methods=['post'])
    @with_booking
    def cancel(self, request, booking):
        try:
            booking.cancel()
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Бронирование успешно отменено.'})

    @swagger_docs['confirm']
    @action(detail=True, methods=['post'])
    @with_booking
    def confirm(self, request, booking):
        if booking.status != BookingStatusChoices.PENDING:
            return Response({'detail': 'Это бронирование уже обработано.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = BookingStatusChoices.CONFIRMED
        booking.save()
        return Response({'detail': 'Бронирование подтверждено.'})

    @swagger_docs['reject']
    @action(detail=True, methods=['post'])
    @with_booking
    def reject(self, request, booking):
        if booking.status != BookingStatusChoices.PENDING:
            return Response({'detail': 'Это бронирование уже обработано.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = BookingStatusChoices.REJECTED
        booking.save()
        return Response({'detail': 'Бронирование отклонено.'})
