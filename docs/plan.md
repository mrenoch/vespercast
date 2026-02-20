# VesperCast — Project Scaffold Plan

## Context
Building VesperCast from scratch: a sunset quality prediction web app using Django + GeoDjango backend, React + Vite frontend. Phase 1 goal is a working end-to-end flow: enter a location → see a sunset quality forecast with score and details.

---

## Stack Decisions
- **Backend:** Python 3.12, Django 5.1, GeoDjango, Django REST Framework
- **Database:** SQLite + SpatiaLite only (PostgreSQL/PostGIS deferred to later)
- **Task queue:** Django-Q2 (ORM broker, no Redis needed for dev)
- **Weather:** Open-Meteo (free, no API key)
- **Astronomy:** `astral` library
- **Frontend:** React 18 + Vite + TypeScript
- **Package manager:** `uv` (backend), `npm` (frontend)
- **Location:** `~/projects/vespercast`

---

## Directory Structure

```
~/projects/vespercast/
├── .gitignore
├── Makefile
├── docs/
│   ├── plan.md
│   └── todo.md
├── backend/
│   ├── pyproject.toml           # uv project manifest
│   ├── manage.py
│   ├── config/
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── settings/
│   │       ├── base.py
│   │       ├── development.py   # SpatiaLite, DEBUG=True
│   │       └── test.py
│   └── apps/
│       ├── locations/           # GeoDjango Location model, geocoding
│       │   └── services/geocoding.py
│       ├── forecasts/           # Core prediction logic
│       │   └── services/
│       │       ├── open_meteo.py
│       │       ├── astro.py
│       │       └── scorer.py    # quality score algorithm
│       ├── ratings/             # ML training data collection
│       ├── accounts/            # UserLocation, saved places
│       └── notifications/       # Alert preferences (stub for Phase 2)
└── frontend/
    ├── vite.config.ts           # proxies /api → Django :8000
    └── src/
        ├── api/                 # axios client + typed API calls
        ├── components/
        │   ├── LocationSearch/  # address input + geolocation button
        │   ├── ForecastCard/    # main result display
        │   ├── QualityMeter/    # score progress bar
        │   └── SunsetDetails/   # cloud layers, humidity, etc.
        ├── hooks/useForecast.ts # React Query hook
        ├── pages/HomePage.tsx
        └── types/index.ts
```

---

## Key Models

### `apps/locations` — `Location`
```python
point = PointField(geography=True, srid=4326)  # GeoDjango
elevation = FloatField(null=True)
horizon_elevation_west = FloatField(default=0.0)  # degrees above flat
```

### `apps/forecasts` — `SunsetForecast`
```python
location = ForeignKey(Location)
forecast_date = DateField()
sunset_time_utc = DateTimeField()
golden_hour_start_utc = DateTimeField()
cloud_cover_total / low / mid / high = FloatField()
relative_humidity = FloatField()
precipitation_probability = FloatField()
precipitation = FloatField()
visibility = FloatField(null=True)
wind_speed = FloatField(null=True)
quality_score = FloatField()     # 0–100
quality_label = CharField()      # poor/fair/good/great/epic
unique_together = [("location", "forecast_date")]
```

### `apps/ratings` — `SunsetRating`
```python
forecast = ForeignKey(SunsetForecast)
user = ForeignKey(User, null=True)   # anonymous allowed
score = PositiveSmallIntegerField()  # 1–5
comment = TextField(blank=True)
# Used as ML training data: predicted score vs. observed rating
```

### `apps/accounts` — `UserLocation`
```python
user = ForeignKey(User)
location = ForeignKey(Location)
nickname = CharField(blank=True)
is_primary = BooleanField()
```

### `apps/notifications` — `NotificationPreference` + `Notification`
```python
minimum_score_threshold = FloatField(default=60.0)
notify_minutes_before = PositiveSmallIntegerField(default=60)
notify_via_email / notify_via_push = BooleanField()
```

---

## Quality Score Algorithm (`apps/forecasts/services/scorer.py`)

