"""FastAPI application entry point for Zenith Pricing Engine."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.models.domain import Property

logger = logging.getLogger("zenith")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup and auto-seed if empty."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Auto-seed so the demo works out-of-the-box
    async with AsyncSessionLocal() as session:
        stmt = select(Property)
        res = await session.execute(stmt)
        if not res.scalars().first():
            logger.info("Empty DB detected — seeding demo data.")
            from scripts.seed_data import seed_database
            await seed_database()

    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Dynamic Hotel Pricing & Availability Engine API."
        " Real-time demand-based rate optimization,"
        " concurrency-safe bookings, and 30-day"
        " rate projections."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — use explicit origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        settings.CORS_ORIGINS if settings.CORS_ORIGINS
        else ["*"]
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Zenith Dynamic Hotel Pricing Engine API",
        "docs": "/docs",
        "health": "/health",
    }
