"""
Schemas for challenge progress
"""
from pydantic import BaseModel, validator
from typing import Optional

class ChallengeProgressUpdate(BaseModel):
    value: float
    is_completed: Optional[bool] = None

    @validator('value')
    def validate_value(cls, v):
        # Aseguramos que el valor esté entre 0 y 100
        return float(max(0.0, min(100.0, v)))