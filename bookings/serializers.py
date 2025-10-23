from rest_framework import serializers
from bookings.models import Booking
from bookings.validators import validate_booking_dates


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.

    Provides read-only fields for tenant email, listing title, and total price.
    Validates booking dates using the custom `validate_booking_dates` function.
    """

    tenant_email = serializers.ReadOnlyField(source="tenant.email")
    listing_title = serializers.ReadOnlyField(source="listing.title")
    total_price = serializers.ReadOnlyField()

    class Meta:
        """
        Meta class for BookingSerializer.

        Attributes:
                model (Booking): The model being serialized.
                fields (list): List of fields included in the serialization.
                read_only_fields (list): Fields that cannot be updated via the API.
        """

        model = Booking
        fields = [
            "id",
            "listing",
            "listing_title",
            "tenant",
            "tenant_email",
            "start_date",
            "end_date",
            "parking_included",
            "status",
            "total_price",
        ]
        read_only_fields = ["status", "tenant", "total_price"]

    def validate(self, data):
        """
        Perform object-level validation.

        Ensures that start_date and end_date are valid according to business rules
        using `validate_booking_dates`.
        Args:
            data (dict): The input data dictionary containing booking fields.
        Raises:
            rest_framework.exceptions.ValidationError: If start_date or end_date
            violates validation rules (e.g., start date in the past, end before start, etc.)
        Returns:
            dict: Validated data.
        """
        validate_booking_dates(
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            use_drf=True,
        )
        return data
