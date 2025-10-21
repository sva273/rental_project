from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    tenant_email = serializers.ReadOnlyField(source='tenant.email')

    class Meta:
        model = Review
        fields = [
            'id',
            'listing',
            'tenant',
            'tenant_email',
            'rating',
            'comment',
            'created_at'
        ]
        read_only_fields = ['tenant', 'created_at']

    def validate_rating(self, value):
        """
        Validation: rating must be between 1 and 5.
        """
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        """
        Automatically set the current user as the review author (tenant) on creation.
        """
        validated_data['tenant'] = self.context['request'].user
        return super().create(validated_data)
