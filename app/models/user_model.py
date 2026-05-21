from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from datetime import datetime

from app.core.roles import UserRole
from app.core.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    restaurant_name: Mapped[str] = mapped_column(nullable=False)

    position: Mapped[str] = mapped_column(nullable=False)

    points: Mapped[int] = mapped_column(default=0, nullable=False)

    hire_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[str] = mapped_column(unique=False, nullable=False)

    role: Mapped[str] = mapped_column(unique=False, nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    shifts = relationship("Shift", back_populates="user")