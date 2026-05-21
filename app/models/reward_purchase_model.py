from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.base import Base

class RewardPurchase(Base):
    __tablename__ = "reward_purchase"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    reward_id: Mapped[int] = mapped_column(ForeignKey("reward.id"), nullable=False)

    cost_points: Mapped[int] = mapped_column(nullable=False)

    purchased_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    reward = relationship("Reward", back_populates="reward_purchase")
    user = relationship("User", back_populates="reward_purchase")