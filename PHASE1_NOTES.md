# Phase 1 — Implemented (points 1–3)

Real geospatial map, official/government dashboard, and pest support.

## 1. Real map (choropleth)
- `frontend/public/maharashtra-districts.geojson` — real 35-district Maharashtra
  boundaries (2011 Census), simplified 1.2 MB → 151 KB.
- `backend/app/data/districts.py` — district centroids + revenue-division regions.
- `backend/app/services/hotspot_service.py` — rewritten: tracks `kind`
  (disease|pest), attaches coordinates, and adds `get_district_risk_map()`
  (one aggregated entry per district: risk %, all threats, crops affected,
  recommended action, lat/lng).
- `GET /risk-map` now returns `districts` (aggregated) **and** `hotspots` (flat).
- `frontend/components/MaharashtraRiskMap.tsx` — Leaflet choropleth, colour-coded
  by risk, click-to-inspect popups (risk %, crops affected, recommended action).
  Loaded client-side only via `next/dynamic` (`ssr: false`).
- `frontend/app/risk-map/page.tsx` — map view + legend + district detail panel,
  with a Map/List toggle (old cards kept as the list view).

## 2. Official dashboard
- New `official` role (`schemas.py`, `auth.py`, register page, redirects).
- `backend/app/routes/official.py` — `GET /official/dashboard` (surveillance
  summary, per-district register, threat leaderboard, division rollup) and
  `GET /official/export` (CSV). Read-only, district-level only.
- `frontend/app/official/page.tsx` — stat tiles, top threats, region rollup,
  district table, CSV export.
- Demo login: `official@demo.com / official123`.

## 3. Pest support (rule-based, honest interim)
- Pests are reported via a **farmer symptom checklist**, not image AI — the model
  is untouched, so nothing silently claims a pest classifier exists.
- `backend/app/data/advisory_kb.py` — 5 pests (Bollworm, Fall Armyworm, Tomato
  Fruit Borer, Aphids, Whitefly) with checklists, IPM actions, safe-usage notes.
- `backend/app/routes/pests.py` — `GET /meta/pests`, `POST /pest-report`,
  `GET /pest-reports`. Reports store into `predictions` with `kind:"pest"`, so they
  flow into hotspots, the risk map, and **district-wide alerts** automatically.
- Pests now also appear in the Treatment Guide (`/treatments`).
- `frontend/app/report-pest/page.tsx` — pest report form with checklist; added to
  the farmer sidebar.

## Run
```
# backend
cd backend && pip install -r requirements.txt
python seed.py            # seeds farmers, expert, official, pest reports, hotspots
uvicorn app.main:app --reload

# frontend
cd frontend && npm install   # installs leaflet + @types/leaflet (added)
npm run dev
```

## Validated
Python syntax (all files), pure-Python logic execution, GeoJSON validity,
i18n en/hi/mr key parity (143 each), route wiring. A full `npm run build` was not
run here — run it once locally to confirm the TS build in your environment.

## Not in this batch (your next 3 points)
Crop coverage (Cotton/Chilli/Soybean model), outbreak forecasting %, and the
remaining roadmap items.

---

# Phase 1 — Batch 2 (points 4–6)

Crop coverage, alert broadcast, and forward-looking outbreak forecast.

## 4. Crop coverage (Cotton, Soybean, Chilli) — honest scoping
- `backend/app/ml/class_map.py` — added the three crops to `SUPPORTED_CROPS`, with
  a per-crop `CROP_CAPABILITY` flag: `ai_disease` (model-backed: Tomato/Potato/Corn)
  vs `advisory_pest` (pest reports + advisories + risk, but no image model yet).
  Added growth stages; `risk_engine.py` got stage-vulnerability curves for each.
- `backend/app/routes/predictions.py` — **capability gate**: for non-model crops the
  API no longer runs the classifier (which would return a wrong Tomato/Potato/Corn
  class). It returns an honest response with environmental (weather+stage) risk, a
  forecast, and a pointer to pest reporting + advisories.
- `advisory_kb.py` — curated disease advisories added for Cotton (Bacterial blight,
  Leaf curl virus), Soybean (Rust, Yellow mosaic), Chilli (Anthracnose, Leaf curl).
- `/meta/crops` now returns `crop_capability` + `model_crops`.
- Frontend: capability badge on crop cards, an honest "coming soon" callout on the
  scan page and prediction page, and the new crops seeded (Cotton/Yavatmal,
  Soybean/Amravati).

## 5. Alert broadcast
- `backend/app/services/alert_service.py` — `broadcast_district_alert()` inserts an
  alert for **every farmer with a crop in the affected district** (deduped over a
  12h window), not just the scanning user.
- Wired into `predictions.py` (moderate/high disease detections). Pest reports
  already broadcast district-wide.

## 6. Outbreak forecast ("Predicted outbreak %")
- `backend/app/services/forecast_service.py` — transparent heuristic combining
  weather favorability, report momentum/trend, expert confirmations and current
  risk into a 0–100 probability with exposed drivers (not a black-box model).
- Attached to prediction responses (`forecast`) and to each district in the risk
  map (`outbreak_forecast`, `forecast_level`).
- Frontend: forecast meter on the prediction page, in the risk-map detail panel and
  map popup, and a Forecast column in the official district register.

## Validated (batch 2)
Python syntax (all files), cross-module reference checks, forecast/capability logic
executed, i18n en/hi/mr parity (152 keys each), every i18n key used in the frontend
confirmed to exist. Run `npm run build` once locally to confirm the TS build.
