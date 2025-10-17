"""
Challenge management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from datetime import date, datetime
import random

from app.database import get_db
from app.core.security import verify_token
from app.crud import challenge as challenge_crud
from app.schemas.challenge import Challenge, ChallengeCreate, ChallengeUpdate, ChallengeProgress
from app.models.database import DailyChallenge, RetoCategoria, Reto
from datetime import date

router = APIRouter()

@router.get("/", response_model=List[Challenge])
async def get_challenges(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all challenges for current user"""
    return challenge_crud.get_user_challenges(db, user_id=int(current_user["user_id"]), skip=skip, limit=limit)

@router.post("/", response_model=Challenge, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    challenge: ChallengeCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new challenge"""
    return challenge_crud.create_challenge(db=db, challenge=challenge, user_id=int(current_user["user_id"]))

@router.get("/{challenge_id}", response_model=Challenge)
async def get_challenge(
    challenge_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get a specific challenge"""
    challenge = challenge_crud.get_challenge(db, challenge_id=challenge_id, user_id=int(current_user["user_id"]))
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    return challenge

@router.put("/{challenge_id}", response_model=Challenge)
async def update_challenge(
    challenge_id: int,
    challenge_update: ChallengeUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a challenge"""
    challenge = challenge_crud.update_challenge(db, challenge_id=challenge_id, challenge_update=challenge_update, user_id=int(current_user["user_id"]))
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    return challenge

@router.post("/{challenge_id}/progress", response_model=Challenge)
async def update_challenge_progress(
    challenge_id: int,
    progress: ChallengeProgress,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update challenge progress"""
    challenge = challenge_crud.update_challenge_progress(db, challenge_id=challenge_id, progress_value=progress.progress_value, user_id=int(current_user["user_id"]))
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    return challenge

@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge(
    challenge_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a challenge"""
    success = challenge_crud.delete_challenge(db, challenge_id=challenge_id, user_id=int(current_user["user_id"]))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )

@router.post("/generate-daily", status_code=status.HTTP_201_CREATED)
async def generate_daily_challenges(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Generate 6 new daily challenges for the user (2 from each category)"""
    try:
        user_id = int(current_user["user_id"])
        today = date.today()

        # Eliminar solo los retos creados hoy
        db.query(DailyChallenge).filter(
            DailyChallenge.user_id == user_id,
            DailyChallenge.challenge_date == today,
            func.date(DailyChallenge.created_at) == today
        ).delete(synchronize_session=False)

        # Obtener 2 retos aleatorios de cada categoría
        new_challenges = []
        for categoria in [RetoCategoria.SOCIAL, RetoCategoria.FISICA, RetoCategoria.INTELECTUAL]:
            # Obtener retos activos de la categoría actual que no hayan sido asignados hoy
            available_retos = db.query(Reto).filter(
                Reto.categoria == categoria,
                Reto.activo == True
            ).all()

            if len(available_retos) < 2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No hay suficientes retos activos en la categoría {categoria.value}"
                )

            # Seleccionar 2 retos aleatorios de esta categoría
            selected_retos = random.sample(available_retos, 2)
            new_challenges.extend(selected_retos)

        # Crear los DailyChallenge para cada reto seleccionado
        created_challenges = []
        for reto in new_challenges:
            daily_challenge = DailyChallenge(
                user_id=user_id,
                reto_id=reto.id,
                challenge_date=today,
                is_completed=False,
                progress_value=0.0
            )
            db.add(daily_challenge)
            created_challenges.append({
                "reto_id": reto.id,
                "nombre_reto": reto.nombre_reto,
                "categoria": reto.categoria.value,
                "descripcion_reto": reto.descripcion_reto
            })

        db.commit()

        return {
            "message": "Retos diarios generados exitosamente",
            "fecha": today,
            "total_retos": len(created_challenges),
            "retos": created_challenges
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar los retos diarios: {str(e)}"
        )
