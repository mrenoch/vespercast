# VesperCast

> *Vesper* (n.) — the evening star; of or relating to the west at dusk.

VesperCast is a sunset quality prediction app. You enter a location, and it tells you how good tonight's sunset is going to be — and why.

Not just a cloud cover percentage. A real score, built from the atmospheric conditions that actually determine whether you'll see a wall of orange fire across the sky or a flat grey nothing. Mid-altitude clouds catch the most color. High cirrus produces dramatic streaks. Low stratus just blocks everything. Humidity hazes it out. Rain kills it. The right combination of all of these, aligned with your horizon, is what makes a memorable sunset — and that's what VesperCast tries to predict.

---

## The Idea

Most weather apps treat sunset as an afterthought — a timestamp buried in the forecast. Photographers, hikers, sailors, and anyone who's ever pulled over on the side of the road to watch the sky know that a great sunset is an event worth planning for.

VesperCast is built around that idea. The long-term vision:

- **Daily forecasts** for any location in the world, scored 0–100 with a plain-language label (poor / fair / good / great / epic)
- **Saved places** so your favorite overlooks, beaches, and rooftops are one tap away
- **Alerts** that notify you when a great sunset is coming — early enough to actually get there
- **A feedback loop**: users rate what they actually saw, and over time those ratings train a better model. Predicted score vs. observed experience becomes the dataset that makes future predictions more accurate
- **Community knowledge**: horizon obstructions, local microclimates, and viewing spots that the raw weather data can't know about

The current Phase 1 delivers the core: enter any address, get a scored forecast backed by real atmospheric data.

---

## How the Score Works

The quality score is a weighted geometric mean of six factors. The geometric mean matters: a catastrophic condition (heavy rain, total overcast) drives the whole score toward zero regardless of how favorable everything else is. No silver linings.

| Factor | Weight | What it measures |
|---|---|---|
| Cloud cover | 40% | Mid clouds (20–50%) and high clouds (15–60%) are ideal; low clouds kill color |
| Precipitation | 25% | Rain or high probability → steep penalty |
| Humidity | 15% | Ideal 30–55%; above 85% hazes out saturation |
| Visibility | 12% | Above 20km is perfect; below 2km is fog or smoke |
| Wind | 4% | Gentle wind clears haze; minor overall factor |
| Horizon | 4% | Degrees of western terrain blockage at your specific location |

Weather data comes from [Open-Meteo](https://open-meteo.com/) (free, no API key). Sunset and golden hour times are calculated with the `astral` library using your exact coordinates.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Django 5.1, GeoDjango, Django REST Framework |
| Database | SQLite + SpatiaLite (PostgreSQL + PostGIS ready when needed) |
| Task queue | Django-Q2 (ORM broker, no Redis required in development) |
| Weather | Open-Meteo API |
| Astronomy | `astral` library |
| Frontend | React 18, Vite, TypeScript |
| Styling | CSS Modules |
| Data fetching | React Query + axios |

---

## Getting Started

### Prerequisites

- [Postgres.app](https://postgresapp.com/) (provides GDAL 3.7.3 — required for GeoDjango)
- `brew install libspatialite`
- `uv` — [install](https://docs.astral.sh/uv/getting-started/installation/)
- Node.js 20+

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export PATH="/Applications/Postgres.app/Contents/Versions/16/bin:$PATH"
export GDAL_LIBRARY_PATH="/Applications/Postgres.app/Contents/Versions/16/lib/libgdal.dylib"
export GEOS_LIBRARY_PATH="/Applications/Postgres.app/Contents/Versions/16/lib/libgeos_c.dylib"
export PROJ_LIB="/Applications/Postgres.app/Contents/Versions/16/share/proj"
```

### Install & run

```bash
git clone <repo>
cd vespercast

make install   # installs Python + Node dependencies
make migrate   # sets up the local database
make run       # starts backend :8000 and frontend :5173
```

Then open [http://localhost:5173](http://localhost:5173).

### Other useful commands

```bash
make run-backend    # Django only
make run-frontend   # Vite only
make shell          # Django interactive shell
make test           # backend test suite
make clean-db       # wipe and re-migrate from scratch
```

---

## API

```
POST /api/v1/locations/geocode/     address → lat/lng + elevation
POST /api/v1/locations/             save a location
GET  /api/v1/forecasts/             ?lat=&lng=&date=YYYY-MM-DD
POST /api/v1/ratings/               submit a 1–5 star rating
GET  /api/v1/accounts/locations/    authenticated user's saved places
```

Forecasts are cached for 3 hours. Omit `date` to get today's forecast.

---

## Project Structure

```
vespercast/
├── backend/
│   ├── apps/
│   │   ├── locations/       # GeoDjango Location model, geocoding
│   │   ├── forecasts/       # Prediction logic, Open-Meteo, scorer
│   │   ├── ratings/         # User ratings (ML training data)
│   │   ├── accounts/        # Saved places
│   │   └── notifications/   # Alert preferences
│   └── config/settings/
│       ├── base.py
│       ├── development.py   # SpatiaLite, DEBUG=True
│       └── test.py
├── frontend/
│   └── src/
│       ├── components/      # LocationSearch, ForecastCard, QualityMeter, SunsetDetails
│       ├── hooks/           # useForecast (React Query)
│       ├── api/             # axios client
│       └── types/           # TypeScript interfaces
└── docs/
    ├── plan.md              # original architecture plan
    └── todo.md              # roadmap and open tasks
```

---

## Roadmap

See [`docs/todo.md`](docs/todo.md) for the full list. High-level phases:

- **Phase 1** ✅ — Core forecast: location search, scored prediction, atmospheric details
- **Phase 2** — User accounts, saved places, push/email alerts before good sunsets
- **Phase 3** — ML feedback loop: user ratings retrain the scoring model over time

---

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
