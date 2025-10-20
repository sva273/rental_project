from django.db.models import Avg
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from listings.models import Listing
from listings.serializers import ListingSerializer
from listings.permissions import IsAdminOrLandlord

from analytics.services import record_listing_view

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ListingViewSet(viewsets.ModelViewSet):
    """
    Управление объявлениями аренды:
    - TENANT может только просматривать активные объявления.
    - LANDLORD и администратор могут создавать, редактировать, удалять и переключать активность.
    """
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated, IsAdminOrLandlord]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'city', 'country']
    ordering_fields = ['price_per_day', 'created_at', 'avg_rating']
    ordering = ['-created_at']
    filterset_fields = ['property_type', 'country', 'city', 'is_active']

    def get_queryset(self):
        # if getattr(self, 'swagger_fake_view', False):
        #     return Listing.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return Listing.objects.none()

        queryset = Listing.objects.filter(is_deleted=False)

        # Фильтрация по цене
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        try:
            if min_price:
                queryset = queryset.filter(price_per_day__gte=float(min_price))
            if max_price:
                queryset = queryset.filter(price_per_day__lte=float(max_price))
        except ValueError:
            pass

        # LANDLORD — только свои
        if user.groups.filter(name__iexact='LANDLORD').exists() and not user.is_staff:
            queryset = queryset.filter(landlord=user)
        # TENANT — только активные
        elif not user.is_staff:
            queryset = queryset.filter(is_active=True)

        # Аннотация рейтинга для всех
        return queryset.annotate(avg_rating=Avg('reviews__rating'))

    def get_ordering(self):
        ordering = self.request.query_params.get('ordering')
        if ordering:
            # Поддержка сортировки по average_rating → avg_rating
            if 'average_rating' in ordering:
                return [ordering.replace('average_rating', 'avg_rating')]
            return [ordering]
        return super().get_ordering()

    def perform_create(self, serializer):
        serializer.save(landlord=self.request.user)

    @swagger_auto_schema(
        operation_summary="Список объявлений",
        operation_description="""
        Возвращает список объявлений:
        - Администратор видит все объявления.
        - LANDLORD — только свои.
        - TENANT — только активные.
        """,
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Поиск по title, description, city, country", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Сортировка по price_per_day, created_at", type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Минимальная цена", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Максимальная цена", type=openapi.TYPE_NUMBER),
            openapi.Parameter('city', openapi.IN_QUERY, description="Город", type=openapi.TYPE_STRING),
            openapi.Parameter('country', openapi.IN_QUERY, description="Страна", type=openapi.TYPE_STRING),
            openapi.Parameter('property_type', openapi.IN_QUERY, description="Тип жилья", type=openapi.TYPE_STRING),
        ],
        responses={200: ListingSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать объявление",
        operation_description="Создаёт новое объявление. Доступно только LANDLORD и администратору.",
        responses={201: ListingSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Получить объявление",
        operation_description="Получает объявление по ID. TENANT видит только активные. Также фиксирует просмотр в истории.",
        responses={200: ListingSerializer, 403: "Нет доступа"}
    )
    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()
        user = request.user

        # Фиксация просмотра для TENANT
        if not user.is_staff and not user.groups.filter(name__iexact='LANDLORD').exists():
            record_listing_view(user, listing)

        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Обновить объявление",
        operation_description="Обновляет объявление. Только владелец или админ.",
        responses={200: ListingSerializer, 403: "Нет доступа"}
    )
    def update(self, request, *args, **kwargs):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удалить объявление",
        operation_description="Помечает объявление как удалённое (is_deleted=True). Только владелец или админ.",
        responses={204: "Удалено", 403: "Нет прав"}
    )
    def destroy(self, request, *args, **kwargs):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        listing.is_deleted = True
        listing.save()
        return Response({'detail': 'Объявление помечено как удалённое.'}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_summary="Переключить активность объявления",
        operation_description="Меняет статус активности объявления (is_active). Только владелец или админ.",
        responses={200: "OK", 403: "Нет прав"}
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrLandlord])
    def toggle_active(self, request, pk=None):
        listing = self.get_object()
        self.check_object_permissions(request, listing)
        listing.is_active = not listing.is_active
        listing.save()
        return Response({'is_active': listing.is_active})
