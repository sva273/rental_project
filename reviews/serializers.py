from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    tenant_email = serializers.ReadOnlyField(source='tenant.email')

    class Meta:
        model = Review
        fields = [
            'id',             # ID отзыва
            'listing',        # Объект, к которому относится отзыв
            'tenant',         # Автор отзыва (устанавливается автоматически)
            'tenant_email',   # Email автора (только для чтения)
            'rating',         # Оценка от 1 до 5
            'comment',        # Текст отзыва
            'created_at'      # Дата создания
        ]
        read_only_fields = ['tenant', 'created_at']

    def validate_rating(self, value):
        """
        Проверка: рейтинг должен быть в диапазоне от 1 до 5.
        """
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Рейтинг должен быть от 1 до 5.")
        return value

    def create(self, validated_data):
        """
        При создании отзыва автоматически устанавливается текущий пользователь как автор (tenant).
        """
        validated_data['tenant'] = self.context['request'].user
        return super().create(validated_data)
