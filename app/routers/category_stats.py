"""
Router for category-specific challenge statistics
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from app.database import get_db
from app.core.security import verify_token
from app.services import category_stats_service
from pydantic import BaseModel

router = APIRouter()

class CategoryStats(BaseModel):
    categoria: str
    total_completados: int
    retos_actuales: List[Dict]
    mejor_racha: int
    racha_actual: int
    porcentaje_completado: float

@router.get("/social", response_model=CategoryStats)
async def get_social_stats(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get statistics for social challenges"""
    return category_stats_service.get_social_stats(db, current_user["id"])

@router.get("/fisica", response_model=CategoryStats)
async def get_physical_stats(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get statistics for physical challenges"""
    return category_stats_service.get_physical_stats(db, current_user["id"])

@router.get("/intelectual", response_model=CategoryStats)
async def get_intellectual_stats(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get statistics for intellectual challenges"""
    return category_stats_service.get_intellectual_stats(db, current_user["id"])