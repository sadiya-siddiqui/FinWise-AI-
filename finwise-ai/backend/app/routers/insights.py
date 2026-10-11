from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Transaction, Insight
from ..schemas import BudgetIn
from ..services import forecast_service
from ..utils.security import current_user
from ..utils.cache import cached

router = APIRouter(prefix="/api/insights", tags=["insights"])

def _txns(db, uid, days=180):
    return db.query(Transaction).filter(Transaction.user_id == uid, Transaction.date >= date.today() - timedelta(days=days)).all()

@router.get("/forecast")
def forecast(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return cached(f"u{user.id}:forecast", 3600, lambda: forecast_service.forecast_spending(_txns(db, user.id)))

@router.get("/subscriptions")
def subscriptions(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return cached(f"u{user.id}:subs", 3600, lambda: forecast_service.detect_subscriptions(_txns(db, user.id, 400)))

@router.post("/budgets")
def set_budget(body: BudgetIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    b = next((i for i in db.query(Insight).filter_by(user_id=user.id, kind="budget") if i.data["category"] == body.category), None)
    if b: b.data = {"category": body.category, "limit": body.limit}
    else: db.add(Insight(user_id=user.id, kind="budget", title=body.category, data=body.model_dump()))
    db.commit()
    return {"ok": True}

@router.get("/alerts")
def alerts(user: User = Depends(current_user), db: Session = Depends(get_db)):
    start = date.today().replace(day=1)
    spent = {}
    for t in db.query(Transaction).filter(Transaction.user_id == user.id, Transaction.date >= start, Transaction.amount > 0):
        spent[t.category] = spent.get(t.category, 0) + t.amount
    out = []
    for b in db.query(Insight).filter_by(user_id=user.id, kind="budget"):
        s, lim = spent.get(b.data["category"], 0), b.data["limit"]
        pct = round(s / lim * 100) if lim else 0
        out.append({"category": b.data["category"], "spent": round(s, 2), "limit": lim, "percent": pct,
                    "level": "over" if pct >= 100 else "warning" if pct >= 80 else "ok"})
    return sorted(out, key=lambda x: -x["percent"])
