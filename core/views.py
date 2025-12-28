from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing notifications.
    
    Permissions:
        - Users can only view their own notifications
    Features:
        - List and retrieve notifications
        - Mark notifications as read
        - Mark all notifications as read
    """
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only notifications for the current user."""
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        return Notification.objects.filter(user=self.request.user)
    
    @swagger_auto_schema(
        operation_summary="Mark notification as read and delete it",
        request_body=NotificationUpdateSerializer,
        responses={204: openapi.Response("No Content - notification deleted")},
    )
    @action(detail=True, methods=["patch"])
    def mark_read(self, request, pk=None):
        """Mark a notification as read and delete it."""
        notification = self.get_object()
        notification.delete()  # Delete the notification after marking as read
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @swagger_auto_schema(
        operation_summary="Mark all notifications as read and delete them",
        responses={200: openapi.Response("OK", {"detail": "All notifications deleted"})},
    )
    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        """Mark all notifications for the current user as read and delete them."""
        deleted_count, _ = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).delete()
        return Response({"detail": f"{deleted_count} notifications deleted"})
    
    @swagger_auto_schema(
        operation_summary="Get unread count",
        responses={200: openapi.Response("OK", {"unread_count": 0})},
    )
    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        """Get count of unread notifications."""
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        return Response({"unread_count": count})

