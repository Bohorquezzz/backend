# Arquitectura del Backend UpDaily

## Visión General

El backend de UpDaily está construido con FastAPI y sigue una arquitectura limpia y modular que facilita el mantenimiento y la escalabilidad.

## Estructura del Proyecto

```
backend/
├── app/
│   ├── core/              # Configuración y utilidades centrales
│   │   ├── config.py      # Configuración de la aplicación
│   │   ├── security.py    # Utilidades de seguridad y JWT
│   │   └── deps.py        # Dependencias de inyección
│   ├── crud/              # Operaciones de base de datos
│   │   ├── user.py        # CRUD para usuarios
│   │   ├── habit.py       # CRUD para hábitos
│   │   ├── challenge.py   # CRUD para desafíos
│   │   └── progress.py    # CRUD para progreso
│   ├── models/            # Modelos de SQLAlchemy
│   │   └── database.py    # Definición de tablas
│   ├── routers/           # Endpoints de la API
│   │   ├── auth.py        # Autenticación
│   │   ├── users.py       # Gestión de usuarios
│   │   ├── habits.py      # Gestión de hábitos
│   │   ├── challenges.py  # Gestión de desafíos
│   │   └── progress.py    # Seguimiento de progreso
│   ├── schemas/           # Esquemas de Pydantic
│   │   ├── user.py        # Esquemas de usuario
│   │   ├── habit.py       # Esquemas de hábito
│   │   ├── challenge.py   # Esquemas de desafío
│   │   ├── progress.py    # Esquemas de progreso
│   │   └── auth.py        # Esquemas de autenticación
│   └── database.py        # Configuración de base de datos
├── tests/                 # Pruebas unitarias
├── main.py               # Punto de entrada
├── requirements.txt      # Dependencias
└── README.md            # Documentación
```

## Flujo de Datos

### 1. Autenticación
```
Cliente → POST /auth/login → Verificar credenciales → Generar JWT → Retornar token
```

### 2. Operaciones CRUD
```
Cliente → Endpoint → Router → CRUD → Base de Datos → Respuesta
```

### 3. Seguridad
```
Request → Middleware CORS → Verificar JWT → Autorizar → Procesar → Respuesta
```

## Modelos de Datos

### User (Usuario)
- **id**: Identificador único
- **email**: Email único del usuario
- **username**: Nombre de usuario único
- **full_name**: Nombre completo
- **hashed_password**: Contraseña hasheada
- **is_active**: Estado activo/inactivo
- **created_at/updated_at**: Timestamps

### Habit (Hábito)
- **id**: Identificador único
- **user_id**: Referencia al usuario
- **name**: Nombre del hábito
- **description**: Descripción opcional
- **habit_type**: Tipo (diario, semanal, mensual)
- **target_value**: Valor objetivo
- **unit**: Unidad de medida
- **icon/color**: Configuración visual
- **is_active**: Estado activo/inactivo

### Challenge (Desafío)
- **id**: Identificador único
- **user_id**: Referencia al usuario
- **title**: Título del desafío
- **description**: Descripción
- **challenge_type**: Tipo (simple, progreso, checklist)
- **status**: Estado (pendiente, en progreso, completado, fallido)
- **target_value**: Valor objetivo
- **current_value**: Progreso actual
- **checklist_items**: Items para checklist (JSON)
- **start_date/end_date**: Fechas de inicio y fin

### ProgressRecord (Registro de Progreso)
- **id**: Identificador único
- **user_id**: Referencia al usuario
- **habit_id**: Referencia al hábito (opcional)
- **challenge_id**: Referencia al desafío (opcional)
- **date**: Fecha del progreso
- **value**: Valor del progreso
- **notes**: Notas opcionales

## Endpoints de la API

### Autenticación (`/api/v1/auth/`)
- `POST /register` - Registro de usuario
- `POST /login` - Inicio de sesión
- `POST /token` - OAuth2 token
- `GET /me` - Información del usuario actual

### Usuarios (`/api/v1/users/`)
- `GET /me` - Obtener perfil
- `PUT /me` - Actualizar perfil
- `DELETE /me` - Eliminar cuenta

### Hábitos (`/api/v1/habits/`)
- `GET /` - Listar hábitos
- `POST /` - Crear hábito
- `GET /{id}` - Obtener hábito
- `PUT /{id}` - Actualizar hábito
- `DELETE /{id}` - Eliminar hábito

### Desafíos (`/api/v1/challenges/`)
- `GET /` - Listar desafíos
- `POST /` - Crear desafío
- `GET /{id}` - Obtener desafío
- `PUT /{id}` - Actualizar desafío
- `POST /{id}/progress` - Actualizar progreso
- `DELETE /{id}` - Eliminar desafío

### Progreso (`/api/v1/progress/`)
- `GET /` - Listar registros
- `POST /` - Crear registro
- `GET /stats` - Estadísticas del usuario
- `GET /habit/{id}` - Progreso de hábito
- `GET /challenge/{id}` - Progreso de desafío
- `GET /{id}` - Obtener registro
- `PUT /{id}` - Actualizar registro
- `DELETE /{id}` - Eliminar registro

## Seguridad

### Autenticación JWT
- Tokens con expiración configurable
- Algoritmo HS256
- Verificación en cada request protegido

### Hash de Contraseñas
- Bcrypt para hashing seguro
- Salt automático
- Verificación segura

### CORS
- Configuración flexible
- Soporte para aplicaciones móviles
- Headers de seguridad

## Base de Datos

### SQLAlchemy ORM
- Modelos declarativos
- Relaciones bien definidas
- Migraciones con Alembic

### SQLite (Desarrollo)
- Base de datos ligera
- Fácil configuración
- Ideal para desarrollo

### PostgreSQL (Producción)
- Base de datos robusta
- Soporte para concurrencia
- Escalabilidad

## Patrones de Diseño

### Dependency Injection
- FastAPI dependency system
- Inyección de base de datos
- Verificación de autenticación

### Repository Pattern
- CRUD operations encapsuladas
- Separación de lógica de negocio
- Fácil testing

### Schema Validation
- Pydantic para validación
- Serialización automática
- Documentación automática

## Escalabilidad

### Horizontal Scaling
- Stateless design
- JWT tokens
- Load balancer ready

### Vertical Scaling
- Optimized queries
- Database indexing
- Connection pooling

### Caching
- Redis ready
- Session management
- API response caching

## Monitoreo y Logging

### Health Checks
- `/health` endpoint
- Database connectivity
- Service status

### Logging
- Structured logging
- Request/response tracking
- Error monitoring

### Metrics
- Performance metrics
- Usage statistics
- Error rates

## Testing

### Unit Tests
- pytest framework
- Test coverage
- Mocking dependencies

### Integration Tests
- API endpoint testing
- Database testing
- Authentication testing

### Load Testing
- Performance benchmarks
- Stress testing
- Scalability validation

## Despliegue

### Docker
- Containerized application
- Multi-stage builds
- Health checks

### Docker Compose
- Local development
- Service orchestration
- Environment configuration

### Production
- Environment variables
- Database migrations
- SSL/TLS configuration
- Reverse proxy setup
