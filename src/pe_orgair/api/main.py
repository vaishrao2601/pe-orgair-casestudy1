"""FastAPI application with comprehensive middleware stack."""
from contextlib import asynccontextmanager
from typing import Callable
import time
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from pe_orgair.config.settings import settings
from pe_orgair.api.routes.v1 import router as v1_router
from pe_orgair.api.routes.v2 import router as v2_router
from pe_orgair.api.routes import health
from pe_orgair.observability.setup import setup_tracing, setup_logging

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with startup/shutdown."""
    # Startup
    logger.info("starting_application",
                app_name=settings.APP_NAME,
                version=settings.APP_VERSION,
                env=settings.APP_ENV)
    
    # Initialize connections, caches, etc.
    # await initialize_redis()
    # await validate_database()
    
    yield
    
    # Shutdown
    logger.info("shutting_down_application")

def create_app() -> FastAPI:
    """Application factory."""
    setup_logging()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.DEBUG else [],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request correlation middleware
    @app.middleware("http")
    async def add_correlation_id(request: Request, call_next: Callable) -> Response:
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
        
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time
        
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time"] = f"{duration:.4f}"
        
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
        )
        
        return response
    
    # Global error handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception("unhandled_exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={
                "type": "https://api.pe-orgair.example.com/errors/internal",
                "title": "Internal Server Error",
                "status": 500,
                "detail": str(exc) if settings.DEBUG else "An internal error occurred",
            },
        )
    
    # Tracing
    setup_tracing(app)
    
    # Routes
    app.include_router(health.router, tags=["Health"])
    app.include_router(v1_router, prefix=settings.API_V1_PREFIX)
    app.include_router(v2_router, prefix=settings.API_V2_PREFIX)
    
    return app

app = create_app()