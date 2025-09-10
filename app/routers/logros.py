"""
Logro management endpoints - Conectado con MySQL
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import verify_token
from app.crud import logro as logro_crud
from app.schemas.logro import Logro, LogroCreate, LogroUpdate, LogroWithDetails

router = APIRouter()

@router.get("/", response_model=List[Logro])
async def get_logros(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all logros"""
    return logro_crud.get_logros(db, skip=skip, limit=limit)

@router.get("/usuario/mis-logros", response_model=List[LogroWithDetails])
async def get_mis_logros(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's logros with detailed information"""
    logros_data = logro_crud.get_logros_with_details(db, user_id=int(current_user["user_id"]))
    return logros_data

@router.get("/usuario", response_model=List[Logro])
async def get_logros_usuario(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's logros"""
    return logro_crud.get_logros_by_usuario(db, user_id=int(current_user["user_id"]))

@router.get("/reto-usuario/{reto_usuario_id}", response_model=List[Logro])
async def get_logros_by_reto_usuario(
    reto_usuario_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get logros by reto_usuario ID"""
    return logro_crud.get_logros_by_reto_usuario(db, reto_usuario_id=reto_usuario_id)

@router.post("/", response_model=Logro, status_code=status.HTTP_201_CREATED)
async def create_logro(
    logro: LogroCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new logro"""
    return logro_crud.create_logro(db=db, logro=logro)

@router.post("/completar-reto/{reto_usuario_id}", response_model=Logro, status_code=status.HTTP_201_CREATED)
async def crear_logro_por_completar_reto(
    reto_usuario_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create logro when a reto is completed"""
    logro = logro_crud.create_logro_for_reto_completion(db, reto_usuario_id=reto_usuario_id)
    if logro is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede crear logro. Verifica que el reto esté completado (100%) o que no exista ya un logro para este reto."
        )
    return logro

@router.get("/{logro_id}", response_model=Logro)
async def get_logro(
    logro_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific logro"""
    logro = logro_crud.get_logro(db, logro_id=logro_id)
    if logro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logro not found"
        )
    return logro

@router.put("/{logro_id}", response_model=Logro)
async def update_logro(
    logro_id: int,
    logro_update: LogroUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a logro"""
    logro = logro_crud.update_logro(db, logro_id=logro_id, logro_update=logro_update)
    if logro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logro not found"
        )
    return logro

@router.delete("/{logro_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_logro(
    logro_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a logro"""
    success = logro_crud.delete_logro(db, logro_id=logro_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logro not found"
        )
