from rest_framework import serializers
from .models import SunsetForecast
from apps.locations.serializers import LocationSerializer


class SunsetForecastSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = SunsetForecast
        fields = [
            "id",
            "location",
            "forecast_date",
            "sunset_time_utc",
            "golden_hour_start_utc",
            "cloud_cover_total",
            "cloud_cover_low",
            "cloud_cover_mid",
            "cloud_cover_high",
            "relative_humidity",
            "precipitation_probability",
            "precipitation",
            "visibility",
            "wind_speed",
            "quality_score",
            "quality_label",
            "fetched_at",
        ]
