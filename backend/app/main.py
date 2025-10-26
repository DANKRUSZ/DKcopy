from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import settings
from .routes import router
from .logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"🚀 {settings.APP_NAME} started")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Using fake LLM: {settings.USE_FAKE_LLM}")
    yield
    # Shutdown (if needed)
    logger.info("Shutting down...")

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"], #settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/health", tags=["meta"])
    async def health():
        return {"status": "ok", "env": settings.APP_ENV}
    
    app.include_router(router)
    return app

app = create_app()
