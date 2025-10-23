from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.

    Features:
    - tenant_email: read-only field, retrieves email of the tenant.
    - Automatically sets the current authenticated user as the tenant when creating a review.
    - Validates rating to ensure it is between 1 and 5.

    Meta:
    - model: Review
    - fields: all relevant fields for API operations
    - read_only_fields: tenant and created_at (cannot be modified by client)
    """

    tenant_email = serializers.ReadOnlyField(source="tenant.email")

    class Meta:
        model = Review
        fields = [
            "id",
            "listing",
            "tenant",
            "tenant_email",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["tenant", "created_at"]

    def validate_rating(self, value):
        """
        Field-level validation for `rating`.

        Rules:
        - Rating must be an integer between 1 and 5 inclusive.
        - Raises serializers.ValidationError if the value is out of range.
        """
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        """
        Override create() to automatically assign the current user as tenant.

        Behavior:
        - Sets `tenant` to the current authenticated user from the request context.
        - Calls the parent create() method to save the instance.
        """
        validated_data["tenant"] = self.context["request"].user
        return super().create(validated_data)
