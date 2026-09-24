from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from app.core.config import settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.models.domain import Property
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize DB tables automatically if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Auto-seed database if empty so demo works out-of-the-box on Render
    async with AsyncSessionLocal() as session:
        stmt = select(Property)
        res = await session.execute(stmt)
        first_prop = res.scalars().first()
        if not first_prop:
            from scripts.seed_data import seed_database
            await seed_database()

    yield
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Resume-ready Dynamic Hotel Pricing & Availability Engine API. Simulates real-time demand-based rate optimization, concurrency-safe room bookings, and 30-day rate projections.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }

@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Welcome to Zenith Dynamic Hotel Pricing Engine API",
        "docs": "/docs",
        "health": "/health"
    }
