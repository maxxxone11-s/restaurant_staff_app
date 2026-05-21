from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_roles, get_current_user
from app.schemas.reward_schema import RewardCreate, RewardResponse
from app.models.reward_model import Reward

router = APIRouter(prefix="/rewards", tags=["rewards"])

@router.post("/", response_model=RewardResponse)
async def create_reward(
    data_reward: RewardCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles(["admin", "manager"])),
):
    reward = Reward(
        title=data_reward.title,
        description=data_reward.description,
        cost_points=data_reward.cost_points
    )
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

@router.post("/{reward_id}/buy")
async def buy_reward(
    reward_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):  
    try:
        result = await db.execute(
            select(Reward)
            .where(Reward.id == reward_id)
            .where(Reward.is_active.is_(True))
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Товара в данный момент нету")

    result = result.scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404, detail="Товар не найден")


    if current_user.points >= result.cost_points:
        current_user.points -= result.cost_points
        balance = current_user.points
        await db.commit()
        await db.refresh(current_user)
        return {"reward": result.title, "price": result.cost_points, "balance": balance}

    raise HTTPException(status_code=400, detail="На балансе недостаточно средств")