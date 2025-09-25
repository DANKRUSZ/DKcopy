from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routes_copy import router as copy_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    @app.get("/health", tags=["_meta"])
    async def health():
        return {"status": "ok", "env": settings.APP_ENV}
    
    app.include_router(copy_router, prefix=settings.API_V1_PREFIX)

    return app

app = create_app()