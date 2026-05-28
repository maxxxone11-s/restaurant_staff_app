from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.api.deps import get_db, require_roles, get_current_user
from app.schemas.reward_schema import RewardCreate, RewardResponse, RewardBuyResponse
from app.models.reward_model import Reward
from app.models.reward_purchase_model import RewardPurchase
from app.utilities.rewards import get_spend_transaction, get_purchase, build_reward
from app.core.redis import redis_client
from app.schemas.reward_purchase_schema import RewardPurchaseHistoryResponse
from app.core.roles import UserRole
from app.core.redis import redis_client

router = APIRouter(prefix="/rewards", tags=["rewards"])

@router.post("/", response_model=RewardResponse)
async def create_reward(
    data_reward: RewardCreate,
    db: AsyncSession = Depends(get_db),
    allow_roles = Depends(require_roles([UserRole.ADMIN, UserRole.MANAGER])),
):
    reward = build_reward(data_reward)
    
    try:
        db.add(reward)
        await db.commit()
        await db.refresh(reward)
        await redis_client.delete(
            "rewards_active"
        )
        return reward
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Не корректные данные для создания награды")
    
@router.get("/", response_model=list[RewardResponse])
async def get_reward(
    db: AsyncSession = Depends(get_db)
):
    cached_data = await redis_client.get("rewards_active")

    if cached_data:
        return json.loads(cached_data)

    result = await db.execute(
        select(Reward)
        .where(Reward.is_active.is_(True))
    )

    result = result.scalars().all()
    data = [
        {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "cost_points": item.cost_points,
            "is_active": item.is_active,
            "created_at": item.created_at.isoformat()
        }
        for item in result
    ]

    if data:
        await redis_client.set(
        "rewards_active",
        json.dumps(data),
        ex=3600
        )
        return data
    
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
            await redis_client.delete(
                "leader_points",
                f"user_points:{current_user.id}",
                f"user_purchase:{current_user.id}"
            )
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
    cached_data = await redis_client.get(f"user_purchase:{current_user.id}")

    if cached_data:
        return json.loads(cached_data)

    result = await db.execute(
        select(Reward.title, RewardPurchase.cost_points, RewardPurchase.purchased_at)
        .join(Reward, RewardPurchase.reward_id == Reward.id)
        .where(RewardPurchase.user_id == current_user.id)
    )

    result = result.mappings().all()
    data = [
        {
            "title": item["title"],
            "cost_points": item["cost_points"],
            "purchased_at": item["purchased_at"].isoformat()
        }
        for item in result
    ]

    if data:
        await redis_client.set(
            f"user_purchase:{current_user.id}",
            json.dumps(data),
            ex=18000
        )
        return data

    raise HTTPException(status_code=404, detail="Вы еще не совершали покупки")


