"""
CRUD operations for Reto model - Conectado con MySQL
"""

from sqlalchemy.orm import Session
from app.models.database import Reto, RetoUsuario
from app.schemas.reto import RetoCreate, RetoUpdate, RetoUsuarioCreate, RetoUsuarioUpdate
from typing import List, Optional

# CRUD para Retos
def get_reto(db: Session, reto_id: int) -> Optional[Reto]:
    """Get reto by ID"""
    return db.query(Reto).filter(Reto.id == reto_id).first()

def get_retos(db: Session, skip: int = 0, limit: int = 100) -> List[Reto]:
    """Get all retos"""
    return db.query(Reto).offset(skip).limit(limit).all()

def create_reto(db: Session, reto: RetoCreate) -> Reto:
    """Create new reto"""
    db_reto = Reto(**reto.dict())
    db.add(db_reto)
    db.commit()
    db.refresh(db_reto)
    return db_reto

def update_reto(db: Session, reto_id: int, reto_update: RetoUpdate) -> Optional[Reto]:
    """Update reto"""
    db_reto = get_reto(db, reto_id)
    if not db_reto:
        return None
    
    update_data = reto_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reto, field, value)
    
    db.commit()
    db.refresh(db_reto)
    return db_reto

def delete_reto(db: Session, reto_id: int) -> bool:
    """Delete reto"""
    db_reto = get_reto(db, reto_id)
    if not db_reto:
        return False
    
    db.delete(db_reto)
    db.commit()
    return True

# CRUD para RetoUsuario (progreso de usuario en retos)
def get_reto_usuario(db: Session, reto_usuario_id: int) -> Optional[RetoUsuario]:
    """Get reto_usuario by ID"""
    return db.query(RetoUsuario).filter(RetoUsuario.id == reto_usuario_id).first()

def get_retos_usuario(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[RetoUsuario]:
    """Get all retos for a user"""
    return db.query(RetoUsuario).filter(RetoUsuario.id_usuario == user_id).offset(skip).limit(limit).all()

def create_reto_usuario(db: Session, reto_usuario: RetoUsuarioCreate) -> RetoUsuario:
    """Create new reto_usuario"""
    db_reto_usuario = RetoUsuario(**reto_usuario.dict())
    db.add(db_reto_usuario)
    db.commit()
    db.refresh(db_reto_usuario)
    return db_reto_usuario

def update_reto_usuario(db: Session, reto_usuario_id: int, reto_usuario_update: RetoUsuarioUpdate) -> Optional[RetoUsuario]:
    """Update reto_usuario progress"""
    db_reto_usuario = get_reto_usuario(db, reto_usuario_id)
    if not db_reto_usuario:
        return None
    
    update_data = reto_usuario_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reto_usuario, field, value)
    
    db.commit()
    db.refresh(db_reto_usuario)
    return db_reto_usuario

def delete_reto_usuario(db: Session, reto_usuario_id: int) -> bool:
    """Delete reto_usuario"""
    db_reto_usuario = get_reto_usuario(db, reto_usuario_id)
    if not db_reto_usuario:
        return False
    
    db.delete(db_reto_usuario)
    db.commit()
    return True
