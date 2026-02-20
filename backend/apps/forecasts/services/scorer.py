"""
Sunset quality scoring algorithm.

Uses a weighted geometric mean so that any catastrophic factor (rain, total
overcast) drives the overall score toward zero.  No single good metric can
compensate for a truly bad condition.

Weights
-------
Cloud   40%  Sweet spot: mid 20–50%, high 15–60%, low < 10%
Precip  25%  > 0.2mm or > 40% prob → steep penalty
Humidity 15% Ideal 30–55%; > 85% = hazy, washed-out colors
Visibility 12% > 20km perfect; < 2km fog/smoke
Wind     4%  Gentle wind clears haze; minor factor
Horizon  4%  Degrees of western terrain blockage

Score → label: 0–20 poor, 21–45 fair, 46–65 good, 66–85 great, 86–100 epic
"""

import math
from dataclasses import dataclass


@dataclass
class ScoreBreakdown:
    total: float
    label: str
    cloud_score: float
    precipitation_score: float
    humidity_score: float
    visibility_score: float
    wind_score: float
    horizon_score: float


def score_cloud(low: float, mid: float, high: float) -> float:
    """
    Score cloud conditions.
    Low cloud < 10% is ideal; mid 20–50% and high 15–60% produce vivid color.
    Total overcast → 0.
    """
    # Low cloud penalty (fog, stratus blocks color entirely)
    if low >= 90:
        return 0.0
    low_score = max(0.0, 1.0 - (low / 10.0) ** 1.5)

    # Mid cloud sweet spot: 20–50%
    if mid <= 20:
        mid_score = mid / 20.0
    elif mid <= 50:
        mid_score = 1.0
    elif mid <= 80:
        mid_score = 1.0 - (mid - 50) / 30.0
    else:
        mid_score = 0.1

    # High cloud sweet spot: 15–60%
    if high <= 15:
        high_score = high / 15.0
    elif high <= 60:
        high_score = 1.0
    elif high <= 90:
        high_score = 1.0 - (high - 60) / 30.0
    else:
        high_score = 0.05

    return low_score * 0.5 + mid_score * 0.3 + high_score * 0.2


def score_precipitation(precip_mm: float, precip_prob: float) -> float:
    """Rain or high probability washes out the sky."""
    if precip_mm > 0.2 or precip_prob > 40:
        # Steep exponential drop
        penalty = max(precip_mm / 5.0, precip_prob / 100.0)
        return max(0.0, 1.0 - penalty ** 0.5)
    # Very light chance of showers still slightly penalized
    return max(0.0, 1.0 - (precip_prob / 100.0) * 0.5)


def score_humidity(rh: float) -> float:
    """Ideal 30–55%; > 85% = haze that washes out saturation."""
    if 30 <= rh <= 55:
        return 1.0
    elif rh < 30:
        # Very dry air is still fine — minor penalty below 20%
        return 0.85 + (rh / 30.0) * 0.15
    elif rh <= 70:
        return 1.0 - (rh - 55) / 15.0 * 0.3
    elif rh <= 85:
        return 0.7 - (rh - 70) / 15.0 * 0.5
    else:
        return max(0.0, 0.2 - (rh - 85) / 15.0 * 0.2)


def score_visibility(vis_km: float | None) -> float:
    """> 20km = perfect; < 2km = fog/smoke."""
    if vis_km is None:
        return 0.75  # unknown — assume moderate
    if vis_km >= 20:
        return 1.0
    elif vis_km >= 10:
        return 0.75 + (vis_km - 10) / 10.0 * 0.25
    elif vis_km >= 2:
        return (vis_km - 2) / 8.0 * 0.75
    else:
        return 0.0


def score_wind(wind_kmh: float | None) -> float:
    """Gentle wind clears haze; very strong wind stirs dust."""
    if wind_kmh is None:
        return 0.75
    if wind_kmh <= 20:
        return 0.7 + (wind_kmh / 20.0) * 0.3
    elif wind_kmh <= 40:
        return 1.0 - (wind_kmh - 20) / 20.0 * 0.3
    else:
        return max(0.3, 0.7 - (wind_kmh - 40) / 40.0)


def score_horizon(horizon_deg: float) -> float:
    """Degrees of western terrain blockage hurts golden color window."""
    if horizon_deg <= 0:
        return 1.0
    elif horizon_deg <= 5:
        return 1.0 - horizon_deg / 5.0 * 0.3
    elif horizon_deg <= 15:
        return 0.7 - (horizon_deg - 5) / 10.0 * 0.5
    else:
        return max(0.0, 0.2 - (horizon_deg - 15) / 10.0 * 0.2)


def label_from_score(score: float) -> str:
    if score <= 20:
        return "poor"
    elif score <= 45:
        return "fair"
    elif score <= 65:
        return "good"
    elif score <= 85:
        return "great"
    else:
        return "epic"


WEIGHTS = {
    "cloud": 0.40,
    "precipitation": 0.25,
    "humidity": 0.15,
    "visibility": 0.12,
    "wind": 0.04,
    "horizon": 0.04,
}


def compute_quality_score(
    cloud_low: float,
    cloud_mid: float,
    cloud_high: float,
    precipitation: float,
    precipitation_probability: float,
    relative_humidity: float,
    visibility: float | None,
    wind_speed: float | None,
    horizon_elevation_west: float = 0.0,
) -> ScoreBreakdown:
    """
    Compute a 0–100 quality score using a weighted geometric mean.
    Each sub-score is in [0, 1].
    """
    sub_scores = {
        "cloud": score_cloud(cloud_low, cloud_mid, cloud_high),
        "precipitation": score_precipitation(precipitation, precipitation_probability),
        "humidity": score_humidity(relative_humidity),
        "visibility": score_visibility(visibility),
        "wind": score_wind(wind_speed),
        "horizon": score_horizon(horizon_elevation_west),
    }

    # Weighted geometric mean: product of (s ** w)
    log_sum = sum(
        WEIGHTS[k] * math.log(max(s, 1e-9))
        for k, s in sub_scores.items()
    )
    raw = math.exp(log_sum)  # in [0, 1]
    total = round(raw * 100, 1)

    return ScoreBreakdown(
        total=total,
        label=label_from_score(total),
        cloud_score=round(sub_scores["cloud"] * 100, 1),
        precipitation_score=round(sub_scores["precipitation"] * 100, 1),
        humidity_score=round(sub_scores["humidity"] * 100, 1),
        visibility_score=round(sub_scores["visibility"] * 100, 1),
        wind_score=round(sub_scores["wind"] * 100, 1),
        horizon_score=round(sub_scores["horizon"] * 100, 1),
    )
