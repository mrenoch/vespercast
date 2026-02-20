from rest_framework import serializers
from .models import UserLocation
from apps.locations.serializers import LocationSerializer


class UserLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        source="location",
        queryset=__import__("apps.locations.models", fromlist=["Location"]).Location.objects.all(),
        write_only=True,
    )

    class Meta:
        model = UserLocation
        fields = ["id", "location", "location_id", "nickname", "is_primary", "created_at"]
        read_only_fields = ["id", "created_at"]
