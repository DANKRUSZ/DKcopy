from fastapi import APIRouter

router = APIRouter(prefix="/copy", tags=["copy"])

@router.get("/ping")
async def copy_ping():
    return {"ok": True, "service": "copy", "message": "pong"}