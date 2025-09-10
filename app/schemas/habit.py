"""
Pydantic schemas for Habit model
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.database import HabitType

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    habit_type: HabitType = HabitType.DAILY
    target_value: float = 1.0
    unit: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    habit_type: Optional[HabitType] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None

class HabitInDB(HabitBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Habit(HabitInDB):
    pass
