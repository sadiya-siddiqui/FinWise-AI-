from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Transaction
from ..schemas import ChatIn
from ..services import ai_service
from ..utils.security import current_user

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("")
def chat(body: ChatIn, user: User = Depends(current_user), db: Session = Depends(get_db)):
    ts = db.query(Transaction).filter(Transaction.user_id == user.id, Transaction.date >= date.today() - timedelta(days=90)) \
        .order_by(Transaction.date.desc()).all()
    return {"reply": ai_service.chat(body.message, ts)}
