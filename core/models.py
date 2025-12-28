from django.db import models
from django.conf import settings
from django.utils import timezone


class NotificationType(models.TextChoices):
    """Types of notifications."""
    BOOKING_CREATED = "booking_created", "New Booking"
    BOOKING_CONFIRMED = "booking_confirmed", "Booking Confirmed"
    BOOKING_REJECTED = "booking_rejected", "Booking Rejected"
    BOOKING_CANCELLED = "booking_cancelled", "Booking Cancelled"
    REVIEW_CREATED = "review_created", "New Review"
    REVIEW_APPROVED = "review_approved", "Review Approved"


class Notification(models.Model):
    """
    Model for storing in-app notifications.
    
    Fields:
        user: User who should receive the notification
        notification_type: Type of notification
        title: Notification title
        message: Notification message
        related_booking: Related booking (if applicable)
        related_review: Related review (if applicable)
        is_read: Whether the notification has been read
        created_at: Timestamp of creation
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_booking = models.ForeignKey(
        "bookings.Booking",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )
    related_review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email} ({'read' if self.is_read else 'unread'})"

    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.save(update_fields=["is_read"])

