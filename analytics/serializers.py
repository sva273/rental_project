from rest_framework import serializers
from .models import SearchHistory, ViewHistory

class SearchHistorySerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'user_email', 'keyword', 'searched_at']
        read_only_fields = ['user', 'searched_at']

class ViewHistorySerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = ViewHistory
        fields = ['id', 'user', 'user_email', 'listing', 'listing_title', 'viewed_at']
        read_only_fields = ['user', 'viewed_at']
