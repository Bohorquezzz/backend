"""
Pydantic schemas for Daily Challenge models
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class DailyChallengeBase(BaseModel):
    user_id: int
    reto_id: int
    challenge_date: date
    is_completed: bool = False
    progress_value: float = 0.0

class DailyChallengeCreate(DailyChallengeBase):
    pass

class DailyChallengeUpdate(BaseModel):
    is_completed: Optional[bool] = None
    progress_value: Optional[float] = None

class DailyChallengeInDB(DailyChallengeBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class DailyChallenge(DailyChallengeInDB):
    pass

class DailyChallengeWithReto(DailyChallenge):
    reto_nombre: Optional[str] = None
    reto_descripcion: Optional[str] = None
    reto_tipo: Optional[int] = None

class DailyChallengeTemplateBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    tipo: int
    categoria: Optional[str] = None
    dificultad: int = 1
    puntos_recompensa: int = 10
    is_active: bool = True

class DailyChallengeTemplateCreate(DailyChallengeTemplateBase):
    pass

class DailyChallengeTemplateUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[int] = None
    categoria: Optional[str] = None
    dificultad: Optional[int] = None
    puntos_recompensa: Optional[int] = None
    is_active: Optional[bool] = None

class DailyChallengeTemplateInDB(DailyChallengeTemplateBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class DailyChallengeTemplate(DailyChallengeTemplateInDB):
    pass

class DailyChallengeStats(BaseModel):
    total_challenges: int
    completed_challenges: int
    completion_rate: float
    current_streak: int
    longest_streak: int
    total_points: int
