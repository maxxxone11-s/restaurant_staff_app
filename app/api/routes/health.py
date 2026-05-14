from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health():
    try:
        return {"status": "ok"}
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }