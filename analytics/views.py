from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count, F

from analytics.models import ViewHistory, SearchHistory
from analytics.serializers import ViewHistorySerializer, SearchHistorySerializer
from listings.models import Listing
from listings.serializers import ListingSerializer

MAX_HISTORY = 50  # максимальное количество записей истории на пользователя


class ViewHistoryViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewHistoryViewSet — управление историей просмотров объявлений пользователем.
    """

    serializer_class = ViewHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['viewed_at']
    search_fields = ['listing__title', 'listing__city']
    queryset = ViewHistory.objects.all()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ViewHistory.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return ViewHistory.objects.none()

        return ViewHistory.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Создаёт запись просмотра, если объявление отличается от последнего просмотренного.
        Также увеличивает счётчик просмотров и ограничивает историю до MAX_HISTORY.
        """
        listing = serializer.validated_data['listing']
        self.record_view(self.request.user, listing)

    @staticmethod
    def record_view(user, listing):
        """
        Статический метод для записи просмотра объявления:
        - Проверяет, отличается ли от последнего просмотренного.
        - Создаёт запись в ViewHistory.
        - Увеличивает views_count у объявления.
        - Удаляет старые записи, если превышен лимит MAX_HISTORY.
        """
        last = ViewHistory.objects.filter(user=user).order_by('-viewed_at').first()
        if not last or last.listing != listing:
            ViewHistory.objects.create(user=user, listing=listing)
            listing.views_count = F('views_count') + 1
            listing.save(update_fields=['views_count'])
            excess = ViewHistory.objects.filter(user=user).count() - MAX_HISTORY
            if excess > 0:
                ViewHistory.objects.filter(user=user).order_by('viewed_at')[:excess].delete()

    @swagger_auto_schema(
        operation_summary="Список просмотров",
        operation_description="Возвращает все просмотры текущего пользователя, можно фильтровать по дате",
        manual_parameters=[
            openapi.Parameter(
                'from_date', openapi.IN_QUERY,
                description="Фильтр: показать только просмотры после этой даты (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: openapi.Response(description="OK", schema=ViewHistorySerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        """
        Возвращает историю просмотров текущего пользователя.
        Поддерживает фильтрацию по дате через параметр from_date.
        """
        queryset = self.get_queryset()
        from_date = request.query_params.get('from_date')
        if from_date:
            queryset = queryset.filter(viewed_at__gte=from_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Популярные объявления",
        operation_description="Возвращает список объявлений, отсортированных по количеству просмотров",
        responses={200: openapi.Response(description="OK", schema=ListingSerializer(many=True))}
    )
    @action(detail=False, methods=['get'], url_path='popular')
    def popular_listings(self, request):
        """
        Возвращает топ-50 объявлений по количеству просмотров (views_count).
        """
        listings = Listing.objects.filter(is_deleted=False).order_by('-views_count')[:50]
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)


class SearchHistoryViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    """
    SearchHistoryViewSet — управление историей поисковых запросов пользователя.
    """

    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['searched_at']
    search_fields = ['keyword']
    queryset = SearchHistory.objects.all()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SearchHistory.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return SearchHistory.objects.none()

        return SearchHistory.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Создаёт запись поискового запроса, если он отличается от последнего.
        Ограничивает историю до MAX_HISTORY.
        """
        keyword = serializer.validated_data['keyword']
        last = SearchHistory.objects.filter(user=self.request.user).order_by('-searched_at').first()
        if not last or last.keyword != keyword:
            serializer.save(user=self.request.user)
            excess = SearchHistory.objects.filter(user=self.request.user).count() - MAX_HISTORY
            if excess > 0:
                SearchHistory.objects.filter(user=self.request.user).order_by('searched_at')[:excess].delete()

    @swagger_auto_schema(
        operation_summary="Список поисковых запросов",
        operation_description="Возвращает все поисковые запросы текущего пользователя, можно фильтровать по дате",
        manual_parameters=[
            openapi.Parameter(
                'from_date', openapi.IN_QUERY,
                description="Фильтр: показать только поисковые запросы после этой даты (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: openapi.Response(description="OK", schema=SearchHistorySerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        """
        Возвращает историю поисковых запросов текущего пользователя.
        Поддерживает фильтрацию по дате через параметр from_date.
        """
        queryset = self.get_queryset()
        from_date = request.query_params.get('from_date')
        if from_date:
            queryset = queryset.filter(searched_at__gte=from_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Популярные поисковые запросы",
        operation_description="Возвращает список ключевых слов, отсортированных по частоте использования",
        responses={200: openapi.Response(description="OK", examples={
            'application/json': [
                {'keyword': 'квартира в Берлине', 'count': 120},
                {'keyword': 'долгосрочная аренда', 'count': 110}
            ]
        })}
    )
    @action(detail=False, methods=['get'], url_path='popular')
    def popular_keywords(self, request):
        """
        Возвращает топ-50 популярных поисковых запросов по количеству повторений.
        """
        keywords = (
            SearchHistory.objects
            .values('keyword')
            .annotate(count=Count('id'))
            .order_by('-count')[:50]
        )
        return Response(keywords)
