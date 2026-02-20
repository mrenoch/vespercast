from django.contrib.gis.db import models


class Location(models.Model):
    """A geographic point with elevation and horizon metadata."""

    name = models.CharField(max_length=255, blank=True)
    point = models.PointField(geography=True, srid=4326)
    elevation = models.FloatField(null=True, blank=True)  # metres
    horizon_elevation_west = models.FloatField(default=0.0)  # degrees above flat
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["point"])]

    def __str__(self):
        return self.name or f"({self.point.y:.4f}, {self.point.x:.4f})"

    @property
    def lat(self):
        return self.point.y

    @property
    def lng(self):
        return self.point.x
