"""
CRUD operations for Daily Challenge models
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from app.models.database import DailyChallenge, DailyChallengeTemplate, Reto, User
from app.schemas.daily_challenge import (
    DailyChallengeCreate, DailyChallengeUpdate, 
    DailyChallengeTemplateCreate, DailyChallengeTemplateUpdate
)
from typing import List, Optional
from datetime import date, datetime, timedelta
import random

# CRUD para DailyChallenge
def get_daily_challenge(db: Session, challenge_id: int) -> Optional[DailyChallenge]:
    """Get daily challenge by ID"""
    return db.query(DailyChallenge).filter(DailyChallenge.id == challenge_id).first()

def get_user_daily_challenges(
    db: Session, 
    user_id: int, 
    challenge_date: Optional[date] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[DailyChallenge]:
    """Get user's daily challenges"""
    query = db.query(DailyChallenge).filter(DailyChallenge.user_id == user_id)
    
    if challenge_date:
        query = query.filter(DailyChallenge.challenge_date == challenge_date)
    
    return query.order_by(desc(DailyChallenge.challenge_date)).offset(skip).limit(limit).all()

def get_today_challenges(db: Session, user_id: int) -> List[DailyChallenge]:
    """Get today's challenges for a user"""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    return (db.query(DailyChallenge)
            .filter(DailyChallenge.user_id == user_id)
            .filter(DailyChallenge.created_at.between(today_start, today_end))
            .all())

def create_daily_challenge(db: Session, challenge: DailyChallengeCreate) -> DailyChallenge:
    """Create new daily challenge"""
    db_challenge = DailyChallenge(**challenge.dict())
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def update_daily_challenge(
    db: Session, 
    challenge_id: int, 
    challenge_update: DailyChallengeUpdate
) -> Optional[DailyChallenge]:
    """Update daily challenge"""
    db_challenge = get_daily_challenge(db, challenge_id)
    if not db_challenge:
        return None
    
    update_data = challenge_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_challenge, field, value)
    
    # Si se marca como completado, actualizar completed_at
    if update_data.get('is_completed') and not db_challenge.completed_at:
        db_challenge.completed_at = datetime.now()
    
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def complete_daily_challenge(db: Session, challenge_id: int, progress_value: float = 1.0) -> Optional[DailyChallenge]:
    """Mark daily challenge as completed"""
    challenge = update_daily_challenge(
        db, 
        challenge_id, 
        DailyChallengeUpdate(is_completed=True, progress_value=progress_value)
    )
    
    # Enviar notificación de completado
    if challenge:
        from app.services.notifications import notification_service
        challenge_name = challenge.reto.nombre_reto if challenge.reto else "Reto"
        notification_service.send_challenge_completion_notification(
            challenge.user_id, challenge_name
        )
        
        # Verificar si hay racha para notificar
        stats = get_user_challenge_stats(db, challenge.user_id)
        if stats['current_streak'] > 0:
            notification_service.send_streak_notification(
                challenge.user_id, stats['current_streak']
            )
    
    return challenge

def delete_daily_challenge(db: Session, challenge_id: int) -> bool:
    """Delete daily challenge"""
    db_challenge = get_daily_challenge(db, challenge_id)
    if not db_challenge:
        return False
    
    db.delete(db_challenge)
    db.commit()
    return True

# CRUD para DailyChallengeTemplate
def get_daily_challenge_template(db: Session, template_id: int) -> Optional[DailyChallengeTemplate]:
    """Get daily challenge template by ID"""
    return db.query(DailyChallengeTemplate).filter(DailyChallengeTemplate.id == template_id).first()

def get_daily_challenge_templates(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    categoria: Optional[str] = None,
    dificultad: Optional[int] = None,
    is_active: bool = True
) -> List[DailyChallengeTemplate]:
    """Get daily challenge templates"""
    query = db.query(DailyChallengeTemplate).filter(DailyChallengeTemplate.is_active == is_active)
    
    if categoria:
        query = query.filter(DailyChallengeTemplate.categoria == categoria)
    
    if dificultad:
        query = query.filter(DailyChallengeTemplate.dificultad == dificultad)
    
    return query.offset(skip).limit(limit).all()

