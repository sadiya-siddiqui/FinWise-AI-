from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Transaction
from ..utils.security import current_user
from ..utils.cache import cached

router = APIRouter(prefix="/api/transactions", tags=["transactions"])

@router.get("")
def list_txns(limit: int = 100, category: str | None = None, user: User = Depends(current_user), db: Session = Depends(get_db)):
    q = db.query(Transaction).filter_by(user_id=user.id)
    if category:
        q = q.filter_by(category=category)
    return [{"id": t.id, "date": t.date.isoformat(), "name": t.name, "merchant": t.merchant, "amount": t.amount,
             "category": t.category, "pending": t.pending} for t in q.order_by(Transaction.date.desc()).limit(limit)]

@router.get("/summary")
def summary(days: int = 30, user: User = Depends(current_user), db: Session = Depends(get_db)):
    def compute():
        since = date.today() - timedelta(days=days)
        ts = db.query(Transaction).filter(Transaction.user_id == user.id, Transaction.date >= since).all()
        cats, daily, income = {}, {}, 0.0
        for t in ts:
            if t.amount < 0 or t.category == "Income":
                income += abs(t.amount); continue
            cats[t.category] = cats.get(t.category, 0) + t.amount
            daily[t.date.isoformat()] = daily.get(t.date.isoformat(), 0) + t.amount
        return {"total_spent": round(sum(cats.values()), 2), "income": round(income, 2),
                "by_category": [{"category": k, "amount": round(v, 2)} for k, v in sorted(cats.items(), key=lambda x: -x[1])],
                "daily": [{"date": k, "amount": round(v, 2)} for k, v in sorted(daily.items())]}
    return cached(f"u{user.id}:summary:{days}", 300, compute)
