from fastapi import APIRouter
from app.schemas.copy import CopyRequest, CopyResponse

router = APIRouter(prefix="/copy", tags=["copy"])

@router.post("/generate", response_model=CopyResponse)
async def generate_copy(payload: CopyRequest) -> CopyResponse:
    # Stubbed response to satisfy tests; you’ll replace with service logic later.
    return CopyResponse(
        generated_copy="stub output",
        keywords=payload.keywords or ["default"],
        tone_used=payload.tone_of_voice or "default",
        content_type=payload.content_type,
        metadata={"status": "stub"}
    )
