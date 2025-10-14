"""
Service for handling category-specific challenge statistics
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import Reto, RetoUsuario, RetoCategoria

def get_category_stats(db: Session, user_id: int, categoria: RetoCategoria):
    """Get statistics for a specific category"""
    stats = {
        "categoria": categoria.value,
        "total_completados": 0,
        "retos_actuales": [],
        "mejor_racha": 0,
        "racha_actual": 0,
        "porcentaje_completado": 0.0
    }
    
    # Get completed challenges for this category
    completed_challenges = (
        db.query(RetoUsuario)
        .join(Reto)
        .filter(
            RetoUsuario.id_usuario == user_id,
            Reto.categoria == categoria,
            RetoUsuario.progreso_reto == 100.0
        )
        .all()
    )
    
    stats["total_completados"] = len(completed_challenges)
    
    # Get active challenges for this category
    today = datetime.utcnow().date()
    active_challenges = (
        db.query(Reto)
        .filter(
            Reto.categoria == categoria,
            Reto.activo == True,
            Reto.fecha_asignacion == today
        )
        .all()
    )
    
    for challenge in active_challenges:
        progress = db.query(RetoUsuario).filter(
            RetoUsuario.id_usuario == user_id,
            RetoUsuario.id_reto == challenge.id
        ).first()
        
        stats["retos_actuales"].append({
            "id": challenge.id,
            "nombre": challenge.nombre_reto,
            "descripcion": challenge.descripcion_reto,
            "progreso": progress.progreso_reto if progress else 0.0
        })
    
    # Calculate completion percentage
    total_assigned = (
        db.query(RetoUsuario)
        .join(Reto)
        .filter(
            RetoUsuario.id_usuario == user_id,
            Reto.categoria == categoria
        )
        .count()
    )
    
    if total_assigned > 0:
        stats["porcentaje_completado"] = (stats["total_completados"] / total_assigned) * 100
    
    return stats

def get_social_stats(db: Session, user_id: int):
    """Get statistics for social challenges"""
    return get_category_stats(db, user_id, RetoCategoria.SOCIAL)

def get_physical_stats(db: Session, user_id: int):
    """Get statistics for physical challenges"""
    return get_category_stats(db, user_id, RetoCategoria.FISICA)

def get_intellectual_stats(db: Session, user_id: int):
    """Get statistics for intellectual challenges"""
    return get_category_stats(db, user_id, RetoCategoria.INTELECTUAL)