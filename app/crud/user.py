"""
CRUD operations for User model - Conectado con MySQL
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.database import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Optional

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, correo: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.correo == correo).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    hashed_password = get_password_hash(user.clave)
    db_user = User(
        nombre=user.nombre,
        correo=user.correo,
        clave=hashed_password,
        fecha_nacimiento=user.fecha_nacimiento,
        telefono=user.telefono
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    if "clave" in update_data:
        update_data["clave"] = get_password_hash(update_data["clave"])
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, correo: str, clave: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, correo)
    if not user:
        return None
    if not verify_password(clave, user.clave):
        return None
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete user"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True