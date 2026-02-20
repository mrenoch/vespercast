from rest_framework import serializers
from .models import SunsetRating


class SunsetRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SunsetRating
        fields = ["id", "forecast", "score", "comment", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value
