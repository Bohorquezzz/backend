"""
Reto management endpoints - Conectado con MySQL
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.core.security import verify_token
from app.crud import reto as reto_crud, user as user_crud
from app.schemas.reto import Reto, RetoCreate, RetoUpdate, RetoUsuario, RetoUsuarioCreate, RetoUsuarioUpdate

router = APIRouter()

@router.get("/", response_model=List[Reto])
async def get_retos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all available retos"""
    return reto_crud.get_retos(db, skip=skip, limit=limit)

@router.post("/", response_model=Reto, status_code=status.HTTP_201_CREATED)
async def create_reto(
    reto: RetoCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new reto (admin only)"""
    return reto_crud.create_reto(db=db, reto=reto)

@router.get("/{reto_id}", response_model=Reto)
async def get_reto(
    reto_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific reto"""
    reto = reto_crud.get_reto(db, reto_id=reto_id)
    if reto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reto not found"
        )
    return reto

@router.put("/{reto_id}", response_model=Reto)
async def update_reto(
    reto_id: int,
    reto_update: RetoUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a reto (admin only)"""
    reto = reto_crud.update_reto(db, reto_id=reto_id, reto_update=reto_update)
    if reto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reto not found"
        )
    return reto

@router.delete("/{reto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reto(
    reto_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a reto (admin only)"""
    success = reto_crud.delete_reto(db, reto_id=reto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reto not found"
        )

# Endpoints para RetoUsuario (progreso del usuario)
@router.get("/usuario/mis-retos", response_model=List[RetoUsuario])
async def get_mis_retos(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's retos"""
    return reto_crud.get_retos_usuario(db, user_id=int(current_user["user_id"]))

@router.post("/usuario/inscribirse", response_model=RetoUsuario, status_code=status.HTTP_201_CREATED)
async def inscribirse_reto(
    reto_usuario: RetoUsuarioCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Inscribirse a un reto"""
    # Verificar que el usuario existe
    user = user_crud.get_user(db, int(current_user["user_id"]))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Asignar el ID del usuario actual
    reto_usuario.id_usuario = int(current_user["user_id"])
    
    return reto_crud.create_reto_usuario(db=db, reto_usuario=reto_usuario)

@router.put("/usuario/progreso/{reto_usuario_id}", response_model=RetoUsuario)
async def update_progreso_reto(
    reto_usuario_id: int,
    progreso_update: RetoUsuarioUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update reto progress"""
    reto_usuario = reto_crud.update_reto_usuario(db, reto_usuario_id=reto_usuario_id, reto_usuario_update=progreso_update)
    if reto_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reto usuario not found"
        )
    return reto_usuario

@router.delete("/usuario/abandonar/{reto_usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def abandonar_reto(
    reto_usuario_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Abandonar un reto"""
    success = reto_crud.delete_reto_usuario(db, reto_usuario_id=reto_usuario_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reto usuario not found"
        )
