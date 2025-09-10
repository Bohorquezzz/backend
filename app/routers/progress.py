"""
Progress tracking endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.core.security import verify_token
from app.crud import progress as progress_crud
from app.schemas.progress import ProgressRecord, ProgressRecordCreate, ProgressRecordUpdate, ProgressStats

router = APIRouter()

@router.get("/", response_model=List[ProgressRecord])
async def get_progress_records(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all progress records for current user"""
    return progress_crud.get_user_progress_records(db, user_id=int(current_user["user_id"]), skip=skip, limit=limit)

@router.post("/", response_model=ProgressRecord, status_code=status.HTTP_201_CREATED)
async def create_progress_record(
    progress: ProgressRecordCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new progress record"""
    return progress_crud.create_progress_record(db=db, progress=progress, user_id=int(current_user["user_id"]))

@router.get("/stats", response_model=ProgressStats)
async def get_progress_stats(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user progress statistics"""
    return progress_crud.get_user_stats(db, user_id=int(current_user["user_id"]))

@router.get("/habit/{habit_id}", response_model=List[ProgressRecord])
async def get_habit_progress(
    habit_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get progress records for a specific habit"""
    return progress_crud.get_habit_progress(db, habit_id=habit_id, user_id=int(current_user["user_id"]), start_date=start_date, end_date=end_date)

@router.get("/challenge/{challenge_id}", response_model=List[ProgressRecord])
async def get_challenge_progress(
    challenge_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get progress records for a specific challenge"""
    return progress_crud.get_challenge_progress(db, challenge_id=challenge_id, user_id=int(current_user["user_id"]))

@router.get("/{record_id}", response_model=ProgressRecord)
async def get_progress_record(
    record_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get a specific progress record"""
    record = progress_crud.get_progress_record(db, record_id=record_id, user_id=int(current_user["user_id"]))
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress record not found"
        )
    return record

@router.put("/{record_id}", response_model=ProgressRecord)
async def update_progress_record(
    record_id: int,
    progress_update: ProgressRecordUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a progress record"""
    record = progress_crud.update_progress_record(db, record_id=record_id, progress_update=progress_update, user_id=int(current_user["user_id"]))
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress record not found"
        )
    return record

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_progress_record(
    record_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a progress record"""
    success = progress_crud.delete_progress_record(db, record_id=record_id, user_id=int(current_user["user_id"]))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress record not found"
        )
