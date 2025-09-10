"""
Habit management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import verify_token
from app.crud import habit as habit_crud
from app.schemas.habit import Habit, HabitCreate, HabitUpdate

router = APIRouter()

@router.get("/", response_model=List[Habit])
async def get_habits(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all habits for current user"""
    return habit_crud.get_user_habits(db, user_id=int(current_user["user_id"]), skip=skip, limit=limit)

@router.post("/", response_model=Habit, status_code=status.HTTP_201_CREATED)
async def create_habit(
    habit: HabitCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new habit"""
    return habit_crud.create_habit(db=db, habit=habit, user_id=int(current_user["user_id"]))

@router.get("/{habit_id}", response_model=Habit)
async def get_habit(
    habit_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get a specific habit"""
    habit = habit_crud.get_habit(db, habit_id=habit_id, user_id=int(current_user["user_id"]))
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )
    return habit

@router.put("/{habit_id}", response_model=Habit)
async def update_habit(
    habit_id: int,
    habit_update: HabitUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a habit"""
    habit = habit_crud.update_habit(db, habit_id=habit_id, habit_update=habit_update, user_id=int(current_user["user_id"]))
    if habit is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )
    return habit

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a habit"""
    success = habit_crud.delete_habit(db, habit_id=habit_id, user_id=int(current_user["user_id"]))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )
