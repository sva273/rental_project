from rest_framework import serializers
from .models import SearchHistory, ViewHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the SearchHistory model.

    Fields:
        user_email (ReadOnlyField): The email of the user who performed the search.
        id (IntegerField): The unique ID of the search record.
        user (PrimaryKeyRelatedField): The user who performed the search (read-only).
        keyword (CharField): The search query string.
        searched_at (DateTimeField): Timestamp when the search was performed (read-only).
    """

    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = SearchHistory
        fields = ["id", "user", "user_email", "keyword", "searched_at"]
        read_only_fields = ["user", "searched_at"]


class ViewHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ViewHistory model.

    Fields:
        user_email (ReadOnlyField): The email of the user who viewed the listing.
        listing_title (ReadOnlyField): The title of the viewed listing.
        id (IntegerField): The unique ID of the view record.
        user (PrimaryKeyRelatedField): The user who viewed the listing (read-only).
        listing (PrimaryKeyRelatedField): The listing that was viewed.
        viewed_at (DateTimeField): Timestamp when the listing was viewed (read-only).
    """

    user_email = serializers.ReadOnlyField(source="user.email")
    listing_title = serializers.ReadOnlyField(source="listing.title")

    class Meta:
        model = ViewHistory
        fields = ["id", "user", "user_email", "listing", "listing_title", "viewed_at"]
        read_only_fields = ["user", "viewed_at"]
