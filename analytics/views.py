from rest_framework import viewsets, mixins, filters, status
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
from rest_framework import serializers

MAX_HISTORY = 50  # maximum number of history records per user


# --- Serializer for popular keywords response ---
class PopularKeywordSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    count = serializers.IntegerField()


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
        listing = serializer.validated_data['listing']
        self.record_view(self.request.user, listing)

    @staticmethod
    def record_view(user, listing):
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
            openapi.Parameter('from_date', openapi.IN_QUERY,
                              description="Filter: show only views after this date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY,
                              description="Order by viewed_at", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY,
                              description="Search by listing title or city", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response(description="OK", schema=ViewHistorySerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        from_date = request.query_params.get('from_date')
        if from_date:
            queryset = queryset.filter(viewed_at__gte=from_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Add listing view",
        operation_description="Adds a new view history entry for the current user.",
        request_body=ViewHistorySerializer,
        responses={201: openapi.Response(description="Created", schema=ViewHistorySerializer())}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Popular listings",
        operation_description="Returns a list of listings sorted by view count.",
        responses={200: openapi.Response(description="OK", schema=ListingSerializer(many=True))}
    )
    @action(detail=False, methods=['get'], url_path='popular')
    def popular_listings(self, request):
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
            openapi.Parameter('from_date', openapi.IN_QUERY,
                              description="Filter: show only searches after this date (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY,
                              description="Order by searched_at", type=openapi.TYPE_STRING),
            openapi.Parameter('search', openapi.IN_QUERY,
                              description="Search by keyword", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response(description="OK", schema=SearchHistorySerializer(many=True))}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        from_date = request.query_params.get('from_date')
        if from_date:
            queryset = queryset.filter(searched_at__gte=from_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Add search query",
        operation_description="Adds a new search keyword to the user's history.",
        request_body=SearchHistorySerializer,
        responses={201: openapi.Response(description="Created", schema=SearchHistorySerializer())}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Popular search keywords",
        operation_description="Returns a list of the most frequent search keywords across all users.",
        responses={200: openapi.Response(description="OK", schema=PopularKeywordSerializer(many=True))}
    )
    @action(detail=False, methods=['get'], url_path='popular')
    def popular_keywords(self, request):
        keywords = (
            SearchHistory.objects
            .values('keyword')
            .annotate(count=Count('id'))
            .order_by('-count')[:50]
        )
        return Response(keywords)
