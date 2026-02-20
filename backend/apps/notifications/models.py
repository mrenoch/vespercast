from django.db import models
from django.contrib.auth import get_user_model
from apps.locations.models import Location

User = get_user_model()


class NotificationPreference(models.Model):
    """Per-user, per-location alert preferences."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_prefs")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="notification_prefs")
    minimum_score_threshold = models.FloatField(default=60.0)
    notify_minutes_before = models.PositiveSmallIntegerField(default=60)
    notify_via_email = models.BooleanField(default=True)
    notify_via_push = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("user", "location")]

    def __str__(self):
        return f"{self.user} → {self.location} (≥{self.minimum_score_threshold})"


class Notification(models.Model):
    """A sent notification record."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]

    preference = models.ForeignKey(NotificationPreference, on_delete=models.CASCADE, related_name="notifications")
    forecast_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("preference", "forecast_date")]

    def __str__(self):
        return f"Notification for {self.preference} on {self.forecast_date}"
