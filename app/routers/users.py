"""
User management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import verify_token
from app.crud import user as user_crud
from app.schemas.user import User, UserUpdate

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Get current user information"""
    user = user_crud.get_user(db, user_id=int(current_user["user_id"]))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    user = user_crud.update_user(db, user_id=int(current_user["user_id"]), user_update=user_update)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete current user account"""
    success = user_crud.delete_user(db, user_id=int(current_user["user_id"]))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
