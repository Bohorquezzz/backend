"""
Pydantic schemas for Challenge model
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.database import ChallengeType, ChallengeStatus

class ChallengeBase(BaseModel):
    title: str
    description: Optional[str] = None
    challenge_type: ChallengeType = ChallengeType.SIMPLE
    target_value: Optional[float] = None
    unit: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    checklist_items: Optional[List[Dict[str, Any]]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    challenge_type: Optional[ChallengeType] = None
    status: Optional[ChallengeStatus] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    unit: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    checklist_items: Optional[List[Dict[str, Any]]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ChallengeInDB(ChallengeBase):
    id: int
    user_id: int
    status: ChallengeStatus
    current_value: float
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Challenge(ChallengeInDB):
    pass

class ChallengeProgress(BaseModel):
    challenge_id: int
    progress_value: float
    notes: Optional[str] = None
