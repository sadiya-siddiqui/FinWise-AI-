from sqlalchemy import String, ForeignKey, JSON, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class Insight(Base):
    """kind: 'budget' | 'subscription' | 'alert' | 'summary'"""
    __tablename__ = "insights"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    kind: Mapped[str] = mapped_column(String(30), index=True)
    title: Mapped[str] = mapped_column(String(200), default="")
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at = mapped_column(DateTime, server_default=func.now())
