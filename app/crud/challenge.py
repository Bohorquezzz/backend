"""
CRUD operations for Challenge model
"""

from sqlalchemy.orm import Session
from app.models.database import Challenge, ChallengeStatus
from app.schemas.challenge import ChallengeCreate, ChallengeUpdate
from typing import List, Optional
import json

def get_challenge(db: Session, challenge_id: int, user_id: int) -> Optional[Challenge]:
    """Get challenge by ID for specific user"""
    return db.query(Challenge).filter(
        Challenge.id == challenge_id,
        Challenge.user_id == user_id
    ).first()

def get_user_challenges(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Challenge]:
    """Get all challenges for a user"""
    return db.query(Challenge).filter(
        Challenge.user_id == user_id
    ).offset(skip).limit(limit).all()

def create_challenge(db: Session, challenge: ChallengeCreate, user_id: int) -> Challenge:
    """Create new challenge"""
    challenge_data = challenge.dict()
    if challenge_data.get("checklist_items"):
        challenge_data["checklist_items"] = json.dumps(challenge_data["checklist_items"])
    
    db_challenge = Challenge(**challenge_data, user_id=user_id)
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def update_challenge(db: Session, challenge_id: int, challenge_update: ChallengeUpdate, user_id: int) -> Optional[Challenge]:
    """Update challenge"""
    db_challenge = get_challenge(db, challenge_id, user_id)
    if not db_challenge:
        return None
    
    update_data = challenge_update.dict(exclude_unset=True)
    if "checklist_items" in update_data and update_data["checklist_items"]:
        update_data["checklist_items"] = json.dumps(update_data["checklist_items"])
    
    for field, value in update_data.items():
        setattr(db_challenge, field, value)
    
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def update_challenge_progress(db: Session, challenge_id: int, progress_value: float, user_id: int) -> Optional[Challenge]:
    """Update challenge progress"""
    db_challenge = get_challenge(db, challenge_id, user_id)
    if not db_challenge:
        return None
    
    db_challenge.current_value = progress_value
    
    # Check if challenge is completed
    if db_challenge.target_value and progress_value >= db_challenge.target_value:
        db_challenge.status = ChallengeStatus.COMPLETED
    
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def delete_challenge(db: Session, challenge_id: int, user_id: int) -> bool:
    """Delete challenge"""
    db_challenge = get_challenge(db, challenge_id, user_id)
    if not db_challenge:
        return False
    
    db.delete(db_challenge)
    db.commit()
    return True
