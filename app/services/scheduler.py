"""
Scheduler service for daily challenge automation
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import daily_challenge as daily_challenge_crud
from datetime import date
import logging

logger = logging.getLogger(__name__)

class DailyChallengeScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self._setup_jobs()
    
    def _setup_jobs(self):
        """Setup scheduled jobs"""
        # Generar retos diarios todos los días a las 6:00 AM
        self.scheduler.add_job(
            self.generate_daily_challenges,
            CronTrigger(hour=6, minute=0),
            id='generate_daily_challenges',
            name='Generate Daily Challenges',
            replace_existing=True
        )
        
        # Limpiar retos antiguos todos los domingos a las 2:00 AM
        self.scheduler.add_job(
            self.cleanup_old_challenges,
            CronTrigger(day_of_week=6, hour=2, minute=0),  # Domingo
            id='cleanup_old_challenges',
            name='Cleanup Old Challenges',
            replace_existing=True
        )
        
        logger.info("Daily challenge scheduler jobs configured")
    
    async def generate_daily_challenges(self):
        """Generate daily challenges for all users"""
        try:
            logger.info("Starting daily challenge generation...")
            
            # Obtener sesión de base de datos
            db = next(get_db())
            
            # Generar retos para hoy
            today = date.today()
            total_challenges = daily_challenge_crud.generate_daily_challenges_for_all_users(
                db, today
            )
            
            logger.info(f"Generated {total_challenges} daily challenges for {today}")
            
            # Enviar notificaciones a usuarios
            from app.services.notifications import notification_service
            from app.models.database import User
            
            users = db.query(User).all()
            for user in users:
                notification_service.send_daily_challenges_notification(user.id)
            
        except Exception as e:
            logger.error(f"Error generating daily challenges: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()
    
    async def cleanup_old_challenges(self):
        """Clean up old completed challenges (older than 30 days)"""
        try:
            logger.info("Starting cleanup of old challenges...")
            
            # Obtener sesión de base de datos
            db = next(get_db())
            
            # Limpiar retos completados de hace más de 30 días
            from datetime import timedelta
            cutoff_date = date.today() - timedelta(days=30)
            
            # Aquí implementarías la lógica de limpieza
            # Por ahora solo logueamos
            logger.info(f"Cleanup would remove challenges older than {cutoff_date}")
            
        except Exception as e:
            logger.error(f"Error cleaning up old challenges: {str(e)}")
        finally:
            if 'db' in locals():
                db.close()
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Daily challenge scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Daily challenge scheduler stopped")
    
    def get_job_status(self):
        """Get status of scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        return jobs

# Instancia global del scheduler
daily_challenge_scheduler = DailyChallengeScheduler()
