# FinWise AI
Multi-bank finance manager with AI insights. FastAPI + SQLAlchemy + PostgreSQL + Redis · React 18 + Vite + Tailwind + Recharts · Plaid · Groq/OpenAI · Prophet.

## Quick start
1. Get free keys: [Plaid](https://dashboard.plaid.com) (sandbox) and [Groq](https://console.groq.com) (or any OpenAI-compatible API).
2. Edit `backend/.env`: set `PLAID_CLIENT_ID`, `PLAID_SECRET`, `LLM_API_KEY`, and a random `SECRET_KEY` (`openssl rand -hex 32`).
3. `docker compose up --build` then open http://localhost:5173 (API docs: http://localhost:8000/docs).
4. Register, click **Link bank account**, choose any sandbox bank (user `user_good`, pass `pass_good`).

### Without Docker
- Backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload` (set `DATABASE_URL`; defaults to SQLite, Redis is optional).
- Frontend: `cd frontend && npm install && npm run dev`

## Features
Plaid linking · `transactions/sync` every 6h (APScheduler) · rule + LLM categorization · chat over your data · Prophet 30-day forecast (moving-average fallback) · subscription detection · budgets with 80%/100% alerts · Redis-cached dashboards.

## Deploy
- Backend → Railway/Render: root `backend/`, Dockerfile, set env vars from `.env`, add Postgres + Redis, set `CORS_ORIGINS` to your Vercel URL.
- Frontend → Vercel: root `frontend/`, env `VITE_API_URL=<backend URL>`.

## Known gaps / next steps
Plaid access tokens are stored unencrypted (encrypt before production) · no Alembic migrations (tables auto-created) · budget alerts are in-app only (no email/push) · no tests · Google/GitHub OAuth login not wired (password OAuth2 flow only) · scheduler runs in-process (use a worker if you scale to multiple instances).
