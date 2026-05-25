from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, require_roles, get_current_user
from app.schemas.reward_schema import RewardCreate, RewardResponse, RewardBuyResponse
from app.schemas.reward_purchase_schema import RewardPurchaseHistoryResponse
from app.models.reward_model import Reward
from app.models.reward_purchase_model import RewardPurchase
from app.utilities.rewards import get_spend_transaction, get_purchase, create_reward
from app.core.roles import UserRole

router = APIRouter(prefix="/rewards", tags=["rewards"])

@router.post("/", response_model=RewardResponse)
async def create_reward(
    data_reward: RewardCreate,
    db: AsyncSession = Depends(get_db),
    allow_roles = Depends(require_roles([UserRole.ADMIN, UserRole.MANAGER])),
):
    reward = create_reward(data_reward)
    
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

@router.post("/{reward_id}/buy", response_model=RewardBuyResponse)
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
        purchase = get_purchase(current_user.id, result.id, result.cost_points)
        balance = current_user.points

        transaction = get_spend_transaction(current_user.id, result.cost_points, result.title)
        try:
            db.add(purchase)
            db.add(transaction)
            await db.commit()
            await db.refresh(current_user)
            await db.refresh(purchase)
            return {"reward": result.title, "price": result.cost_points, "balance": balance}
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=400, detail=f"Детали: {str(e)}")

    raise HTTPException(status_code=400, detail="На балансе недостаточно средств")

@router.get("/my", response_model=list[RewardPurchaseHistoryResponse])
async def get_list_purchase(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Reward.title, RewardPurchase.cost_points, RewardPurchase.purchased_at)
        .join(Reward, RewardPurchase.reward_id == Reward.id)
        .where(RewardPurchase.user_id == current_user.id)
    )

    result = result.mappings().all()

    return result


