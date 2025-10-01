# Categorías de Retos en UpDaily

## Estructura

Los retos en UpDaily ahora están categorizados en tres tipos principales:

1. **SOCIAL**: Retos que involucran interacción social, desarrollo de habilidades interpersonales o actividades comunitarias.
2. **FISICA**: Retos relacionados con actividad física, ejercicio, deportes o salud.
3. **INTELECTUAL**: Retos que promueven el desarrollo mental, aprendizaje, creatividad o habilidades cognitivas.

## Cambios Técnicos

### Modelo de Base de Datos
- Se ha añadido una nueva columna `categoria` a la tabla `reto`
- La columna es de tipo ENUM con los valores: SOCIAL, FISICA, INTELECTUAL
- Se utiliza el tipo RetoCategoria de SQLAlchemy/Pydantic para validación
- Por defecto, los retos existentes se categorizarán como SOCIAL

### API Endpoints
Los endpoints existentes ahora soportan la categorización:

- `POST /retos/`: Requiere especificar una categoría al crear un nuevo reto
- `PUT /retos/{id}`: Permite actualizar la categoría de un reto existente
- `GET /retos/`: Devuelve la categoría junto con la información del reto

### Migración de Datos
Se ha creado una migración de Alembic para:
1. Añadir la nueva columna `categoria`
2. Establecer un valor por defecto para retos existentes
3. Configurar la restricción de no nulo

## Uso

### Crear un Nuevo Reto
```json
POST /retos/
{
    "nombre_reto": "Nuevo Reto",
    "descripcion_reto": "Descripción del reto",
    "tipo": 1,
    "categoria": "SOCIAL"  // SOCIAL, FISICA, o INTELECTUAL
}