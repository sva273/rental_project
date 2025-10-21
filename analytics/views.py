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

MAX_HISTORY = 50  # maximum number of history records per user


class ViewHistoryViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewHistoryViewSet — manages user's listing view history.
    """

    serializer_class = ViewHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['viewed_at']
    search_fields = ['listing__title', 'listing__city']
    queryset = ViewHistory.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return ViewHistory.objects.none()

        return ViewHistory.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Creates a new view history entry if the listing differs
        from the most recently viewed one. Also increments the
        listing view count and trims old records based on MAX_HISTORY.
        """
        listing = serializer.validated_data['listing']
        self.record_view(self.request.user, listing)

    @staticmethod
    def record_view(user, listing):
        """
        Records a listing view:
        - Checks if the listing differs from the last viewed one.
        - Creates a ViewHistory entry.
        - Increments the listing `views_count` value.
        - Deletes old entries if MAX_HISTORY is exceeded.
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
        operation_summary="List of listing views",
        operation_description="Returns all viewed listings of the current user, optionally filtered by date.",
        manual_parameters=[
            openapi.Parameter(
                'from_date', openapi.IN_QUERY,
                description="Filter: show only views after this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: openapi.Response(description="OK", schema=ViewHistorySerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        """
        Returns the view history of the current user.
        Supports filtering by `from_date` query parameter.
        """
        queryset = self.get_queryset()
        from_date = request.query_params.get('from_date')
        if from_date:
            queryset = queryset.filter(viewed_at__gte=from_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Popular listings",
        operation_description="Returns a list of listings sorted by view count.",
        responses={200: openapi.Response(description="OK", schema=ListingSerializer(many=True))}
    )
    @action(detail=False, methods=['get'], url_path='popular')
    def popular_listings(self, request):
        """
        Returns the top 50 listings by number of views (`views_count`).
        """
        listings = Listing.objects.filter(is_deleted=False).order_by('-views_count')[:50]
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)


class SearchHistoryViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    """
    SearchHistoryViewSet — manages user's search keyword history.
    """

    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['searched_at']
    search_fields = ['keyword']
    queryset = SearchHistory.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return SearchHistory.objects.none()

        return SearchHistory.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Saves a search query if it differs from the last one.
        Also trims old history entries based on MAX_HISTORY.
        """
        keyword = serializer.validated_data['keyword']
        last = SearchHistory.objects.filter(user=self.request.user).order_by('-searched_at').first()
        if not last or last.keyword != keyword:
            serializer.save(user=self.request.user)
            excess = SearchHistory.objects.filter(user=self.request.user).count() - MAX_HISTORY
            if excess > 0:
                SearchHistory.objects.filter(user=self.request.user).order_by('searched_at')[:excess].delete()

    @swagger_auto_schema(
        operation_summary="List of search queries",
        operation_description="Returns all search queries of the current user, optionally filtered by date.",
        manual_parameters=[
            openapi.Parameter(
                'from_date', openapi.IN_QUERY,
                description="Filter: show only searches after this date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={200: openapi.Response(description="OK", schema=SearchHistorySerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        """
        Returns the search history of the current user.
        Supports filtering by `from_date` query parameter.
        """
        queryset = self.get_queryset()
        from_date = request.query_params.get('from_date')
        if from_date:
            queryset = queryset.filter(searched_at__gte=from_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Popular search keywords",
        operation_description="Returns a list of the most frequent search keywords across all users.",
        responses={200: openapi.Response(description="OK", examples={
            'application/json': [
                {'keyword': 'apartment in Berlin', 'count': 120},
                {'keyword': 'long-term rent', 'count': 110}
            ]
        })}
    )
    @action(detail=False, methods=['get'], url_path='popular')
    def popular_keywords(self, request):
        """
        Returns the top 50 most used search keywords by frequency.
        """
        keywords = (
            SearchHistory.objects
            .values('keyword')
            .annotate(count=Count('id'))
            .order_by('-count')[:50]
        )
        return Response(keywords)
