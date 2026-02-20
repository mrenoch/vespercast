# VesperCast — TODO

## Quick Wins

- [ ] Add `timezonefinder` library to replace rough longitude-based timezone estimate in `apps/forecasts/services/astro.py` — fixes golden hour accuracy for locations near timezone boundaries
- [ ] Wire up geocode → save location → fetch forecast flow in the frontend (currently the UI queries by lat/lng directly without persisting the location to the DB)
- [ ] Fix `accounts/serializers.py` `__import__` hack — replace with a proper top-level import of `Location`
- [ ] Use `timezonefinder` result to display local sunset time in `SunsetDetails` (currently shows UTC; `toZonedTime` is imported but unused)

## Phase 1 Completion

- [ ] Star rating UI on `ForecastCard` — the `POST /api/v1/ratings/` endpoint is live, just needs a frontend widget
- [ ] 7-day forecast strip — Open-Meteo returns up to 16 days free; add a date picker or day row to `HomePage`
- [ ] Better error states for edge cases: polar coordinates, far-future dates, network failures
- [ ] Loading skeleton for `ForecastCard` instead of plain spinner

## Code Quality

- [ ] Replace `estimate_timezone` with `timezonefinder` throughout before Phase 2
- [ ] Add basic tests for the scorer algorithm (`apps/forecasts/services/scorer.py`)
- [ ] Add tests for the forecast view cache logic
- [ ] Lint / format pass (consider `ruff` for backend, `eslint` already scaffolded for frontend)

## Phase 2 — User Accounts & Saved Places

- [ ] Auth endpoints (registration, login, logout) — Django allauth or simple JWT
- [ ] Saved locations UI — `GET /api/v1/accounts/locations/` is ready, needs frontend
- [ ] Primary location auto-loaded on page visit
- [ ] Nickname editing for saved locations

## Phase 2 — Notifications (stub already in DB)

- [ ] Notification preference UI (threshold score, minutes before sunset, email/push toggle)
- [ ] Django-Q2 scheduled task to send alerts when forecast quality exceeds threshold
- [ ] Email backend configuration (SMTP or SendGrid)
- [ ] Push notification support (Web Push API)

## Phase 3 — ML / Feedback Loop

- [ ] Admin view showing predicted score vs. user ratings over time
- [ ] Export `SunsetRating` + `SunsetForecast` pairs as CSV for model training
- [ ] Retrain / recalibrate scorer weights from collected ratings
- [ ] A/B test new scoring models against baseline

## Infrastructure (deferred)

- [ ] Swap SQLite + SpatiaLite → PostgreSQL + PostGIS (one-line `ENGINE` change in settings)
- [ ] Dockerize backend + frontend
- [ ] CI pipeline (GitHub Actions): lint, test, build
- [ ] Production settings (`config/settings/production.py`) — static files, HTTPS, allowed hosts
