from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    
    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "related_booking",
            "related_review",
            "is_read",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notification (mark as read)."""
    
    class Meta:
        model = Notification
        fields = ["is_read"]

