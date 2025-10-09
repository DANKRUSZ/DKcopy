from fastapi import APIRouter
from app.schemas.copy import CopyRequest, CopyResponse
from app.usecases.generate_copy import CopyGenerator

router = APIRouter(prefix="/copy", tags=["copy"])

@router.post("/generate", response_model=CopyResponse)
async def generate_copy(payload: CopyRequest) -> CopyResponse:
    generator = CopyGenerator()
    text, final_keywords = await generator.generate(
        payload,
        temperature=0.2,
        require_cta=bool(payload.cta),
    )
    return CopyResponse(
        generated_copy=text,
        keywords=final_keywords,
        tone_used=payload.tone_of_voice or "default",
        content_type=payload.content_type,
        metadata={"status": "ok"},
    )

