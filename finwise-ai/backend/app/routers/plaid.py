from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import PublicToken
from ..models import User, Account
from ..services import plaid_service
from ..utils.security import current_user

router = APIRouter(prefix="/api/plaid", tags=["plaid"])

@router.post("/link-token")
def link_token(user: User = Depends(current_user)):
    return {"link_token": plaid_service.create_link_token(user.id)}

@router.post("/exchange")
def exchange(body: PublicToken, user: User = Depends(current_user), db: Session = Depends(get_db)):
    plaid_service.exchange_and_store(db, user.id, body.public_token)
    return {"status": "linked"}

@router.post("/sync")
def sync(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return {"added": plaid_service.sync_user(db, user.id)}

@router.get("/accounts")
def accounts(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return [{"id": a.id, "name": a.name, "institution": a.institution, "type": a.type, "balance": a.balance}
            for a in db.query(Account).filter_by(user_id=user.id)]
