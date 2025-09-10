"""
CRUD operations for Progress model
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.database import ProgressRecord, Habit, Challenge
from app.schemas.progress import ProgressRecordCreate, ProgressRecordUpdate
from typing import List, Optional
from datetime import datetime, date

def get_progress_record(db: Session, record_id: int, user_id: int) -> Optional[ProgressRecord]:
    """Get progress record by ID for specific user"""
    return db.query(ProgressRecord).filter(
        ProgressRecord.id == record_id,
        ProgressRecord.user_id == user_id
    ).first()

def get_user_progress_records(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[ProgressRecord]:
    """Get all progress records for a user"""
    return db.query(ProgressRecord).filter(
        ProgressRecord.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_habit_progress(db: Session, habit_id: int, user_id: int, start_date: date = None, end_date: date = None) -> List[ProgressRecord]:
    """Get progress records for a specific habit"""
    query = db.query(ProgressRecord).filter(
        ProgressRecord.habit_id == habit_id,
        ProgressRecord.user_id == user_id
    )
    
    if start_date:
        query = query.filter(ProgressRecord.date >= start_date)
    if end_date:
        query = query.filter(ProgressRecord.date <= end_date)
    
    return query.order_by(ProgressRecord.date.desc()).all()

def get_challenge_progress(db: Session, challenge_id: int, user_id: int) -> List[ProgressRecord]:
    """Get progress records for a specific challenge"""
    return db.query(ProgressRecord).filter(
        ProgressRecord.challenge_id == challenge_id,
        ProgressRecord.user_id == user_id
    ).order_by(ProgressRecord.date.desc()).all()

def create_progress_record(db: Session, progress: ProgressRecordCreate, user_id: int) -> ProgressRecord:
    """Create new progress record"""
    db_progress = ProgressRecord(**progress.dict(), user_id=user_id)
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def update_progress_record(db: Session, record_id: int, progress_update: ProgressRecordUpdate, user_id: int) -> Optional[ProgressRecord]:
    """Update progress record"""
    db_progress = get_progress_record(db, record_id, user_id)
    if not db_progress:
        return None
    
    update_data = progress_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_progress, field, value)
    
    db.commit()
    db.refresh(db_progress)
    return db_progress

def delete_progress_record(db: Session, record_id: int, user_id: int) -> bool:
    """Delete progress record"""
    db_progress = get_progress_record(db, record_id, user_id)
    if not db_progress:
        return False
    
    db.delete(db_progress)
    db.commit()
    return True

def get_user_stats(db: Session, user_id: int) -> dict:
    """Get user progress statistics"""
    # Total habits
    total_habits = db.query(Habit).filter(
        Habit.user_id == user_id,
        Habit.is_active == True
    ).count()
    
    # Completed today
    today = date.today()
    completed_today = db.query(ProgressRecord).filter(
        ProgressRecord.user_id == user_id,
        func.date(ProgressRecord.date) == today
    ).count()
    
    # Total challenges
    total_challenges = db.query(Challenge).filter(
        Challenge.user_id == user_id
    ).count()
    
    # Completed challenges
    completed_challenges = db.query(Challenge).filter(
        Challenge.user_id == user_id,
        Challenge.status == "completed"
    ).count()
    
    # Calculate completion rate
    completion_rate = (completed_today / total_habits * 100) if total_habits > 0 else 0
    
    return {
        "total_habits": total_habits,
        "completed_today": completed_today,
        "current_streak": 0,  # TODO: Implement streak calculation
        "longest_streak": 0,  # TODO: Implement streak calculation
        "completion_rate": round(completion_rate, 2),
        "total_challenges": total_challenges,
        "completed_challenges": completed_challenges
    }
