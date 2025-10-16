"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from app.schemas.auth import UserLogin, Token, RefreshToken

from app.database import get_db
from app.core.config import settings
from app.core.security import create_access_token, verify_token
from app.crud import user as user_crud
from app.schemas.user import UserCreate, User, Token
from app.schemas.auth import UserLogin

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    db_user = user_crud.get_user_by_email(db, correo=user.correo)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    return user_crud.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access and refresh tokens"""
    user = user_crud.authenticate_user(db, user_credentials.correo, user_credentials.clave)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires,
        is_refresh_token=False
    )
    
    # Crear refresh token
    refresh_token = create_access_token(
        data={"sub": str(user.id)},
        is_refresh_token=True
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(token: RefreshToken, db: Session = Depends(get_db)):
    """Get new access token using refresh token"""
    try:
        # Verificar el refresh token
        payload = jwt.decode(token.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # Verificar que sea un refresh token
        if not payload.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Verificar que el usuario existe
        user = user_crud.get_user(db, int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Crear nuevo access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=access_token_expires,
            is_refresh_token=False
        )
        
        # Crear nuevo refresh token
        refresh_token = create_access_token(
            data={"sub": user_id},
            is_refresh_token=True
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2 compatible token endpoint"""
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

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
