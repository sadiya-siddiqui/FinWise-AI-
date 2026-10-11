from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PublicToken(BaseModel):
    public_token: str

class ChatIn(BaseModel):
    message: str

class BudgetIn(BaseModel):
    category: str
    limit: float
