from sqlalchemy import String, ForeignKey, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    plaid_account_id: Mapped[str] = mapped_column(String(100), unique=True)
    item_id: Mapped[str] = mapped_column(String(100))
    access_token: Mapped[str] = mapped_column(String(200))  # encrypt at rest in production
    cursor: Mapped[str | None] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(String(200))
    institution: Mapped[str] = mapped_column(String(200), default="")
    type: Mapped[str] = mapped_column(String(50), default="")
    balance: Mapped[float] = mapped_column(Float, default=0)
    user = relationship("User", back_populates="accounts")
