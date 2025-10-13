"""
Notification service for daily challenges
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.database import User, DailyChallenge
from app.crud import daily_challenge as daily_challenge_crud
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.db = SessionLocal()
    
    def send_daily_challenges_notification(self, user_id: int):
        """Send notification about new daily challenges"""
        try:
            # Obtener retos de hoy para el usuario
            today_challenges = daily_challenge_crud.get_today_challenges(self.db, user_id)
            
            if not today_challenges:
                logger.info(f"No challenges found for user {user_id} today")
                return
            
            # Aquí implementarías el envío real de notificaciones
            # Por ejemplo: push notifications, email, SMS, etc.
            logger.info(f"Sending daily challenges notification to user {user_id}")
            logger.info(f"User has {len(today_challenges)} challenges for today")
            
            # Ejemplo de notificación
            notification_message = f"¡Tienes {len(today_challenges)} nuevos retos para hoy! ¡Vamos a completarlos!"
            logger.info(f"Notification: {notification_message}")
            
        except Exception as e:
            logger.error(f"Error sending notification to user {user_id}: {str(e)}")
    
    def send_challenge_completion_notification(self, user_id: int, challenge_name: str):
        """Send notification when user completes a challenge"""
        try:
            # Obtener estadísticas del usuario
            stats = daily_challenge_crud.get_user_challenge_stats(self.db, user_id)
            
            # Mensaje de felicitación
            if stats['current_streak'] > 1:
                message = f"¡Excelente! Completaste '{challenge_name}'. ¡Llevas {stats['current_streak']} días seguidos!"
            else:
                message = f"¡Bien hecho! Completaste '{challenge_name}'. ¡Sigue así!"
            
            logger.info(f"Completion notification for user {user_id}: {message}")
            
        except Exception as e:
            logger.error(f"Error sending completion notification: {str(e)}")
    
    def send_streak_notification(self, user_id: int, streak_days: int):
        """Send notification for streak milestones"""
        try:
            if streak_days in [3, 7, 14, 30, 50, 100]:  # Milestones importantes
                message = f"🎉 ¡Increíble! Llevas {streak_days} días seguidos completando retos. ¡Eres imparable!"
                logger.info(f"Streak notification for user {user_id}: {message}")
            
        except Exception as e:
            logger.error(f"Error sending streak notification: {str(e)}")
    
    def send_reminder_notification(self, user_id: int):
        """Send reminder for incomplete challenges"""
        try:
            # Obtener retos incompletos de hoy
            today_challenges = daily_challenge_crud.get_today_challenges(self.db, user_id)
            incomplete_challenges = [c for c in today_challenges if not c.is_completed]
            
            if incomplete_challenges:
                message = f"¡No olvides completar tus {len(incomplete_challenges)} retos de hoy!"
                logger.info(f"Reminder notification for user {user_id}: {message}")
            
        except Exception as e:
            logger.error(f"Error sending reminder notification: {str(e)}")
    
    def send_weekly_summary(self, user_id: int):
        """Send weekly summary of user's progress"""
        try:
            # Obtener estadísticas de la semana
            stats = daily_challenge_crud.get_user_challenge_stats(self.db, user_id)
            
            message = f"📊 Resumen semanal: Completaste {stats['completed_challenges']} de {stats['total_challenges']} retos ({stats['completion_rate']}%)"
            logger.info(f"Weekly summary for user {user_id}: {message}")
            
        except Exception as e:
            logger.error(f"Error sending weekly summary: {str(e)}")
    
    def close(self):
        """Close database connection"""
        if self.db:
            self.db.close()

# Instancia global del servicio de notificaciones
notification_service = NotificationService()
