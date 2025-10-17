"""
Progress tracking endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import date, datetime
from sqlalchemy import func, and_
import random

from app.database import get_db
from app.core.security import verify_token
from app.crud import progress as progress_crud
from app.schemas.progress import ProgressRecord, ProgressRecordCreate, ProgressRecordUpdate, ProgressStats
from app.services import progress_service
from app.schemas.reto import RetoUsuario
from app.schemas.challenge_progress import ChallengeProgressUpdate
from app.models.database import DailyChallenge, RetoCategoria
from app.schemas.daily_progress import DailyProgressStats
from sqlalchemy import func
from pydantic import BaseModel

class ChallengeStats(BaseModel):
    total_completed: int
    by_category: Dict[str, int]
    completion_rate: float

router = APIRouter()

@router.get("/", response_model=List[ProgressRecord])
async def get_progress_records(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all progress records for current user"""
    return progress_crud.get_user_progress_records(db, user_id=int(current_user["user_id"]), skip=skip, limit=limit)

@router.post("/", response_model=ProgressRecord, status_code=status.HTTP_201_CREATED)
async def create_progress_record(
    progress: ProgressRecordCreate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Create a new progress record"""
    return progress_crud.create_progress_record(db=db, progress=progress, user_id=int(current_user["user_id"]))

@router.get("/daily-progress", response_model=DailyProgressStats, responses={
    200: {"description": "Estadísticas diarias obtenidas exitosamente"},
    404: {"description": "No se encontraron retos para el día actual"},
    500: {"description": "Error interno del servidor"}
})
async def get_daily_progress(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get daily progress statistics and completion by category"""
    try:
        user_id = int(current_user["user_id"])
        today = date.today()

        # Obtener retos del día actual
        daily_challenges = db.query(DailyChallenge).join(
            DailyChallenge.reto
        ).filter(
            DailyChallenge.user_id == user_id,
            DailyChallenge.challenge_date == today,
            DailyChallenge.created_at >= today
        ).all()

        if not daily_challenges:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron retos asignados para el día actual"
            )

        # Contar total de retos y completados
        total_challenges = len(daily_challenges)
        completed_challenges = sum(1 for c in daily_challenges if c.is_completed)

        # Calcular porcentaje de completación
        daily_completion_percentage = (completed_challenges / total_challenges * 100) if total_challenges > 0 else 0.0

        # Inicializar contador por categoría con valores en minúscula
        completion_by_category = {
            "social": 0,
            "fisico": 0,
            "intelectual": 0
        }

        # Contar retos completados por categoría
        for challenge in daily_challenges:
            if challenge.is_completed and challenge.reto and challenge.reto.categoria:
                categoria = challenge.reto.categoria.value.upper()
                if categoria == "SOCIAL":
                    completion_by_category["social"] += 1
                elif categoria == "FISICA":
                    completion_by_category["fisico"] += 1
                elif categoria == "INTELECTUAL":
                    completion_by_category["intelectual"] += 1

        # Mantener todas las categorías en la respuesta, incluso con valor 0

        return {
            "daily_completion_percentage": round(daily_completion_percentage, 2),
            "total_daily_challenges": total_challenges,
            "completed_daily_challenges": completed_challenges,
            "completion_by_category": completion_by_category,
            "remaining_challenges": total_challenges - completed_challenges
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas diarias: {str(e)}"
        )

