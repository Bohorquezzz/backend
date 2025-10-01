"""
UpDaily Backend API
FastAPI application for the UpDaily mobile app
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.database import init_db
from app.routers import auth, users, habits, challenges, progress, retos, criterios, logros, daily_retos, category_stats
from app.core.config import settings

# Security scheme
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

# Create FastAPI app
app = FastAPI(
    title="UpDaily API",
    description="Backend API for UpDaily - Daily Habits and Challenges Tracker",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
    expose_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(habits.router, prefix="/api/v1/habits", tags=["Habits"])
app.include_router(challenges.router, prefix="/api/v1/challenges", tags=["Challenges"])
app.include_router(category_stats.router, prefix="/api/v1/stats/category", tags=["Category Statistics"])
app.include_router(daily_retos.router, prefix="/api/v1/daily-retos", tags=["Daily Challenges"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])
app.include_router(retos.router, prefix="/api/v1/retos", tags=["Retos"])
app.include_router(criterios.router, prefix="/api/v1/criterios", tags=["Criterios"])
app.include_router(logros.router, prefix="/api/v1/logros", tags=["Logros"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to UpDaily API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
