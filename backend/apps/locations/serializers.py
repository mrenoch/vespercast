from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(read_only=True)
    lng = serializers.FloatField(read_only=True)

    class Meta:
        model = Location
        fields = ["id", "name", "lat", "lng", "elevation", "horizon_elevation_west", "created_at"]
        read_only_fields = ["id", "created_at"]


class GeocodeRequestSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=500)


class GeocodeResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    elevation = serializers.FloatField(allow_null=True)
