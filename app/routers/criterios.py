"""
Criterio management endpoints - Conectado con MySQL
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import verify_token
from app.crud import criterio as criterio_crud
from app.schemas.criterio import Criterio, CriterioCreate, CriterioUpdate, CriterioReto, CriterioRetoCreate, CriterioRetoUpdate

router = APIRouter()

@router.get("/", response_model=List[Criterio])
async def get_criterios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all criterios"""
    return criterio_crud.get_criterios(db, skip=skip, limit=limit)

@router.get("/reto/{reto_id}", response_model=List[Criterio])
async def get_criterios_by_reto(
    reto_id: int,
    db: Session = Depends(get_db)
):
    """Get criterios by reto ID"""
    return criterio_crud.get_criterios_by_reto(db, reto_id=reto_id)

@router.post("/", response_model=Criterio, status_code=status.HTTP_201_CREATED)
async def create_criterio(
    criterio: CriterioCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new criterio (admin only)"""
    return criterio_crud.create_criterio(db=db, criterio=criterio)

@router.get("/{criterio_id}", response_model=Criterio)
async def get_criterio(
    criterio_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific criterio"""
    criterio = criterio_crud.get_criterio(db, criterio_id=criterio_id)
    if criterio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criterio not found"
        )
    return criterio

@router.put("/{criterio_id}", response_model=Criterio)
async def update_criterio(
    criterio_id: int,
    criterio_update: CriterioUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a criterio (admin only)"""
    criterio = criterio_crud.update_criterio(db, criterio_id=criterio_id, criterio_update=criterio_update)
    if criterio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criterio not found"
        )
    return criterio

@router.delete("/{criterio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_criterio(
    criterio_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a criterio (admin only)"""
    success = criterio_crud.delete_criterio(db, criterio_id=criterio_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criterio not found"
        )

# Endpoints para CriterioReto (progreso de criterios)
@router.get("/usuario/{reto_usuario_id}", response_model=List[CriterioReto])
async def get_criterios_reto_usuario(
    reto_usuario_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get criterios for a specific reto_usuario"""
    return criterio_crud.get_criterios_reto_by_usuario(db, reto_usuario_id=reto_usuario_id)

@router.post("/usuario/completar", response_model=CriterioReto, status_code=status.HTTP_201_CREATED)
async def completar_criterio(
    criterio_reto: CriterioRetoCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Completar un criterio"""
    return criterio_crud.create_criterio_reto(db=db, criterio_reto=criterio_reto)

@router.put("/usuario/{criterio_reto_id}/marcar-completado", response_model=CriterioReto)
async def marcar_criterio_completado(
    criterio_reto_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Marcar criterio como completado"""
    criterio_reto = criterio_crud.mark_criterio_completed(db, criterio_reto_id=criterio_reto_id)
    if criterio_reto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criterio reto not found"
        )
    return criterio_reto

@router.put("/usuario/{criterio_reto_id}", response_model=CriterioReto)
async def update_criterio_reto(
    criterio_reto_id: int,
    criterio_reto_update: CriterioRetoUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update criterio reto"""
    criterio_reto = criterio_crud.update_criterio_reto(db, criterio_reto_id=criterio_reto_id, criterio_reto_update=criterio_reto_update)
    if criterio_reto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Criterio reto not found"
        )
    return criterio_reto
