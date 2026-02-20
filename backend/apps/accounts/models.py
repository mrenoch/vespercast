from django.db import models
from django.contrib.auth import get_user_model
from apps.locations.models import Location

User = get_user_model()


class UserLocation(models.Model):
    """A location saved to a user's profile."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_locations")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="saved_by")
    nickname = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "nickname"]
        unique_together = [("user", "location")]

    def __str__(self):
        return self.nickname or str(self.location)
