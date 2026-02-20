from django.db import models
from apps.locations.models import Location


QUALITY_LABELS = [
    ("poor", "Poor"),
    ("fair", "Fair"),
    ("good", "Good"),
    ("great", "Great"),
    ("epic", "Epic"),
]


class SunsetForecast(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="forecasts")
    forecast_date = models.DateField()
    sunset_time_utc = models.DateTimeField()
    golden_hour_start_utc = models.DateTimeField()

    # Cloud layers (percentage 0–100)
    cloud_cover_total = models.FloatField()
    cloud_cover_low = models.FloatField()
    cloud_cover_mid = models.FloatField()
    cloud_cover_high = models.FloatField()

    # Atmospheric conditions
    relative_humidity = models.FloatField()
    precipitation_probability = models.FloatField()
    precipitation = models.FloatField()
    visibility = models.FloatField(null=True, blank=True)  # km
    wind_speed = models.FloatField(null=True, blank=True)  # km/h

    # Quality
    quality_score = models.FloatField()
    quality_label = models.CharField(max_length=10, choices=QUALITY_LABELS)

    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("location", "forecast_date")]
        ordering = ["-forecast_date"]

    def __str__(self):
        return f"{self.location} — {self.forecast_date} ({self.quality_label})"
