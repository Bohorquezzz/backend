# 🎯 Sistema de Retos Diarios Automáticos - UpDaily

## 📋 Descripción

El sistema de retos diarios automáticos permite generar y gestionar retos personalizados para cada usuario todos los días, con rotación automática y sistema de notificaciones.

## 🚀 Características

### ✨ Funcionalidades Principales
- **Generación Automática**: Retos diarios generados automáticamente a las 6:00 AM
- **Rotación Inteligente**: Selección aleatoria de retos de diferentes categorías
- **Sistema de Puntos**: Recompensas por completar retos
- **Estadísticas**: Seguimiento de progreso y rachas
- **Notificaciones**: Alertas automáticas para motivar a los usuarios

### 🏷️ Categorías de Retos
- **Físicos**: Ejercicios físicos, deportes, actividades corporales y bienestar físico
- **Intelectuales**: Lectura, meditación, aprendizaje, resolución de problemas y desarrollo mental
- **Sociales**: Interacciones sociales, comunicación, ayuda a otros y actividades comunitarias

### 📊 Niveles de Dificultad
- **Fácil (1)**: 5-10 puntos de recompensa
- **Medio (2)**: 10-15 puntos de recompensa  
- **Difícil (3)**: 15-25 puntos de recompensa

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install apscheduler==3.10.4
```

### 2. Ejecutar Migración de Base de Datos
```bash
python migration_daily_challenges.py
```

### 3. Poblar Plantillas de Retos
```bash
python init_daily_challenges.py
```

### 4. Iniciar la Aplicación
```bash
python main.py
```

## 📡 Endpoints de la API

### Retos Diarios del Usuario

#### `GET /api/v1/daily-challenges/mis-retos`
Obtener retos diarios del usuario
- **Parámetros**:
  - `challenge_date` (opcional): Fecha específica (por defecto: hoy)
  - `skip`: Número de registros a omitir
  - `limit`: Número máximo de registros

#### `GET /api/v1/daily-challenges/hoy`
Obtener retos de hoy para el usuario

#### `POST /api/v1/daily-challenges/completar/{challenge_id}`
Marcar un reto como completado
- **Parámetros**:
  - `progress_value`: Valor de progreso (0.0-1.0)

#### `PUT /api/v1/daily-challenges/{challenge_id}`
Actualizar un reto diario

#### `GET /api/v1/daily-challenges/estadisticas`
Obtener estadísticas del usuario

### Gestión de Plantillas (Admin)

#### `GET /api/v1/daily-challenges/plantillas`
Obtener plantillas de retos
- **Filtros**:
  - `categoria`: Filtrar por categoría
  - `dificultad`: Filtrar por dificultad (1-3)

#### `POST /api/v1/daily-challenges/plantillas`
Crear nueva plantilla de reto

#### `PUT /api/v1/daily-challenges/plantillas/{template_id}`
Actualizar plantilla de reto

#### `DELETE /api/v1/daily-challenges/plantillas/{template_id}`
Eliminar plantilla de reto

#### `POST /api/v1/daily-challenges/generar-retos`
Generar retos manualmente para todos los usuarios

## ⏰ Tareas Programadas

### Generación Automática
- **Frecuencia**: Diaria a las 6:00 AM
- **Función**: Genera 3-5 retos aleatorios para cada usuario
- **Notificaciones**: Envía notificaciones a todos los usuarios

### Limpieza de Datos
- **Frecuencia**: Domingos a las 2:00 AM
- **Función**: Limpia retos completados de hace más de 30 días

## 📊 Estadísticas del Usuario

```json
{
  "total_challenges": 45,
  "completed_challenges": 38,
  "completion_rate": 84.44,
  "current_streak": 7,
  "longest_streak": 15,
  "total_points": 450
}
```

## 🔔 Sistema de Notificaciones

### Tipos de Notificaciones
1. **Nuevos Retos**: Cuando se generan retos diarios
2. **Completado**: Cuando el usuario completa un reto
3. **Racha**: Notificaciones por días consecutivos
4. **Recordatorio**: Para retos pendientes
5. **Resumen Semanal**: Estadísticas de la semana

## 🗄️ Estructura de Base de Datos

### Tabla `daily_challenges`
```sql
- id: INT PRIMARY KEY
- user_id: INT (FK a usuario)
- reto_id: INT (FK a reto)
- challenge_date: DATE
- is_completed: BOOLEAN
- completed_at: DATETIME
- progress_value: FLOAT
- created_at: DATETIME
```

### Tabla `daily_challenge_templates`
```sql
- id: INT PRIMARY KEY
- nombre: VARCHAR(100)
- descripcion: TEXT
- tipo: INT (1=simple, 2=progreso, 3=checklist)
- categoria: VARCHAR(50)
- dificultad: INT (1-3)
- puntos_recompensa: INT
- is_active: BOOLEAN
- created_at: DATETIME
```

## 🎮 Flujo de Usuario

1. **6:00 AM**: Sistema genera retos automáticamente
2. **Usuario recibe notificación** de nuevos retos
3. **Usuario completa retos** durante el día
4. **Sistema envía notificaciones** de felicitación
5. **Usuario ve estadísticas** de progreso
6. **Al día siguiente**: Nuevos retos se generan automáticamente

## 🔧 Configuración Avanzada

### Personalizar Horarios
```python
# En app/services/scheduler.py
self.scheduler.add_job(
    self.generate_daily_challenges,
    CronTrigger(hour=6, minute=0),  # Cambiar hora aquí
    id='generate_daily_challenges'
)
```

### Agregar Nuevas Categorías
```python
# En init_daily_challenges.py
{
    "nombre": "Nuevo Reto",
    "descripcion": "Descripción del reto",
    "tipo": 1,
    "categoria": "nueva_categoria",  # Nueva categoría
    "dificultad": 2,
    "puntos_recompensa": 15
}
```

## 🐛 Solución de Problemas

### Los retos no se generan automáticamente
1. Verificar que el scheduler esté iniciado
2. Revisar logs de la aplicación
3. Verificar conexión a la base de datos

### Error en notificaciones
1. Verificar configuración de logging
2. Revisar permisos de base de datos
3. Verificar que las plantillas estén activas

## 📈 Métricas y Monitoreo

### Logs Importantes
- Generación de retos diarios
- Completado de retos por usuario
- Errores en notificaciones
- Estadísticas de uso

### KPIs Recomendados
- Tasa de completado de retos
- Retención de usuarios
- Engagement diario
- Distribución por categorías

## 🚀 Próximas Mejoras

- [ ] Notificaciones push móviles
- [ ] Retos personalizados por usuario
- [ ] Sistema de logros y badges
- [ ] Competencias entre usuarios
- [ ] Integración con wearables
- [ ] IA para recomendaciones personalizadas
