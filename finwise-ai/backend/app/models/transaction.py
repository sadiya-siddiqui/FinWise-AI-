from sqlalchemy import String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    plaid_txn_id: Mapped[str] = mapped_column(String(100), unique=True)
    date = mapped_column(Date, index=True)
    name: Mapped[str] = mapped_column(String(300))
    merchant: Mapped[str] = mapped_column(String(200), default="")
    amount: Mapped[float] = mapped_column(Float)  # positive = spending (Plaid convention)
    category: Mapped[str] = mapped_column(String(80), default="Uncategorized")
    pending: Mapped[bool] = mapped_column(Boolean, default=False)
