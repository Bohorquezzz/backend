"""
Dependencies for dependency injection
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import verify_token
from app.crud import user as user_crud
from app.models.database import User

def get_current_user(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    user = user_crud.get_user(db, user_id=int(current_user["user_id"]))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
