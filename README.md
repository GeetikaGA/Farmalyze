# Farmalyze

Farmalyze is a crop-health early-warning and decision-support platform: farmers photograph a
leaf, get an AI-assisted diagnosis with confidence and an explainability heatmap, a
context-aware risk score, curated (non-AI-invented) treatment guidance, and — when confidence
is low or risk is high — a route to a human expert for verification. Agri-officers get a
district-level risk map and a review queue.

Workflow: **Detect → Assess risk → Alert → Act → Verify → Monitor**

This repo merges two source projects:
- The **Farmalyze brand and UI** (Next.js/TypeScript, custom CSS design system) — kept as-is.
- The **SIH'26 "Crop Health Early-Warning & Decision Support System"** backend and feature set
  (FastAPI + MongoDB + TensorFlow/Grad-CAM) — fully re-implemented in the Farmalyze frontend.

## What's included

| Area | Pages / endpoints |
|---|---|
| Marketing site | `/` |
| Auth | `/login`, `/register` → `POST /auth/login`, `POST /auth/register` |
| Farmer dashboard | `/dashboard` — quick scan, field snapshot, alerts, hotspots, recent scans |
| Crops | `/crops`, `/crops/[id]` → `GET/POST /crops`, `GET/PUT/DELETE /crops/{id}` |
| Diagnosis | `/scan` → `POST /predict` (multipart image upload) |
| Result | `/prediction/[id]` → `GET /predictions/{id}`, Grad-CAM explainability, risk factors, curated recommendation, `POST /verify-request` |
| Risk map | `/risk-map` → `GET /risk-map` |
| Alerts | `/alerts` → `GET /alerts`, `PATCH /alerts/{id}/read` |
| History | `/history` → `GET /reports` |
| Expert desk | `/expert`, `/expert/reviews` → `GET /expert/dashboard`, `GET /expert/pending`, `POST /expert/review` |
| Verification status | `/verification/[id]` → `GET /verify-status/{id}` |
| Settings | `/settings` — account info, language (English/Hindi) |

Every farmer-only, expert-only, and shared route from the original app is present and wired to
the real backend (no mock data). Role-based access (`farmer` vs `expert`) and the low/moderate/
high risk language are preserved as in the original.

## Project layout

```
farmalyze/
├── frontend/          Next.js app (Farmalyze branding + all product features)
├── backend/           FastAPI service (unchanged logic from SIH'26)
├── scripts/           start-backend.sh, start-frontend.sh
├── docker-compose.yml MongoDB service
└── .env.example       Reference for all env vars (backend + frontend)
```

## Running it locally

### 1. MongoDB
```bash
docker compose up -d mongodb
# or point MONGODB_URL at an existing instance
```

### 2. Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # edit JWT_SECRET
python seed.py               # creates demo users + demo data
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend
```bash
cd frontend
cp .env.example .env.local   # NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

Open http://localhost:3000. Demo accounts (from `seed.py`): `farmer@demo.com` / `farmer123`
and `expert@demo.com` / `expert123`.

Or use the helper scripts: `scripts/start-backend.sh` and `scripts/start-frontend.sh`.

## Notes

- The ML model, risk engine, weather service, hotspot aggregation, and advisory knowledge base
  are unchanged from the original backend — this project only replaced the frontend, so the
  product's core intelligence is untouched.
- District-level data only — no precise farmer location is ever exposed on the risk map, per
  the original design.
- Demo/simulated data may appear in the risk map and hotspot views, as in the source project.
