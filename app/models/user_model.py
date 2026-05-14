from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.core.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=True)

    hashed_password: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)

    full_name: Mapped[str] = mapped_column(unique=False, nullable=True)

    role: Mapped[str] = mapped_column(unique=False, nullable=True)