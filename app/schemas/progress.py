"""
Pydantic schemas for Progress model
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProgressRecordBase(BaseModel):
    date: datetime
    value: float = 1.0
    notes: Optional[str] = None

class ProgressRecordCreate(ProgressRecordBase):
    habit_id: Optional[int] = None
    challenge_id: Optional[int] = None

class ProgressRecordUpdate(BaseModel):
    value: Optional[float] = None
    notes: Optional[str] = None

class ProgressRecordInDB(ProgressRecordBase):
    id: int
    user_id: int
    habit_id: Optional[int] = None
    challenge_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProgressRecord(ProgressRecordInDB):
    pass

class ProgressStats(BaseModel):
    total_habits: int
    completed_today: int
    current_streak: int
    longest_streak: int
    completion_rate: float
    total_challenges: int
    completed_challenges: int
