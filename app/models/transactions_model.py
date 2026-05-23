from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func, String
from datetime import datetime

from app.core.base import Base

class PointTransaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    amount: Mapped[int] = mapped_column(
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        nullable=False,
        unique=False
    )

    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship("User", back_populates="transactions")