from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, func

from app.core.base import Base

class Shift(Base):
    __tablename__ = "shifts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    open_shift: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True
    )

    closed_shift: Mapped[datetime| None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    revenue: Mapped[int] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship("User", back_populates="shifts")