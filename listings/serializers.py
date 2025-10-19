from django.db.models import Avg
from rest_framework import serializers

from listings.models import Listing

class ListingSerializer(serializers.ModelSerializer):
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
            'is_deleted',
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
            'is_deleted',
            'full_address',
            'average_rating',
            'reviews_count',
            'created_at',
            'updated_at',
        ]

    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 2) if avg else 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def validate(self, data):
        daily_enabled = data.get('daily_enabled')
        price_per_day = data.get('price_per_day')

        if daily_enabled and (not price_per_day or price_per_day <= 0):
            raise serializers.ValidationError(
                "Если включена суточная аренда, укажите положительную цену за день."
            )
        return data
