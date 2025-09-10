"""
CRUD operations for Habit model
"""

from sqlalchemy.orm import Session
from app.models.database import Habit
from app.schemas.habit import HabitCreate, HabitUpdate
from typing import List, Optional

def get_habit(db: Session, habit_id: int, user_id: int) -> Optional[Habit]:
    """Get habit by ID for specific user"""
    return db.query(Habit).filter(
        Habit.id == habit_id,
        Habit.user_id == user_id
    ).first()

def get_user_habits(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Habit]:
    """Get all habits for a user"""
    return db.query(Habit).filter(
        Habit.user_id == user_id,
        Habit.is_active == True
    ).offset(skip).limit(limit).all()

def create_habit(db: Session, habit: HabitCreate, user_id: int) -> Habit:
    """Create new habit"""
    db_habit = Habit(**habit.dict(), user_id=user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def update_habit(db: Session, habit_id: int, habit_update: HabitUpdate, user_id: int) -> Optional[Habit]:
    """Update habit"""
    db_habit = get_habit(db, habit_id, user_id)
    if not db_habit:
        return None
    
    update_data = habit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_habit, field, value)
    
    db.commit()
    db.refresh(db_habit)
    return db_habit

def delete_habit(db: Session, habit_id: int, user_id: int) -> bool:
    """Delete habit (soft delete by setting is_active to False)"""
    db_habit = get_habit(db, habit_id, user_id)
    if not db_habit:
        return False
    
    db_habit.is_active = False
    db.commit()
    return True
