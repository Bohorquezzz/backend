"""
Script to initialize retos data
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.database import Reto, RetoCategoria

def init_retos(db: Session):
    # Physical challenges
    retos_fisicos = [
        {
            "nombre_reto": "Abdominales Básicos",
            "descripcion_reto": "Realiza 10 abdominales hoy",
            "tipo": 1,  # simple
            "categoria": RetoCategoria.FISICA
        },
        {
            "nombre_reto": "Sentadillas Express",
            "descripcion_reto": "Completa 15 sentadillas",
            "tipo": 1,
            "categoria": RetoCategoria.FISICA
        },
        {
            "nombre_reto": "Caminata Saludable",
            "descripcion_reto": "Camina 20 minutos continuos",
            "tipo": 1,
            "categoria": RetoCategoria.FISICA
        }
    ]

    # Social challenges
    retos_sociales = [
        {
            "nombre_reto": "Llamada Familiar",
            "descripcion_reto": "Llama a un familiar que hace tiempo no contactas",
            "tipo": 1,
            "categoria": RetoCategoria.SOCIAL
        },
        {
            "nombre_reto": "Café con Amigos",
            "descripcion_reto": "Organiza un café con un amigo",
            "tipo": 1,
            "categoria": RetoCategoria.SOCIAL
        },
        {
            "nombre_reto": "Networking Simple",
            "descripcion_reto": "Saluda a un compañero nuevo",
            "tipo": 1,
            "categoria": RetoCategoria.SOCIAL
        }
    ]

    # Intellectual challenges
    retos_intelectuales = [
        {
            "nombre_reto": "Lectura Rápida",
            "descripcion_reto": "Lee 5 páginas de un libro",
            "tipo": 1,
            "categoria": RetoCategoria.INTELECTUAL
        },
        {
            "nombre_reto": "Vocabulario Nuevo",
            "descripcion_reto": "Aprende 3 palabras nuevas",
            "tipo": 1,
            "categoria": RetoCategoria.INTELECTUAL
        },
        {
            "nombre_reto": "Rompecabezas Mental",
            "descripcion_reto": "Resuelve un sudoku o crucigrama",
            "tipo": 1,
            "categoria": RetoCategoria.INTELECTUAL
        }
    ]

    # Add all challenges
    all_retos = retos_fisicos + retos_sociales + retos_intelectuales
    
    for reto_data in all_retos:
        reto = Reto(**reto_data)
        db.add(reto)
    
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_retos(db)
        print("Retos inicializados correctamente")
    except Exception as e:
        print(f"Error al inicializar retos: {e}")
    finally:
        db.close()