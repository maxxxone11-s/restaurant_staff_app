from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_roles
from app.schemas.reward_schema import RewardCreate, RewardResponse
from app.models.reward_model import Reward

router = APIRouter(prefix="/rewards", tags=["rewards"])

@router.post("/", response_model=RewardResponse)
async def create_reward(
    data_reward: RewardCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles(["admin", "manager"])),
):
    reward = {
        "title": data_reward.title,
        "description": data_reward.description,
        "cost_points": data_reward.cost_points
    }
    try:
        db.add(reward)
        await db.commit()
        await db.refresh(reward)
        return reward
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Не корректные данные для создания награды")
    
@router.get("/", response_model=list[RewardResponse])
async def get_reward(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Reward)
        .where(Reward.is_active.is_(True))
    )

    result = result.scalars().all()

    if result:
        return result
    
    raise HTTPException(status_code=404, detail="Наград в данный момент нету")