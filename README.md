# UpDaily Backend API

Backend API para la aplicación móvil UpDaily - Sistema de seguimiento de hábitos y desafíos diarios.

## Características

- **Autenticación JWT**: Sistema seguro de autenticación con tokens JWT
- **Gestión de Usuarios**: Registro, login y gestión de perfiles
- **Hábitos**: Creación, edición y seguimiento de hábitos diarios
- **Desafíos**: Sistema de desafíos con diferentes tipos (simple, progreso, checklist)
- **Seguimiento de Progreso**: Registro y estadísticas de progreso
- **API RESTful**: Endpoints bien documentados con FastAPI
- **Base de Datos**: SQLAlchemy con soporte para SQLite (fácil migración a PostgreSQL)

## Tecnologías

- **FastAPI**: Framework web moderno y rápido para Python
- **SQLAlchemy**: ORM para manejo de base de datos
- **Pydantic**: Validación de datos y serialización
- **JWT**: Autenticación con JSON Web Tokens
- **Bcrypt**: Hashing seguro de contraseñas

## Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd backend
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar la aplicación**:
```bash
python main.py
```

La API estará disponible en `http://localhost:8000`

## Documentación

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Estructura del Proyecto

```
backend/
├── app/
│   ├── core/           # Configuración y utilidades
│   ├── crud/           # Operaciones de base de datos
│   ├── models/         # Modelos de SQLAlchemy
│   ├── routers/        # Endpoints de la API
│   ├── schemas/        # Esquemas de Pydantic
│   └── database.py     # Configuración de base de datos
├── main.py             # Punto de entrada de la aplicación
├── requirements.txt    # Dependencias de Python
└── README.md          # Este archivo
```

## Endpoints Principales

### Autenticación
- `POST /api/v1/auth/register` - Registro de usuario
- `POST /api/v1/auth/login` - Inicio de sesión
- `GET /api/v1/auth/me` - Información del usuario actual

### Usuarios
- `GET /api/v1/users/me` - Obtener perfil
- `PUT /api/v1/users/me` - Actualizar perfil
- `DELETE /api/v1/users/me` - Eliminar cuenta

### Hábitos
- `GET /api/v1/habits/` - Listar hábitos
- `POST /api/v1/habits/` - Crear hábito
- `GET /api/v1/habits/{id}` - Obtener hábito
- `PUT /api/v1/habits/{id}` - Actualizar hábito
- `DELETE /api/v1/habits/{id}` - Eliminar hábito

### Desafíos
- `GET /api/v1/challenges/` - Listar desafíos
- `POST /api/v1/challenges/` - Crear desafío
- `GET /api/v1/challenges/{id}` - Obtener desafío
- `PUT /api/v1/challenges/{id}` - Actualizar desafío
- `POST /api/v1/challenges/{id}/progress` - Actualizar progreso
- `DELETE /api/v1/challenges/{id}` - Eliminar desafío

### Progreso
- `GET /api/v1/progress/` - Listar registros de progreso
- `POST /api/v1/progress/` - Crear registro de progreso
- `GET /api/v1/progress/stats` - Estadísticas del usuario
- `GET /api/v1/progress/habit/{id}` - Progreso de hábito específico
- `GET /api/v1/progress/challenge/{id}` - Progreso de desafío específico

## Modelos de Datos

### Usuario
- Información personal (email, username, nombre completo)
- Autenticación segura con hash de contraseñas
- Timestamps de creación y actualización

### Hábito
- Nombre, descripción y tipo (diario, semanal, mensual)
- Valor objetivo y unidad de medida
- Configuración visual (icono, color)
- Estado activo/inactivo

### Desafío
- Título, descripción y tipo (simple, progreso, checklist)
- Valor objetivo y progreso actual
- Fechas de inicio y fin
- Estado (pendiente, en progreso, completado, fallido)
- Items de checklist (para desafíos tipo checklist)

### Registro de Progreso
- Fecha y valor del progreso
- Notas opcionales
- Relación con hábito o desafío específico

## Seguridad

- **JWT Tokens**: Autenticación stateless con tokens JWT
- **Hash de Contraseñas**: Uso de bcrypt para hashing seguro
- **CORS**: Configuración de CORS para aplicaciones móviles
- **Validación**: Validación estricta de datos con Pydantic

## Desarrollo

### Ejecutar en modo desarrollo
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Ejecutar tests
```bash
pytest
```

### Migraciones de base de datos
```bash
alembic upgrade head
```

## Despliegue

Para producción, considera:

1. **Base de datos**: Cambiar de SQLite a PostgreSQL
2. **Variables de entorno**: Configurar SECRET_KEY y DATABASE_URL
3. **HTTPS**: Configurar SSL/TLS
4. **CORS**: Restringir ALLOWED_ORIGINS a dominios específicos
5. **Logging**: Configurar logging apropiado
6. **Monitoreo**: Implementar monitoreo y alertas

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
