"""
Schemas for daily progress statistics
"""
from pydantic import BaseModel
from typing import Dict

class DailyProgressStats(BaseModel):
    daily_completion_percentage: float
    total_daily_challenges: int
    completed_daily_challenges: int
    completion_by_category: Dict[str, int]  # {"SOCIAL": 2, "FISICA": 1, etc}
    remaining_challenges: int