import logging
from datetime import date, datetime, timezone

from django.conf import settings
from django.contrib.gis.geos import Point
from django.utils import timezone as django_tz
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.locations.models import Location
from .models import SunsetForecast
from .serializers import SunsetForecastSerializer
from .services.astro import get_sun_times, estimate_timezone
from .services.open_meteo import get_weather_at_sunset
from .services.scorer import compute_quality_score

logger = logging.getLogger(__name__)

CACHE_HOURS = getattr(settings, "FORECAST_CACHE_HOURS", 3)


class ForecastView(APIView):
    """
    GET /api/v1/forecasts/?lat=&lng=&date=YYYY-MM-DD

    Returns a SunsetForecast, fetching from Open-Meteo if the cached
    version is older than FORECAST_CACHE_HOURS.
    """

    def get(self, request):
        lat_str = request.query_params.get("lat")
        lng_str = request.query_params.get("lng")
        date_str = request.query_params.get("date")

        if not lat_str or not lng_str:
            return Response({"error": "lat and lng are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lat = float(lat_str)
            lng = float(lng_str)
        except ValueError:
            return Response({"error": "lat and lng must be numeric."}, status=status.HTTP_400_BAD_REQUEST)

        if date_str:
            try:
                target_date = date.fromisoformat(date_str)
            except ValueError:
                return Response({"error": "date must be YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            target_date = date.today()

        # Get or create location
        point = Point(lng, lat, srid=4326)
        location, _ = Location.objects.get_or_create(point=point)

        # Check cache
        forecast = _get_cached_forecast(location, target_date)
        if forecast:
            return Response(SunsetForecastSerializer(forecast).data)

        # Fetch fresh forecast
        forecast = _build_forecast(location, target_date)
        if forecast is None:
            return Response(
                {"error": "Could not compute forecast. Sun may not set at this location/date."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(SunsetForecastSerializer(forecast).data)


def _get_cached_forecast(location: Location, target_date: date) -> SunsetForecast | None:
    """Return a cached forecast if it exists and was fetched within CACHE_HOURS."""
    try:
        forecast = SunsetForecast.objects.get(location=location, forecast_date=target_date)
    except SunsetForecast.DoesNotExist:
        return None

    age_hours = (django_tz.now() - forecast.fetched_at).total_seconds() / 3600
    if age_hours <= CACHE_HOURS:
        return forecast

    # Stale — delete and re-fetch
    forecast.delete()
    return None


def _build_forecast(location: Location, target_date: date) -> SunsetForecast | None:
    """Fetch weather + astro data and compute quality score, saving to DB."""
    tz_name = estimate_timezone(location.lng)

    sun_times = get_sun_times(location.lat, location.lng, target_date, tz_name)
    if sun_times is None:
        return None

    weather = get_weather_at_sunset(
        location.lat,
        location.lng,
        target_date,
        sun_times.sunset_hour_local,
        tz_name,
    )
    if weather is None:
        return None

    breakdown = compute_quality_score(
        cloud_low=weather.cloud_cover_low,
        cloud_mid=weather.cloud_cover_mid,
        cloud_high=weather.cloud_cover_high,
        precipitation=weather.precipitation,
        precipitation_probability=weather.precipitation_probability,
        relative_humidity=weather.relative_humidity,
        visibility=weather.visibility,
        wind_speed=weather.wind_speed,
        horizon_elevation_west=location.horizon_elevation_west,
    )

    forecast = SunsetForecast.objects.create(
        location=location,
        forecast_date=target_date,
        sunset_time_utc=sun_times.sunset_utc,
        golden_hour_start_utc=sun_times.golden_hour_start_utc,
        cloud_cover_total=weather.cloud_cover_total,
        cloud_cover_low=weather.cloud_cover_low,
        cloud_cover_mid=weather.cloud_cover_mid,
        cloud_cover_high=weather.cloud_cover_high,
        relative_humidity=weather.relative_humidity,
        precipitation_probability=weather.precipitation_probability,
        precipitation=weather.precipitation,
        visibility=weather.visibility,
        wind_speed=weather.wind_speed,
        quality_score=breakdown.total,
        quality_label=breakdown.label,
    )
    return forecast
