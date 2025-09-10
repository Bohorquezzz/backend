"""
Script para inicializar la base de datos MySQL con datos de ejemplo
"""

import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.crud import user as user_crud, reto as reto_crud, criterio as criterio_crud
from app.schemas.user import UserCreate
from app.schemas.reto import RetoCreate, RetoUsuarioCreate
from app.schemas.criterio import CriterioCreate, CriterioRetoCreate
from datetime import datetime, date, time

def create_sample_data():
    """Crear datos de ejemplo para la aplicación"""
    db = SessionLocal()
    
    try:
        # Crear usuario de ejemplo
        user_data = UserCreate(
            nombre="Usuario Demo",
            correo="demo@updaily.com",
            clave="demo123",
            fecha_nacimiento=date(1990, 1, 1),
            telefono=1234567890
        )
        
        # Verificar si el usuario ya existe
        existing_user = user_crud.get_user_by_email(db, user_data.correo)
        if existing_user:
            print("Usuario demo ya existe")
            user = existing_user
        else:
            user = user_crud.create_user(db, user_data)
            print(f"Usuario creado: {user.nombre}")
        
        # Crear retos de ejemplo
        retos_data = [
            RetoCreate(
                nombre_reto="Trota 5Km",
                descripcion_reto="Completa una carrera de 5 kilómetros",
                tipo=2  # Progreso
            ),
            RetoCreate(
                nombre_reto="Lee 5 páginas",
                descripcion_reto="Lee al menos 5 páginas de un libro",
                tipo=1  # Simple
            ),
            RetoCreate(
                nombre_reto="Habla con personas",
                descripcion_reto="Habla con personas en diferentes lugares",
                tipo=3  # Checklist
            ),
            RetoCreate(
                nombre_reto="Realiza 10 burpees",
                descripcion_reto="Completa 10 burpees como ejercicio",
                tipo=2  # Progreso
            ),
            RetoCreate(
                nombre_reto="Realiza un sudoku",
                descripcion_reto="Completa un sudoku de cualquier dificultad",
                tipo=1  # Simple
            )
        ]
        
        retos_creados = []
        for reto_data in retos_data:
            existing_reto = db.query(reto_crud.Reto).filter(
                reto_crud.Reto.nombre_reto == reto_data.nombre_reto
            ).first()
            
            if not existing_reto:
                reto = reto_crud.create_reto(db, reto_data)
                retos_creados.append(reto)
                print(f"Reto creado: {reto.nombre_reto}")
            else:
                retos_creados.append(existing_reto)
        
        # Crear criterios para los retos
        criterios_data = [
            # Criterios para "Trota 5Km"
            CriterioCreate(
                id_reto=retos_creados[0].id,
                desc_criterio="Calentamiento previo",
                tiempo_est=time(0, 10)  # 10 minutos
            ),
            CriterioCreate(
                id_reto=retos_creados[0].id,
                desc_criterio="Carrera continua",
                tiempo_est=time(0, 30)  # 30 minutos
            ),
            CriterioCreate(
                id_reto=retos_creados[0].id,
                desc_criterio="Enfriamiento",
                tiempo_est=time(0, 10)  # 10 minutos
            ),
            
            # Criterios para "Habla con personas"
            CriterioCreate(
                id_reto=retos_creados[2].id,
                desc_criterio="Cafetería",
                tiempo_est=time(0, 15)  # 15 minutos
            ),
            CriterioCreate(
                id_reto=retos_creados[2].id,
                desc_criterio="Librería",
                tiempo_est=time(0, 15)  # 15 minutos
            ),
            CriterioCreate(
                id_reto=retos_creados[2].id,
                desc_criterio="Centro comercial",
                tiempo_est=time(0, 15)  # 15 minutos
            ),
            
            # Criterios para "Realiza 10 burpees"
            CriterioCreate(
                id_reto=retos_creados[3].id,
                desc_criterio="Posición inicial",
                tiempo_est=time(0, 1)  # 1 minuto
            ),
            CriterioCreate(
                id_reto=retos_creados[3].id,
                desc_criterio="Ejecución del burpee",
                tiempo_est=time(0, 5)  # 5 minutos
            ),
            CriterioCreate(
                id_reto=retos_creados[3].id,
                desc_criterio="Recuperación",
                tiempo_est=time(0, 2)  # 2 minutos
            )
        ]
        
        for criterio_data in criterios_data:
            existing_criterio = db.query(criterio_crud.Criterio).filter(
                criterio_crud.Criterio.desc_criterio == criterio_data.desc_criterio,
                criterio_crud.Criterio.id_reto == criterio_data.id_reto
            ).first()
            
            if not existing_criterio:
                criterio = criterio_crud.create_criterio(db, criterio_data)
                print(f"Criterio creado: {criterio.desc_criterio}")
        
        # Inscribir al usuario demo en algunos retos
        reto_usuario_data = [
            RetoUsuarioCreate(
                id_usuario=user.id,
                id_reto=retos_creados[0].id,  # Trota 5Km
                progreso_reto=0.0
            ),
            RetoUsuarioCreate(
                id_usuario=user.id,
                id_reto=retos_creados[1].id,  # Lee 5 páginas
                progreso_reto=0.0
            ),
            RetoUsuarioCreate(
                id_usuario=user.id,
                id_reto=retos_creados[2].id,  # Habla con personas
                progreso_reto=0.0
            )
        ]
        
        for reto_usuario_data_item in reto_usuario_data:
            existing_reto_usuario = db.query(reto_crud.RetoUsuario).filter(
                reto_crud.RetoUsuario.id_usuario == reto_usuario_data_item.id_usuario,
                reto_crud.RetoUsuario.id_reto == reto_usuario_data_item.id_reto
            ).first()
            
            if not existing_reto_usuario:
                reto_usuario = reto_crud.create_reto_usuario(db, reto_usuario_data_item)
                print(f"Usuario inscrito en reto: {reto_usuario.id_reto}")
        
        print("\n✅ Datos de ejemplo creados exitosamente!")
        print(f"📧 Email: {user.correo}")
        print(f"🔑 Contraseña: demo123")
        print(f"👤 Usuario: {user.nombre}")
        print(f"🎯 Retos disponibles: {len(retos_creados)}")
        
    except Exception as e:
        print(f"❌ Error creando datos de ejemplo: {e}")
        db.rollback()
    finally:
        db.close()

async def main():
    """Función principal"""
    print("🚀 Inicializando base de datos MySQL...")
    await init_db()
    print("📊 Creando datos de ejemplo...")
    create_sample_data()

if __name__ == "__main__":
    asyncio.run(main())
