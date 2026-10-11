from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from .config import settings
from .database import Base, engine, SessionLocal
from . import models  # noqa
from .models import User
from .routers import auth, plaid, transactions, insights, chat
from .services import plaid_service

def sync_all():
    db = SessionLocal()
    try:
        for u in db.query(User):
            try: plaid_service.sync_user(db, u.id)
            except Exception as e: print(f"sync failed for {u.id}: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)  # use Alembic migrations for production
    sched = BackgroundScheduler()
    sched.add_job(sync_all, "interval", hours=6)  # auto-sync every 6 hours
    sched.start()
    yield
    sched.shutdown()

app = FastAPI(title="FinWise AI", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS.split(","), allow_methods=["*"], allow_headers=["*"])
for r in (auth, plaid, transactions, insights, chat):
    app.include_router(r.router)

@app.get("/health")
def health(): return {"status": "ok"}
