from rest_framework import serializers
from bookings.models import Booking
from bookings.validators import validate_booking_dates

class BookingSerializer(serializers.ModelSerializer):
    tenant_email = serializers.ReadOnlyField(source='tenant.email')
    listing_title = serializers.ReadOnlyField(source='listing.title')
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'listing',
            'listing_title',
            'tenant',
            'tenant_email',
            'start_date',
            'end_date',
            'parking_included',
            'status',
            'total_price',
        ]
        read_only_fields = ['status', 'tenant', 'total_price']

    def validate(self, data):
        validate_booking_dates(
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            use_drf=True
        )
        return data