@router.get("/stats", response_model=ProgressStats, responses={
    200: {"description": "Estadísticas obtenidas exitosamente"},
    404: {"description": "No se encontraron datos para el usuario"},
    500: {"description": "Error interno del servidor"}
})
async def get_progress_stats(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user progress statistics"""
    try:
        user_id = int(current_user["user_id"])
        today = date.today()
        
        # Verificar si el usuario existe y tiene retos
        user_exists = db.query(DailyChallenge).filter(
            DailyChallenge.user_id == user_id
        ).first()
        
        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontraron retos para este usuario"
            )
        
        try:
            # Total retos del usuario
            total_challenges = db.query(DailyChallenge).filter(
                DailyChallenge.user_id == user_id
            ).count()
            
            # Retos completados totales
            completed_challenges = db.query(DailyChallenge).filter(
                DailyChallenge.user_id == user_id,
                DailyChallenge.is_completed == True
            ).count()
            
            # Tasa de completación (retos completados / retos totales * 100)
            total_habits = total_challenges
            completion_percentage = (completed_challenges / total_challenges * 100) if total_challenges > 0 else 0.0
            
            # Retos completados hoy
            completed_today = db.query(DailyChallenge).filter(
                DailyChallenge.user_id == user_id,
                DailyChallenge.is_completed == True,
                DailyChallenge.completed_at >= today
            ).count()
            
            # Obtener todos los retos completados ordenados por fecha
            completed_challenges_list = db.query(DailyChallenge).filter(
                DailyChallenge.user_id == user_id,
                DailyChallenge.is_completed == True
            ).order_by(DailyChallenge.completed_at).all()
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al consultar la base de datos: {str(e)}"
            )
            
        try:
            # Calcular current_streak y longest_streak
            current_streak = 0
            longest_streak = 0
            temp_streak = 0
            last_date = None
            
            for challenge in completed_challenges_list:
                if not challenge.completed_at:
                    continue
                    
                current_date = challenge.completed_at.date()
                
                if last_date is None:
                    temp_streak = 1
                elif (current_date - last_date).days == 1:
                    temp_streak += 1
                elif (current_date - last_date).days > 1:
                    if temp_streak > longest_streak:
                        longest_streak = temp_streak
                    temp_streak = 1
                    
                last_date = current_date
            
            # Actualizar longest_streak una última vez
            if temp_streak > longest_streak:
                longest_streak = temp_streak
            
            # Si el último reto completado fue ayer o hoy, mantener la racha actual
            if last_date and (today - last_date).days <= 1:
                current_streak = temp_streak
            else:
                current_streak = 0
                
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al calcular las rachas: {str(e)}"
            )
            
        try:
            # Calcular tiempo promedio de completación (en horas)
            total_time = 0
            completed_count = 0
            
            for challenge in completed_challenges_list:
                if challenge.completed_at and challenge.created_at:
                    if challenge.completed_at < challenge.created_at:
                        raise ValueError("Fecha de completado anterior a fecha de creación")
                    time_diff = challenge.completed_at - challenge.created_at
                    total_time += time_diff.total_seconds() / 3600  # convertir a horas
                    completed_count += 1
            
            completion_rate = total_time / completed_count if completed_count > 0 else 0.0
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en la integridad de los datos: {str(ve)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al calcular el tiempo promedio: {str(e)}"
            )
        
        return {
            "total_habits": total_habits,
            "completed_today": completed_today,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "completion_rate": round(completion_rate, 2),  # Redondear a 2 decimales
            "total_challenges": total_challenges,
            "completed_challenges": completed_challenges
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )

@router.get("/challenges/stats", response_model=ChallengeStats)
async def get_challenge_stats(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's challenge completion statistics"""
    return progress_service.get_user_challenge_stats(db, current_user["id"])

@router.post("/challenges/{reto_id}/complete", response_model=RetoUsuario)
async def complete_challenge(
    reto_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Mark a challenge as complete"""
    return progress_service.mark_challenge_complete(db, current_user["id"], reto_id)

@router.get("/challenges/active")
async def get_active_challenges(
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get user's currently active challenges with progress"""
    return progress_service.get_user_active_challenges(db, current_user["id"])

@router.get("/habit/{habit_id}", response_model=List[ProgressRecord])
async def get_habit_progress(
    habit_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get progress records for a specific habit"""
    return progress_crud.get_habit_progress(db, habit_id=habit_id, user_id=int(current_user["user_id"]), start_date=start_date, end_date=end_date)

@router.get("/challenge/{challenge_id}", response_model=List[ProgressRecord])
async def get_challenge_progress(
    challenge_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get progress records for a specific challenge"""
    return progress_crud.get_challenge_progress(db, challenge_id=challenge_id, user_id=int(current_user["user_id"]))

@router.post("/challenge/{challenge_id}")
async def update_challenge_progress(
    challenge_id: int,
    progress: ChallengeProgressUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update progress value for a daily challenge using the daily_challenges table id"""
    try:
        # Buscar directamente por el id de daily_challenges
        daily_challenge = db.query(DailyChallenge).filter(
            DailyChallenge.id == challenge_id,
            DailyChallenge.user_id == int(current_user["user_id"])
        ).first()
        
        if not daily_challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró el reto diario con ID {challenge_id}"
            )

        # Si el reto ya está completado, no permitir modificaciones
        if daily_challenge.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede modificar un reto que ya está completado"
            )
        
        # Actualizar el progreso (el valor ya está validado entre 0 y 100)
        daily_challenge.progress_value = progress.value
        
        # Si se marca explícitamente como completado o el progreso es 100%
        if progress.is_completed or progress.value >= 100.0:
            daily_challenge.is_completed = True
            daily_challenge.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(daily_challenge)
        
        return {
            "id": daily_challenge.id,
            "reto_id": daily_challenge.reto_id,
            "progress_value": daily_challenge.progress_value,
            "is_completed": daily_challenge.is_completed,
            "completed_at": daily_challenge.completed_at,
            "challenge_date": daily_challenge.challenge_date,
            "message": f"Progreso actualizado correctamente a {progress.value}%"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el progreso: {str(e)}"
        )

@router.get("/{record_id}", response_model=ProgressRecord)
async def get_progress_record(
    record_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get a specific progress record"""
    record = progress_crud.get_progress_record(db, record_id=record_id, user_id=int(current_user["user_id"]))
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress record not found"
        )
    return record

@router.put("/{record_id}", response_model=ProgressRecord)
async def update_progress_record(
    record_id: int,
    progress_update: ProgressRecordUpdate,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Update a progress record"""
    record = progress_crud.update_progress_record(db, record_id=record_id, progress_update=progress_update, user_id=int(current_user["user_id"]))
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress record not found"
        )
    return record

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_progress_record(
    record_id: int,
    current_user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Delete a progress record"""
    success = progress_crud.delete_progress_record(db, record_id=record_id, user_id=int(current_user["user_id"]))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress record not found"
        )


