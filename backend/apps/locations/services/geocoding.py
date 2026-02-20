"""
Geocoding service using Nominatim (OpenStreetMap) via geopy.
No API key required.
"""

import logging
from dataclasses import dataclass

import httpx
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

logger = logging.getLogger(__name__)

OPEN_ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup"


@dataclass
class GeocodingResult:
    name: str
    lat: float
    lng: float
    elevation: float | None = None


def geocode_address(address: str) -> GeocodingResult | None:
    """Convert a freeform address string to lat/lng + elevation."""
    geocoder = Nominatim(user_agent="vespercast/1.0")
    try:
        location = geocoder.geocode(address, exactly_one=True, timeout=10)
    except (GeocoderTimedOut, GeocoderServiceError) as exc:
        logger.error("Geocoding failed for %r: %s", address, exc)
        return None

    if location is None:
        return None

    lat, lng = location.latitude, location.longitude
    elevation = _fetch_elevation(lat, lng)

    return GeocodingResult(
        name=location.address,
        lat=lat,
        lng=lng,
        elevation=elevation,
    )


def _fetch_elevation(lat: float, lng: float) -> float | None:
    """Fetch elevation in metres from open-elevation.com."""
    try:
        resp = httpx.get(
            OPEN_ELEVATION_URL,
            params={"locations": f"{lat},{lng}"},
            timeout=8.0,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if results:
            return float(results[0]["elevation"])
    except Exception as exc:
        logger.warning("Elevation fetch failed for (%s, %s): %s", lat, lng, exc)
    return None
