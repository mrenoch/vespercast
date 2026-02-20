"""
Open-Meteo weather data fetcher.
Free API, no key required.
Docs: https://open-meteo.com/en/docs
"""

import logging
from dataclasses import dataclass
from datetime import date

import httpx

logger = logging.getLogger(__name__)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

HOURLY_VARS = [
    "cloudcover",
    "cloudcover_low",
    "cloudcover_mid",
    "cloudcover_high",
    "relativehumidity_2m",
    "precipitation_probability",
    "precipitation",
    "visibility",
    "windspeed_10m",
]


@dataclass
class HourlyWeather:
    """Weather conditions for a single hour."""
    time: str  # ISO8601 local time
    cloud_cover_total: float
    cloud_cover_low: float
    cloud_cover_mid: float
    cloud_cover_high: float
    relative_humidity: float
    precipitation_probability: float
    precipitation: float
    visibility: float | None
    wind_speed: float | None


def fetch_hourly_weather(
    lat: float,
    lng: float,
    target_date: date,
    timezone: str = "UTC",
) -> list[HourlyWeather]:
    """
    Fetch hourly weather for a given location and date.
    Returns a list of HourlyWeather objects for each hour of the day.
    """
    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": ",".join(HOURLY_VARS),
        "start_date": target_date.isoformat(),
        "end_date": target_date.isoformat(),
        "timezone": timezone,
        "windspeed_unit": "kmh",
        "precipitation_unit": "mm",
    }

    try:
        resp = httpx.get(OPEN_METEO_URL, params=params, timeout=15.0)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error("Open-Meteo request failed: %s", exc)
        raise

    data = resp.json()
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])

    results = []
    for i, time_str in enumerate(times):
        results.append(
            HourlyWeather(
                time=time_str,
                cloud_cover_total=float(hourly["cloudcover"][i] or 0),
                cloud_cover_low=float(hourly["cloudcover_low"][i] or 0),
                cloud_cover_mid=float(hourly["cloudcover_mid"][i] or 0),
                cloud_cover_high=float(hourly["cloudcover_high"][i] or 0),
                relative_humidity=float(hourly["relativehumidity_2m"][i] or 50),
                precipitation_probability=float(hourly["precipitation_probability"][i] or 0),
                precipitation=float(hourly["precipitation"][i] or 0),
                visibility=float(hourly["visibility"][i]) if hourly["visibility"][i] is not None else None,
                wind_speed=float(hourly["windspeed_10m"][i]) if hourly["windspeed_10m"][i] is not None else None,
            )
        )

    return results


def get_weather_at_sunset(
    lat: float,
    lng: float,
    target_date: date,
    sunset_hour: int,
    timezone: str = "UTC",
) -> HourlyWeather | None:
    """Return the HourlyWeather closest to the sunset hour."""
    hourly = fetch_hourly_weather(lat, lng, target_date, timezone)
    if not hourly:
        return None

    # Find the entry closest to the sunset hour
    def hour_of(hw: HourlyWeather) -> int:
        return int(hw.time.split("T")[1].split(":")[0])

    return min(hourly, key=lambda hw: abs(hour_of(hw) - sunset_hour))
