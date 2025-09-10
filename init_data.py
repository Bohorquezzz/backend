"""
Script para inicializar la base de datos con datos de ejemplo
"""

import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.crud import user as user_crud, habit as habit_crud, challenge as challenge_crud
from app.schemas.user import UserCreate
from app.schemas.habit import HabitCreate
from app.schemas.challenge import ChallengeCreate
from app.models.database import HabitType, ChallengeType
from datetime import datetime, timedelta

def create_sample_data():
    """Crear datos de ejemplo para la aplicación"""
    db = SessionLocal()
    
    try:
        # Crear usuario de ejemplo
        user_data = UserCreate(
            email="demo@updaily.com",
            username="demo_user",
            full_name="Usuario Demo",
            password="demo123"
        )
        
        # Verificar si el usuario ya existe
        existing_user = user_crud.get_user_by_email(db, user_data.email)
        if existing_user:
            print("Usuario demo ya existe")
            user = existing_user
        else:
            user = user_crud.create_user(db, user_data)
            print(f"Usuario creado: {user.username}")
        
        # Crear hábitos de ejemplo
        habits_data = [
            HabitCreate(
                name="Leer 5 páginas",
                description="Leer al menos 5 páginas de un libro cada día",
                habit_type=HabitType.DAILY,
                target_value=5.0,
                unit="páginas",
                icon="book_icon",
                color="#D6C8F0"
            ),
            HabitCreate(
                name="Ejercicio",
                description="Hacer ejercicio por 30 minutos",
                habit_type=HabitType.DAILY,
                target_value=30.0,
                unit="minutos",
                icon="exercise_icon",
                color="#C7F3C8"
            ),
            HabitCreate(
                name="Meditar",
                description="Meditar por 10 minutos",
                habit_type=HabitType.DAILY,
                target_value=10.0,
                unit="minutos",
                icon="meditation_icon",
                color="#E6D6B9"
            ),
            HabitCreate(
                name="Beber agua",
                description="Beber 8 vasos de agua al día",
                habit_type=HabitType.DAILY,
                target_value=8.0,
                unit="vasos",
                icon="water_icon",
                color="#B3E5FC"
            )
        ]
        
        for habit_data in habits_data:
            existing_habit = db.query(habit_crud.Habit).filter(
                habit_crud.Habit.name == habit_data.name,
                habit_crud.Habit.user_id == user.id
            ).first()
            
            if not existing_habit:
                habit = habit_crud.create_habit(db, habit_data, user.id)
                print(f"Hábito creado: {habit.name}")
        
        # Crear desafíos de ejemplo
        challenges_data = [
            ChallengeCreate(
                title="Trota 5Km",
                description="Completa una carrera de 5 kilómetros",
                challenge_type=ChallengeType.PROGRESS,
                target_value=5.0,
                unit="kilómetros",
                icon="run_icon",
                color="#E6D6B9",
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=7)
            ),
            ChallengeCreate(
                title="Lee 5 páginas de un libro",
                description="Lee al menos 5 páginas de cualquier libro",
                challenge_type=ChallengeType.SIMPLE,
                icon="intellectual_icon",
                color="#D6C8F0"
            ),
            ChallengeCreate(
                title="Habla con personas en diferentes lugares",
                description="Habla con personas en una cafetería, librería y centro comercial",
                challenge_type=ChallengeType.CHECKLIST,
                icon="social_icon",
                color="#E6D6B9",
                checklist_items=[
                    {"text": "Cafetería", "completed": True},
                    {"text": "Librería", "completed": False},
                    {"text": "Centro comercial", "completed": False}
                ]
            ),
            ChallengeCreate(
                title="Realiza 10 burpees",
                description="Completa 10 burpees como ejercicio",
                challenge_type=ChallengeType.PROGRESS,
                target_value=10.0,
                unit="repeticiones",
                icon="physical_icon",
                color="#C7F3C8"
            ),
            ChallengeCreate(
                title="Realiza un sudoku",
                description="Completa un sudoku de cualquier dificultad",
                challenge_type=ChallengeType.SIMPLE,
                icon="intellectual_icon",
                color="#D6C8F0"
            )
        ]
        
        for challenge_data in challenges_data:
            existing_challenge = db.query(challenge_crud.Challenge).filter(
                challenge_crud.Challenge.title == challenge_data.title,
                challenge_crud.Challenge.user_id == user.id
            ).first()
            
            if not existing_challenge:
                challenge = challenge_crud.create_challenge(db, challenge_data, user.id)
                print(f"Desafío creado: {challenge.title}")
        
        print("\n✅ Datos de ejemplo creados exitosamente!")
        print(f"📧 Email: {user.email}")
        print(f"🔑 Contraseña: demo123")
        print(f"👤 Usuario: {user.username}")
        
    except Exception as e:
        print(f"❌ Error creando datos de ejemplo: {e}")
        db.rollback()
    finally:
        db.close()

async def main():
    """Función principal"""
    print("🚀 Inicializando base de datos...")
    await init_db()
    print("📊 Creando datos de ejemplo...")
    create_sample_data()

if __name__ == "__main__":
    asyncio.run(main())
