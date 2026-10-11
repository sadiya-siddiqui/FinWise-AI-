from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, Token
from ..utils.security import hash_pw, verify_pw, make_token, current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(body: UserCreate, db: Session = Depends(get_db)):
    if len(body.password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")
    if db.query(User).filter_by(email=body.email.lower()).first():
        raise HTTPException(409, "Email already registered")
    u = User(email=body.email.lower(), password_hash=hash_pw(body.password))
    db.add(u); db.commit(); db.refresh(u)
    return Token(access_token=make_token(u.id))

@router.post("/login", response_model=Token)  # OAuth2 password flow (form: username=email)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = db.query(User).filter_by(email=form.username.lower()).first()
    if not u or not verify_pw(form.password, u.password_hash):
        raise HTTPException(401, "Incorrect email or password")
    return Token(access_token=make_token(u.id))

@router.get("/me")
def me(user: User = Depends(current_user)):
    return {"id": user.id, "email": user.email}
