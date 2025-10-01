"""
Router for challenge rotation system
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.services.reto_service import get_daily_challenges, rotate_challenges
from app.schemas.reto import Reto
from app.core.security import verify_token

router = APIRouter()

@router.get("/daily", response_model=List[Reto])
async def get_todays_challenges(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Get today's challenges - one from each category"""
    return get_daily_challenges(db)

@router.post("/rotate")
async def force_challenge_rotation(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_token)
):
    """Force a rotation of challenges (admin only)"""
    rotate_challenges(db)
    return {"message": "Challenges rotated successfully"}