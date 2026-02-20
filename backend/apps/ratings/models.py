from django.db import models
from django.contrib.auth import get_user_model
from apps.forecasts.models import SunsetForecast

User = get_user_model()


class SunsetRating(models.Model):
    """User-submitted rating used as ML training data."""

    forecast = models.ForeignKey(SunsetForecast, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="ratings")
    score = models.PositiveSmallIntegerField()  # 1–5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rating {self.score}/5 for {self.forecast}"
