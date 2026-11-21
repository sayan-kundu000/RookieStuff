import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.api.routes import router as api_router

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("rookiestuff")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for startup and shutdown events."""
    settings = get_settings()
    logger.info(f"Starting {settings.app_name} v{settings.version} [{settings.environment}]")
    yield
    logger.info(f"Shutting down {settings.app_name}")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()

    app = FastAPI(
        title="RookieStuff - Autonomous Code Review & Refactoring Agent",
        description=(
            "An autonomous, stateful code review and refactoring agent built with LangGraph, "
            "FastAPI, and GitHub API integration. Features isolated sandbox linting, "
            "persistent memory checkpoints, and Human-in-the-Loop (HITL) review gates."
        ),
        version=settings.version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    app.include_router(api_router)

    @app.get("/", tags=["Health"])
    async def root():
        """Root welcome endpoint providing service status and metadata."""
        return {
            "name": settings.app_name,
            "version": settings.version,
            "status": "online",
            "documentation": "/docs",
            "openapi": "/openapi.json",
            "endpoints": {
                "webhook": "POST /api/webhooks/github",
                "approve": "POST /api/reviews/{thread_id}/approve",
                "review_state": "GET /api/reviews/{thread_id}",
            },
        }

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "checkpointer": settings.checkpointer_type,
            "environment": settings.environment,
        }

    return app


app = create_app()
