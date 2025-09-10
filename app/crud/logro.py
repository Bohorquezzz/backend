"""
CRUD operations for Logro model - Conectado con MySQL
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.database import Logro, RetoUsuario, Reto, User
from app.schemas.logro import LogroCreate, LogroUpdate
from typing import List, Optional

def get_logro(db: Session, logro_id: int) -> Optional[Logro]:
    """Get logro by ID"""
    return db.query(Logro).filter(Logro.id == logro_id).first()

def get_logros(db: Session, skip: int = 0, limit: int = 100) -> List[Logro]:
    """Get all logros"""
    return db.query(Logro).offset(skip).limit(limit).all()

def get_logros_by_usuario(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Logro]:
    """Get logros by user ID"""
    return db.query(Logro).join(RetoUsuario).filter(
        RetoUsuario.id_usuario == user_id
    ).offset(skip).limit(limit).all()

def get_logros_by_reto_usuario(db: Session, reto_usuario_id: int) -> List[Logro]:
    """Get logros by reto_usuario ID"""
    return db.query(Logro).filter(Logro.id_reto_usuario == reto_usuario_id).all()

def create_logro(db: Session, logro: LogroCreate) -> Logro:
    """Create new logro"""
    db_logro = Logro(**logro.dict())
    db.add(db_logro)
    db.commit()
    db.refresh(db_logro)
    return db_logro

def update_logro(db: Session, logro_id: int, logro_update: LogroUpdate) -> Optional[Logro]:
    """Update logro"""
    db_logro = get_logro(db, logro_id)
    if not db_logro:
        return None
    
    update_data = logro_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_logro, field, value)
    
    db.commit()
    db.refresh(db_logro)
    return db_logro

def delete_logro(db: Session, logro_id: int) -> bool:
    """Delete logro"""
    db_logro = get_logro(db, logro_id)
    if not db_logro:
        return False
    
    db.delete(db_logro)
    db.commit()
    return True

def get_logros_with_details(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
    """Get logros with detailed information"""
    logros = db.query(
        Logro,
        RetoUsuario,
        Reto,
        User
    ).join(
        RetoUsuario, Logro.id_reto_usuario == RetoUsuario.id
    ).join(
        Reto, RetoUsuario.id_reto == Reto.id
    ).join(
        User, RetoUsuario.id_usuario == User.id
    ).filter(
        User.id == user_id
    ).offset(skip).limit(limit).all()
    
    result = []
    for logro, reto_usuario, reto, usuario in logros:
        result.append({
            "id": logro.id,
            "id_reto_usuario": logro.id_reto_usuario,
            "reto_usuario": {
                "id": reto_usuario.id,
                "progreso_reto": reto_usuario.progreso_reto
            },
            "reto": {
                "id": reto.id,
                "nombre_reto": reto.nombre_reto,
                "descripcion_reto": reto.descripcion_reto,
                "tipo": reto.tipo
            },
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "correo": usuario.correo
            }
        })
    
    return result

def create_logro_for_reto_completion(db: Session, reto_usuario_id: int) -> Optional[Logro]:
    """Create logro when a reto is completed (100% progress)"""
    # Verificar que el reto_usuario existe
    reto_usuario = db.query(RetoUsuario).filter(RetoUsuario.id == reto_usuario_id).first()
    if not reto_usuario:
        return None
    
    # Verificar que el progreso es 100%
    if reto_usuario.progreso_reto < 1.0:
        return None
    
    # Verificar que no existe ya un logro para este reto_usuario
    existing_logro = db.query(Logro).filter(Logro.id_reto_usuario == reto_usuario_id).first()
    if existing_logro:
        return existing_logro
    
    # Crear nuevo logro
    logro_data = LogroCreate(id_reto_usuario=reto_usuario_id)
    return create_logro(db, logro_data)
