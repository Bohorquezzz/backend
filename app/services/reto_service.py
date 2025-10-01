"""
Service for handling daily challenge rotation
"""

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import Reto, RetoCategoria
import random

def get_daily_challenges(db: Session):
    """Get one random challenge for each category for today"""
    today = datetime.utcnow().date()
    
    daily_challenges = []
    for categoria in RetoCategoria:
        # Get all active challenges for this category
        available_challenges = db.query(Reto).filter(
            Reto.categoria == categoria,
            Reto.activo == True
        ).all()
        
        if available_challenges:
            # Select a random challenge
            daily_challenge = random.choice(available_challenges)
            
            # Update fecha_asignacion
            daily_challenge.fecha_asignacion = today
            daily_challenges.append(daily_challenge)
    
    db.commit()
    return daily_challenges

def rotate_challenges(db: Session):
    """Rotate active challenges"""
    today = datetime.utcnow().date()
    
    # Get yesterday's challenges and deactivate them
    yesterday_challenges = db.query(Reto).filter(
        Reto.fecha_asignacion < today,
        Reto.activo == True
    ).all()
    
    for challenge in yesterday_challenges:
        challenge.activo = False
    
    # Activate new random challenges
    for categoria in RetoCategoria:
        inactive_challenges = db.query(Reto).filter(
            Reto.categoria == categoria,
            Reto.activo == False
        ).all()
        
        if inactive_challenges:
            new_active = random.choice(inactive_challenges)
            new_active.activo = True
            new_active.fecha_asignacion = today
    
    db.commit()