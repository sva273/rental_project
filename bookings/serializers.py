from datetime import date
from rest_framework import serializers
from bookings.models import Booking

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
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError("Дата начала не может быть позже даты окончания.")
            if start_date == end_date:
                raise serializers.ValidationError("Бронирование должно быть минимум на 1 сутки.")
            if start_date < date.today():
                raise serializers.ValidationError("Дата начала не может быть в прошлом.")

            # Вычисляем максимально допустимую дату окончания (3 месяца от начала)
            month = start_date.month + 3
            year = start_date.year + (month - 1) // 12
            month = (month - 1) % 12 + 1
            try:
                max_end_date = start_date.replace(year=year, month=month)
            except ValueError:
                from calendar import monthrange
                day = min(start_date.day, monthrange(year, month)[1])
                max_end_date = start_date.replace(year=year, month=month, day=day)

            if end_date > max_end_date:
                raise serializers.ValidationError(
                    "Бронирование не может превышать 3 месяца. "
                    "Для более длительного срока свяжитесь с администрацией."
                )

        return data


