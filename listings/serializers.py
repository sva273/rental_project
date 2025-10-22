from django.db.models import Avg
from rest_framework import serializers
from listings.models import Listing


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Listing model.

    Provides read-only fields for computed properties:
    - landlord_email: Email of the listing owner
    - full_address: Concatenated address string
    - average_rating: Average rating of all reviews
    - reviews_count: Total number of reviews

    Validation:
    - Ensures that daily rental price is positive if daily renting is enabled.
    """

    landlord_email = serializers.ReadOnlyField(source='landlord.email')
    full_address = serializers.ReadOnlyField()
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            'id',
            'landlord',
            'landlord_email',
            'title',
            'description',
            'country',
            'city',
            'street',
            'house_number',
            'latitude',
            'longitude',
            'property_type',
            'rooms',
            'floor',
            'has_elevator',
            'has_terrace',
            'has_balcony',
            'bathroom_type',
            'has_internet',
            'has_parking',
            'daily_enabled',
            'price_per_day',
            'parking_price_per_day',
            'is_active',
            'main_image',
            'full_address',
            'average_rating',
            'reviews_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'landlord',
            'landlord_email',
            'is_active',
            'full_address',
            'average_rating',
            'reviews_count',
            'created_at',
            'updated_at',
        ]

    def get_average_rating(self, obj):
        """
        Returns the average rating for the listing.

        Calculation:
        - Aggregates the 'rating' field from related reviews.
        - Rounded to 2 decimal places.
        - Returns 0 if there are no reviews.
        """
        if hasattr(obj, 'average_rating_value'):
            return round(obj.average_rating_value or 0, 2)

        avg = obj.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 2) if avg else 0

    def get_reviews_count(self, obj):
        """
        Returns the total number of reviews for the listing.
        """
        return obj.reviews.count()

    def validate(self, data):
        """
        Ensures that if daily rental is enabled, a positive daily price is provided.

        Raises:
            serializers.ValidationError: If daily_enabled is True but price_per_day is missing or <= 0
        """
        daily_enabled = data.get('daily_enabled')
        price_per_day = data.get('price_per_day')

        if daily_enabled and (not price_per_day or price_per_day <= 0):
            raise serializers.ValidationError(
                "If daily rental is enabled, please provide a positive price per day."
            )
        return data


class ToggleActiveResponseSerializer(serializers.Serializer):
    """
    Serializer used to return the response of toggle_active endpoint.

    Fields:
    - is_active: Boolean indicating the new active state of the listing
    """
    is_active = serializers.BooleanField()
