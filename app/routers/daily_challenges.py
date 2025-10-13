"""
Daily Challenge management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.core.security import verify_token
from app.crud import daily_challenge as daily_challenge_crud
from app.schemas.daily_challenge import (
    DailyChallenge, DailyChallengeCreate, DailyChallengeUpdate,
    DailyChallengeTemplate, DailyChallengeTemplateCreate, DailyChallengeTemplateUpdate,
    DailyChallengeWithReto, DailyChallengeStats
)

router = APIRouter()

# Endpoints para DailyChallenge
@router.get("/mis-retos", response_model=List[DailyChallengeWithReto])
async def get_my_daily_challenges(
    challenge_date: Optional[date] = Query(None, description="Fecha específica (por defecto: hoy)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's daily challenges"""
    if challenge_date is None:
        challenge_date = date.today()
    
    challenges = daily_challenge_crud.get_user_daily_challenges(
        db, user_id=int(current_user["user_id"]), 
        challenge_date=challenge_date, skip=skip, limit=limit
    )
    
    # Enriquecer con información del reto
    enriched_challenges = []
    for challenge in challenges:
        challenge_dict = challenge.__dict__.copy()
        if challenge.reto:
            challenge_dict.update({
                "reto_nombre": challenge.reto.nombre_reto,
                "reto_descripcion": challenge.reto.descripcion_reto,
                "reto_tipo": challenge.reto.tipo
            })
        enriched_challenges.append(DailyChallengeWithReto(**challenge_dict))
    
    return enriched_challenges

@router.get("/hoy", response_model=List[DailyChallengeWithReto])
async def get_today_challenges(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get today's challenges for the user"""
    challenges = daily_challenge_crud.get_today_challenges(db, int(current_user["user_id"]))
    
    # Enriquecer con información del reto
    enriched_challenges = []
    for challenge in challenges:
        challenge_dict = challenge.__dict__.copy()
        if challenge.reto:
            challenge_dict.update({
                "reto_nombre": challenge.reto.nombre_reto,
                "reto_descripcion": challenge.reto.descripcion_reto,
                "reto_tipo": challenge.reto.tipo
            })
        enriched_challenges.append(DailyChallengeWithReto(**challenge_dict))
    
    return enriched_challenges

@router.post("/completar/{challenge_id}", response_model=DailyChallenge)
async def complete_challenge(
    challenge_id: int,
    progress_value: float = Query(1.0, ge=0.0, le=1.0, description="Valor de progreso (0.0-1.0)"),
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Mark a daily challenge as completed"""
    # Verificar que el reto pertenece al usuario
    challenge = daily_challenge_crud.get_daily_challenge(db, challenge_id)
    if not challenge or challenge.user_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    if challenge.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Challenge already completed"
        )
    
    completed_challenge = daily_challenge_crud.complete_daily_challenge(
        db, challenge_id, progress_value
    )
    
    if not completed_challenge:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete challenge"
        )
    
    return completed_challenge

@router.put("/{challenge_id}", response_model=DailyChallenge)
async def update_challenge(
    challenge_id: int,
    challenge_update: DailyChallengeUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a daily challenge"""
    # Verificar que el reto pertenece al usuario
    challenge = daily_challenge_crud.get_daily_challenge(db, challenge_id)
    if not challenge or challenge.user_id != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    updated_challenge = daily_challenge_crud.update_daily_challenge(
        db, challenge_id, challenge_update
    )
    
    if not updated_challenge:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update challenge"
        )
    
    return updated_challenge

@router.get("/estadisticas", response_model=DailyChallengeStats)
async def get_challenge_stats(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's challenge statistics"""
    stats = daily_challenge_crud.get_user_challenge_stats(db, int(current_user["user_id"]))
    return DailyChallengeStats(**stats)

# Endpoints para DailyChallengeTemplate (admin)
@router.get("/plantillas", response_model=List[DailyChallengeTemplate])
async def get_challenge_templates(
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    dificultad: Optional[int] = Query(None, ge=1, le=3, description="Filtrar por dificultad (1-3)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get daily challenge templates"""
    templates = daily_challenge_crud.get_daily_challenge_templates(
        db, skip=skip, limit=limit, categoria=categoria, dificultad=dificultad
    )
    return templates

@router.post("/plantillas", response_model=DailyChallengeTemplate, status_code=status.HTTP_201_CREATED)
async def create_challenge_template(
    template: DailyChallengeTemplateCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new daily challenge template (admin only)"""
    # Aquí podrías agregar verificación de permisos de admin
    return daily_challenge_crud.create_daily_challenge_template(db, template)

@router.put("/plantillas/{template_id}", response_model=DailyChallengeTemplate)
async def update_challenge_template(
    template_id: int,
    template_update: DailyChallengeTemplateUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a daily challenge template (admin only)"""
    template = daily_challenge_crud.update_daily_challenge_template(
        db, template_id, template_update
    )
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return template

@router.delete("/plantillas/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge_template(
    template_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a daily challenge template (admin only)"""
    success = daily_challenge_crud.delete_daily_challenge_template(db, template_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )

# Endpoint para generar retos manualmente (admin)
@router.post("/generar-retos", status_code=status.HTTP_201_CREATED)
async def generate_daily_challenges(
    challenge_date: Optional[date] = Query(None, description="Fecha para generar retos (por defecto: hoy)"),
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Generate daily challenges for all users (admin only)"""
    if challenge_date is None:
        challenge_date = date.today()
    
    total_challenges = daily_challenge_crud.generate_daily_challenges_for_all_users(
        db, challenge_date
    )
    
    return {
        "message": f"Generated {total_challenges} daily challenges for {challenge_date}",
        "date": challenge_date,
        "total_challenges": total_challenges
    }
