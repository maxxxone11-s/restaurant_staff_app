from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.core.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    full_name: Mapped[str] = mapped_column(unique=False, nullable=False)

    role: Mapped[str] = mapped_column(unique=False, nullable=False)