"""
Challenge management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import verify_token
from app.crud import challenge as challenge_crud
from app.schemas.challenge import Challenge, ChallengeCreate, ChallengeUpdate, ChallengeProgress

router = APIRouter()

@router.get("/", response_model=List[Challenge])
async def get_challenges(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all challenges for current user"""
    return challenge_crud.get_user_challenges(db, user_id=int(current_user["user_id"]), skip=skip, limit=limit)

@router.post("/", response_model=Challenge, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    challenge: ChallengeCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new challenge"""
    return challenge_crud.create_challenge(db=db, challenge=challenge, user_id=int(current_user["user_id"]))

@router.get("/{challenge_id}", response_model=Challenge)
async def get_challenge(
    challenge_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get a specific challenge"""
    challenge = challenge_crud.get_challenge(db, challenge_id=challenge_id, user_id=int(current_user["user_id"]))
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    return challenge

@router.put("/{challenge_id}", response_model=Challenge)
async def update_challenge(
    challenge_id: int,
    challenge_update: ChallengeUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a challenge"""
    challenge = challenge_crud.update_challenge(db, challenge_id=challenge_id, challenge_update=challenge_update, user_id=int(current_user["user_id"]))
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    return challenge

@router.post("/{challenge_id}/progress", response_model=Challenge)
async def update_challenge_progress(
    challenge_id: int,
    progress: ChallengeProgress,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update challenge progress"""
    challenge = challenge_crud.update_challenge_progress(db, challenge_id=challenge_id, progress_value=progress.progress_value, user_id=int(current_user["user_id"]))
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    return challenge

@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge(
    challenge_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a challenge"""
    success = challenge_crud.delete_challenge(db, challenge_id=challenge_id, user_id=int(current_user["user_id"]))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
