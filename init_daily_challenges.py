"""
Script para inicializar plantillas de retos diarios
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.database import DailyChallengeTemplate
from app.crud import daily_challenge as daily_challenge_crud
from app.schemas.daily_challenge import DailyChallengeTemplateCreate

def create_daily_challenge_templates():
    """Crear plantillas de retos diarios"""
    
    templates_data = [
        # CATEGORÍA: FÍSICOS
        {
            "nombre": "Hacer 30 flexiones",
            "descripcion": "Completa 30 flexiones en cualquier momento del día",
            "tipo": 2,  # progreso
            "categoria": "fisicos",
            "dificultad": 2,
            "puntos_recompensa": 15
        },
        {
            "nombre": "Caminar 10,000 pasos",
            "descripcion": "Camina al menos 10,000 pasos durante el día",
            "tipo": 2,  # progreso
            "categoria": "fisicos",
            "dificultad": 1,
            "puntos_recompensa": 10
        },
        {
            "nombre": "Hacer 5 minutos de estiramiento",
            "descripcion": "Dedica 5 minutos a estirar tu cuerpo",
            "tipo": 1,  # simple
            "categoria": "fisicos",
            "dificultad": 1,
            "puntos_recompensa": 5
        },
        {
            "nombre": "Hacer 20 sentadillas",
            "descripcion": "Completa 20 sentadillas con buena forma",
            "tipo": 2,  # progreso
            "categoria": "fisicos",
            "dificultad": 1,
            "puntos_recompensa": 10
        },
        {
            "nombre": "Correr 2 kilómetros",
            "descripcion": "Corre al menos 2 kilómetros",
            "tipo": 2,  # progreso
            "categoria": "fisicos",
            "dificultad": 3,
            "puntos_recompensa": 25
        },
        {
            "nombre": "Hacer 10 minutos de yoga",
            "descripcion": "Practica yoga durante 10 minutos",
            "tipo": 1,  # simple
            "categoria": "fisicos",
            "dificultad": 1,
            "puntos_recompensa": 8
        },
        {
            "nombre": "Subir escaleras durante 5 minutos",
            "descripcion": "Sube y baja escaleras durante 5 minutos seguidos",
            "tipo": 1,  # simple
            "categoria": "fisicos",
            "dificultad": 2,
            "puntos_recompensa": 12
        },
        {
            "nombre": "Hacer 50 saltos de tijera",
            "descripcion": "Completa 50 saltos de tijera (jumping jacks)",
            "tipo": 2,  # progreso
            "categoria": "fisicos",
            "dificultad": 2,
            "puntos_recompensa": 12
        },
        {
            "nombre": "Caminar al aire libre 20 minutos",
            "descripcion": "Camina al aire libre durante al menos 20 minutos",
            "tipo": 1,  # simple
            "categoria": "fisicos",
            "dificultad": 1,
            "puntos_recompensa": 10
        },
        {
            "nombre": "Hacer 3 series de plancha",
            "descripcion": "Mantén la posición de plancha por 30 segundos, 3 veces",
            "tipo": 2,  # progreso
            "categoria": "fisicos",
            "dificultad": 3,
            "puntos_recompensa": 20
        },
        
        # CATEGORÍA: INTELECTUALES
        {
            "nombre": "Leer 10 páginas de un libro",
            "descripcion": "Lee al menos 10 páginas de cualquier libro",
            "tipo": 2,  # progreso
            "categoria": "intelectuales",
            "dificultad": 1,
            "puntos_recompensa": 10
        },
        {
            "nombre": "Meditar 10 minutos",
            "descripcion": "Dedica 10 minutos a la meditación o mindfulness",
            "tipo": 1,  # simple
            "categoria": "intelectuales",
            "dificultad": 2,
            "puntos_recompensa": 15
        },
        {
            "nombre": "Aprender 5 palabras nuevas",
            "descripcion": "Aprende y memoriza 5 palabras nuevas en cualquier idioma",
            "tipo": 2,  # progreso
            "categoria": "intelectuales",
            "dificultad": 1,
            "puntos_recompensa": 8
        },
        {
            "nombre": "Resolver un sudoku",
            "descripcion": "Completa un sudoku de cualquier dificultad",
            "tipo": 1,  # simple
            "categoria": "intelectuales",
            "dificultad": 2,
            "puntos_recompensa": 12
        },
        {
            "nombre": "Escribir en un diario",
            "descripcion": "Escribe al menos 3 párrafos en tu diario personal",
            "tipo": 1,  # simple
            "categoria": "intelectuales",
            "dificultad": 1,
            "puntos_recompensa": 8
        },
        {
            "nombre": "Estudiar un tema nuevo por 30 minutos",
            "descripcion": "Dedica 30 minutos a estudiar algo que no sepas",
            "tipo": 1,  # simple
            "categoria": "intelectuales",
            "dificultad": 2,
            "puntos_recompensa": 15
        },
        {
            "nombre": "Resolver 5 crucigramas",
            "descripcion": "Resuelve al menos 5 crucigramas o sopas de letras",
            "tipo": 2,  # progreso
            "categoria": "intelectuales",
            "dificultad": 2,
            "puntos_recompensa": 12
        },
        {
            "nombre": "Ver un documental educativo",
            "descripcion": "Mira un documental educativo de al menos 20 minutos",
            "tipo": 1,  # simple
            "categoria": "intelectuales",
            "dificultad": 1,
            "puntos_recompensa": 10
        },
        {
            "nombre": "Practicar un idioma extranjero",
            "descripcion": "Practica un idioma extranjero durante 15 minutos",
            "tipo": 1,  # simple
            "categoria": "intelectuales",
            "dificultad": 2,
            "puntos_recompensa": 12
        },
        {
            "nombre": "Resolver un problema matemático",
            "descripcion": "Resuelve un problema matemático o de lógica",
            "tipo": 1,  # simple
            "categoria": "intelectuales",
            "dificultad": 2,
            "puntos_recompensa": 12
        },
        
        # CATEGORÍA: SOCIALES
        {
            "nombre": "Llamar a un amigo o familiar",
            "descripcion": "Haz una llamada de al menos 5 minutos a alguien importante",
            "tipo": 1,  # simple
            "categoria": "sociales",
            "dificultad": 1,
            "puntos_recompensa": 10
        },
        {
            "nombre": "Hacer un cumplido genuino",
            "descripcion": "Haz un cumplido sincero a alguien durante el día",
            "tipo": 1,  # simple
            "categoria": "sociales",
            "dificultad": 1,
            "puntos_recompensa": 8
        },
        {
            "nombre": "Ayudar a alguien",
            "descripcion": "Ayuda a alguien con una tarea o problema",
            "tipo": 1,  # simple
            "categoria": "sociales",
            "dificultad": 2,
            "puntos_recompensa": 15
        },
        {
            "nombre": "Sonreír a 3 personas",
            "descripcion": "Sonríe genuinamente a al menos 3 personas diferentes",
            "tipo": 2,  # progreso
            "categoria": "sociales",
            "dificultad": 1,
            "puntos_recompensa": 5
        },
        {
            "nombre": "Escribir una carta de agradecimiento",
            "descripcion": "Escribe una carta o mensaje de agradecimiento a alguien",
            "tipo": 1,  # simple
            "categoria": "sociales",
            "dificultad": 2,
            "puntos_recompensa": 12
        },
        {
            "nombre": "Iniciar una conversación con un desconocido",
            "descripcion": "Inicia una conversación amigable con alguien que no conozcas",
            "tipo": 1,  # simple
            "categoria": "sociales",
            "dificultad": 3,
            "puntos_recompensa": 20
        },
        {
            "nombre": "Participar en una actividad grupal",
            "descripcion": "Participa en una actividad grupal o de equipo",
            "tipo": 1,  # simple
            "categoria": "sociales",
            "dificultad": 2,
            "puntos_recompensa": 15
        },
        {
            "nombre": "Dar las gracias a 3 personas",
            "descripcion": "Expresa gratitud genuina a al menos 3 personas",
            "tipo": 2,  # progreso
            "categoria": "sociales",
            "dificultad": 1,
            "puntos_recompensa": 8
        },
        {
            "nombre": "Compartir una comida con alguien",
            "descripcion": "Comparte una comida o bebida con otra persona",
            "tipo": 1,  # simple
            "categoria": "sociales",
            "dificultad": 1,
            "puntos_recompensa": 10
        },
        {
            "nombre": "Hacer una buena acción anónima",
            "descripcion": "Haz una buena acción sin que nadie sepa que fuiste tú",
            "tipo": 1,  # simple
            "categoria": "sociales",
            "dificultad": 2,
            "puntos_recompensa": 15
        }
    ]
    
    db = SessionLocal()
    try:
        # Verificar si ya existen plantillas
        existing_templates = db.query(DailyChallengeTemplate).count()
        if existing_templates > 0:
            print(f"Ya existen {existing_templates} plantillas de retos diarios")
            return
        
        # Crear plantillas
        for template_data in templates_data:
            template = DailyChallengeTemplateCreate(**template_data)
            daily_challenge_crud.create_daily_challenge_template(db, template)
            print(f"Plantilla creada: {template_data['nombre']}")
        
        print(f"✅ Se crearon {len(templates_data)} plantillas de retos diarios")
        
    except Exception as e:
        print(f"❌ Error creando plantillas: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_daily_challenge_templates()