**Weighted geometric mean** — any catastrophic factor (rain, total overcast) drives the score to zero. No compensation from other factors.

| Factor | Weight | Logic |
|--------|--------|-------|
| Cloud | 40% | Sweet spot: mid clouds 20–50%, high clouds 15–60%, low clouds < 10% |
| Precipitation | 25% | > 0.2mm or > 40% probability → steep penalty |
| Humidity | 15% | Ideal 30–55%; > 85% → haze washes out color |
| Visibility | 12% | > 20km = perfect; < 2km = fog/smoke |
| Wind | 4% | Gentle wind clears haze; minor factor |
| Horizon | 4% | degrees of western terrain blockage |

Score → label: 0–20 poor, 21–45 fair, 46–65 good, 66–85 great, 86–100 epic

---

## Phase 1 API Endpoints

```
POST /api/v1/locations/geocode/     address → lat/lng + elevation
POST /api/v1/locations/             save a location
GET  /api/v1/forecasts/             ?lat=&lng=&date= → SunsetForecast
                                    cache: serve if fetched < 3hrs ago
POST /api/v1/ratings/               submit 1–5 star rating
GET  /api/v1/accounts/locations/    user's saved locations
```

---

## macOS Setup (Critical)

GDAL Python package version **must match** system GDAL from Postgres.app (3.7.3). No PostgreSQL installation needed — SpatiaLite runs on top of SQLite.

```bash
# Prerequisites
brew install libspatialite

# Add to ~/.zshrc (uses Postgres.app's bundled GDAL — no separate brew install needed):
export PATH="/Applications/Postgres.app/Contents/Versions/16/bin:$PATH"
export GDAL_LIBRARY_PATH="/Applications/Postgres.app/Contents/Versions/16/lib/libgdal.dylib"
export GEOS_LIBRARY_PATH="/Applications/Postgres.app/Contents/Versions/16/lib/libgeos_c.dylib"
export PROJ_LIB="/Applications/Postgres.app/Contents/Versions/16/share/proj"
```

`development.py` settings:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
SPATIALITE_LIBRARY_PATH = "/opt/homebrew/lib/mod_spatialite.dylib"
GDAL_LIBRARY_PATH = "/Applications/Postgres.app/Contents/Versions/16/lib/libgdal.dylib"
GEOS_LIBRARY_PATH = "/Applications/Postgres.app/Contents/Versions/16/lib/libgeos_c.dylib"
```

> PostgreSQL/PostGIS migration deferred — the Django ORM swap is a one-line `ENGINE` change when needed.

---

## Scaffolding Steps (completed)

1. **System deps:** `brew install libspatialite`, env vars added to `~/.zshrc`
2. **Monorepo root:** `~/projects/vespercast` + git init
3. **Backend:**
   - `uv init` + dependencies installed
   - `django-admin startproject config .`
   - Settings split into `settings/` package
   - 5 apps created: locations, forecasts, ratings, accounts, notifications
   - Models, services, views, serializers, urls populated
   - `makemigrations && migrate` — all OK
4. **Frontend:**
   - `npm create vite@latest frontend -- --template react-ts`
   - `@tanstack/react-query`, `axios`, `date-fns`, `date-fns-tz` installed
   - Vite proxy configured (`/api → localhost:8000`)
   - Components, hooks, types, api client scaffolded
5. **Verified:** `GET /api/v1/forecasts/?lat=34.025&lng=-118.780` returns `quality_score: 74.5, quality_label: "great"`

---

## Verification Commands

```bash
# Backend smoke test
curl "http://localhost:8000/api/v1/forecasts/?lat=34.025&lng=-118.780"
# Returns JSON with quality_score, sunset_time_utc, cloud data

# GeoDjango sanity check
python manage.py shell -c "
from django.contrib.gis.geos import Point
p = Point(-118.780, 34.025, srid=4326)
print('GeoDjango OK:', p)
"

# Frontend: http://localhost:5173 — enter "Malibu, CA" → see forecast card
```
