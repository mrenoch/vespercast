import logging

from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Location
from .serializers import GeocodeRequestSerializer, GeocodeResponseSerializer, LocationSerializer
from .services.geocoding import geocode_address

logger = logging.getLogger(__name__)


class GeocodeView(APIView):
    """POST /api/v1/locations/geocode/ — address → lat/lng + elevation."""

    def post(self, request):
        req_ser = GeocodeRequestSerializer(data=request.data)
        req_ser.is_valid(raise_exception=True)

        result = geocode_address(req_ser.validated_data["address"])
        if result is None:
            return Response({"error": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

        resp_ser = GeocodeResponseSerializer(result.__dict__)
        return Response(resp_ser.data)


class LocationListCreateView(APIView):
    """POST /api/v1/locations/ — save a location."""

    def post(self, request):
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        name = request.data.get("name", "")
        elevation = request.data.get("elevation")
        horizon = request.data.get("horizon_elevation_west", 0.0)

        if lat is None or lng is None:
            return Response({"error": "lat and lng are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lat = float(lat)
            lng = float(lng)
        except (TypeError, ValueError):
            return Response({"error": "lat and lng must be numeric."}, status=status.HTTP_400_BAD_REQUEST)

        location, _ = Location.objects.get_or_create(
            point=Point(lng, lat, srid=4326),
            defaults={
                "name": name,
                "elevation": float(elevation) if elevation is not None else None,
                "horizon_elevation_west": float(horizon),
            },
        )
        return Response(LocationSerializer(location).data, status=status.HTTP_201_CREATED)
