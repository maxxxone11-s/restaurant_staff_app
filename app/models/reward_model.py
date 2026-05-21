from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func, DateTime, String

from app.core.base import Base

class Reward(Base):
    __tablename__ = "reward"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(55), nullable=False, unique=False)

    description: Mapped[str] = mapped_column(String(255), nullable=False, unique=False)

    cost_points: Mapped[int] = mapped_column(nullable=False, unique=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )