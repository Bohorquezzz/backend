"""
Service for handling user challenge progress and completion
"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import Reto, RetoUsuario, User, Logro, RetoCategoria

def get_user_challenge_stats(db: Session, user_id: int):
    """Get user's challenge completion statistics"""
    stats = {
        "total_completed": 0,
        "by_category": {
            "SOCIAL": 0,
            "FISICA": 0,
            "INTELECTUAL": 0
        },
        "completion_rate": 0.0
    }
    
    # Get all completed challenges for the user
    completed_challenges = (
        db.query(RetoUsuario)
        .join(Reto)
        .filter(
            RetoUsuario.id_usuario == user_id,
            RetoUsuario.progreso_reto == 100.0
        )
        .all()
    )
    
    # Count total completed challenges
    stats["total_completed"] = len(completed_challenges)
    
    # Count by category
    for challenge in completed_challenges:
        categoria = challenge.reto.categoria.value
        stats["by_category"][categoria] += 1
    
    # Calculate completion rate
    total_assigned = db.query(RetoUsuario).filter(
        RetoUsuario.id_usuario == user_id
    ).count()
    
    if total_assigned > 0:
        stats["completion_rate"] = (stats["total_completed"] / total_assigned) * 100
    
    return stats

def mark_challenge_complete(db: Session, user_id: int, reto_id: int):
    """Mark a challenge as complete for a user"""
    # Find or create reto_usuario record
    reto_usuario = db.query(RetoUsuario).filter(
        RetoUsuario.id_usuario == user_id,
        RetoUsuario.id_reto == reto_id
    ).first()
    
    if not reto_usuario:
        reto_usuario = RetoUsuario(
            id_usuario=user_id,
            id_reto=reto_id,
            progreso_reto=100.0
        )
        db.add(reto_usuario)
    else:
        reto_usuario.progreso_reto = 100.0
    
    # Create logro record
    logro = Logro(
        id_reto_usuario=reto_usuario.id,
        id_usuario=user_id
    )
    db.add(logro)
    
    db.commit()
    return reto_usuario

def get_user_active_challenges(db: Session, user_id: int):
    """Get user's currently active challenges"""
    today = datetime.utcnow().date()
    
    active_challenges = (
        db.query(Reto)
        .filter(
            Reto.activo == True,
            Reto.fecha_asignacion == today
        )
        .all()
    )
    
    result = []
    for challenge in active_challenges:
        # Check if user has already started/completed this challenge
        progress = db.query(RetoUsuario).filter(
            RetoUsuario.id_usuario == user_id,
            RetoUsuario.id_reto == challenge.id
        ).first()
        
        result.append({
            "reto": challenge,
            "progreso": progress.progreso_reto if progress else 0.0
        })
    
    return result