def create_daily_challenge_template(db: Session, template: DailyChallengeTemplateCreate) -> DailyChallengeTemplate:
    """Create new daily challenge template"""
    db_template = DailyChallengeTemplate(**template.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def update_daily_challenge_template(
    db: Session, 
    template_id: int, 
    template_update: DailyChallengeTemplateUpdate
) -> Optional[DailyChallengeTemplate]:
    """Update daily challenge template"""
    db_template = get_daily_challenge_template(db, template_id)
    if not db_template:
        return None
    
    update_data = template_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_template, field, value)
    
    db.commit()
    db.refresh(db_template)
    return db_template

def delete_daily_challenge_template(db: Session, template_id: int) -> bool:
    """Delete daily challenge template"""
    db_template = get_daily_challenge_template(db, template_id)
    if not db_template:
        return False
    
    db.delete(db_template)
    db.commit()
    return True

# Lógica de rotación de retos diarios
def generate_daily_challenges_for_user(db: Session, user_id: int, challenge_date: date) -> List[DailyChallenge]:
    """Generate daily challenges for a user on a specific date"""
    # Verificar si ya existen retos para esta fecha
    existing_challenges = get_user_daily_challenges(db, user_id, challenge_date)
    if existing_challenges:
        return existing_challenges
    
    # Obtener plantillas activas
    templates = get_daily_challenge_templates(db, is_active=True)
    if not templates:
        return []
    
    # Seleccionar 3-5 retos aleatorios (puedes ajustar este número)
    num_challenges = min(5, len(templates))
    selected_templates = random.sample(templates, num_challenges)
    
    challenges = []
    for template in selected_templates:
        # Crear un reto basado en la plantilla
        reto_data = {
            "nombre_reto": template.nombre,
            "descripcion_reto": template.descripcion,
            "tipo": template.tipo
        }
        
        # Crear el reto en la tabla reto
        reto = Reto(**reto_data)
        db.add(reto)
        db.flush()  # Para obtener el ID
        
        # Crear el reto diario
        challenge_data = DailyChallengeCreate(
            user_id=user_id,
            reto_id=reto.id,
            challenge_date=challenge_date
        )
        
        challenge = create_daily_challenge(db, challenge_data)
        challenges.append(challenge)
    
    return challenges

def generate_daily_challenges_for_all_users(db: Session, challenge_date: date) -> int:
    """Generate daily challenges for all active users"""
    # Obtener todos los usuarios activos
    users = db.query(User).all()
    
    total_challenges = 0
    for user in users:
        challenges = generate_daily_challenges_for_user(db, user.id, challenge_date)
        total_challenges += len(challenges)
    
    return total_challenges

def get_user_challenge_stats(db: Session, user_id: int) -> dict:
    """Get user's challenge statistics"""
    # Total de retos
    total_challenges = db.query(DailyChallenge).filter(DailyChallenge.user_id == user_id).count()
    
    # Retos completados
    completed_challenges = db.query(DailyChallenge).filter(
        and_(
            DailyChallenge.user_id == user_id,
            DailyChallenge.is_completed == True
        )
    ).count()
    
    # Tasa de completación
    completion_rate = (completed_challenges / total_challenges * 100) if total_challenges > 0 else 0
    
    # Racha actual (días consecutivos completados)
    current_streak = 0
    today = date.today()
    
    # Verificar días consecutivos hacia atrás
    for i in range(30):  # Máximo 30 días hacia atrás
        check_date = today - timedelta(days=i)
        day_challenges = get_user_daily_challenges(db, user_id, check_date)
        
        if not day_challenges:
            break
            
        all_completed = all(challenge.is_completed for challenge in day_challenges)
        if all_completed:
            current_streak += 1
        else:
            break
    
    # Puntos totales (suma de puntos de retos completados)
    total_points = db.query(func.sum(DailyChallengeTemplate.puntos_recompensa)).join(
        DailyChallenge, DailyChallenge.reto_id == DailyChallengeTemplate.id
    ).filter(
        and_(
            DailyChallenge.user_id == user_id,
            DailyChallenge.is_completed == True
        )
    ).scalar() or 0
    
    return {
        "total_challenges": total_challenges,
        "completed_challenges": completed_challenges,
        "completion_rate": round(completion_rate, 2),
        "current_streak": current_streak,
        "total_points": total_points
    }
