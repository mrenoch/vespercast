"""
Astronomical calculations using the `astral` library.
Computes sunset time, golden hour start, and solar angle.
"""

import logging
from dataclasses import dataclass
from datetime import date, datetime, timezone

from astral import LocationInfo
from astral.sun import sun, golden_hour

logger = logging.getLogger(__name__)


@dataclass
class SunTimes:
    sunset_utc: datetime
    golden_hour_start_utc: datetime
    golden_hour_end_utc: datetime
    sunset_hour_local: int  # local hour (0–23) for weather lookup


def get_sun_times(lat: float, lng: float, target_date: date, timezone_name: str = "UTC") -> SunTimes | None:
    """
    Calculate sunset and golden hour times for a given location and date.
    Returns None if the sun doesn't set (polar regions).
    """
    try:
        loc = LocationInfo(
            name="location",
            region="",
            timezone=timezone_name,
            latitude=lat,
            longitude=lng,
        )
        s = sun(loc.observer, date=target_date, tzinfo=loc.timezone)
        gh = golden_hour(loc.observer, date=target_date, direction=1, tzinfo=loc.timezone)
    except Exception as exc:
        logger.error("astral calculation failed for (%s, %s) on %s: %s", lat, lng, target_date, exc)
        return None

    sunset_utc = s["sunset"].astimezone(timezone.utc)
    # golden_hour returns (start, end) tuple for the evening golden hour
    gh_start, gh_end = gh
    gh_start_utc = gh_start.astimezone(timezone.utc)
    gh_end_utc = gh_end.astimezone(timezone.utc)

    # Local sunset hour for matching Open-Meteo hourly data
    sunset_local_hour = s["sunset"].hour

    return SunTimes(
        sunset_utc=sunset_utc,
        golden_hour_start_utc=gh_start_utc,
        golden_hour_end_utc=gh_end_utc,
        sunset_hour_local=sunset_local_hour,
    )


def estimate_timezone(lng: float) -> str:
    """
    Very rough timezone estimate from longitude for initial weather queries.
    For production, use timezonefinder or GeoDjango's timezone support.
    """
    offset = round(lng / 15)
    if offset >= 0:
        return f"Etc/GMT-{offset}"
    else:
        return f"Etc/GMT+{abs(offset)}"
