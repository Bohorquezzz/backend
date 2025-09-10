"""
Database models for UpDaily API - Conectado con MySQL
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, Enum, Date, Time, Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class HabitType(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class ChallengeType(enum.Enum):
    SIMPLE = "simple"
    PROGRESS = "progress"
    CHECKLIST = "checklist"

class ChallengeStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

# Modelo basado en la tabla 'usuario' de tu base de datos
class User(Base):
    __tablename__ = "usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=True)
    correo = Column(String(50), nullable=True, unique=True, index=True)
    clave = Column(String(50), nullable=True)  # Contraseña hasheada
    fecha_nacimiento = Column(Date, nullable=True)
    telefono = Column(Integer, nullable=True)
    img_foto_usuario = Column(Binary, nullable=True)
    
    # Relaciones con las tablas existentes
    retos_usuario = relationship("RetoUsuario", back_populates="usuario")
    logros = relationship("Logro", back_populates="usuario")

# Modelo basado en la tabla 'reto' de tu base de datos
class Reto(Base):
    __tablename__ = "reto"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_reto = Column(String(50), nullable=True)
    descripcion_reto = Column(String(50), nullable=True)
    tipo = Column(Integer, nullable=True)  # 1=simple, 2=progreso, 3=checklist
    
    # Relaciones
    retos_usuario = relationship("RetoUsuario", back_populates="reto")
    criterios_reto = relationship("CriterioReto", back_populates="reto")

# Modelo basado en la tabla 'criterio' de tu base de datos
class Criterio(Base):
    __tablename__ = "criterio"
    
    id = Column(Integer, primary_key=True, index=True)
    id_reto = Column(Integer, nullable=True)
    desc_criterio = Column(String(50), nullable=True)
    tiempo_est = Column(Time, nullable=True)
    
    # Relaciones
    criterios_reto = relationship("CriterioReto", back_populates="criterio")

# Modelo basado en la tabla 'criterio_reto' de tu base de datos
class CriterioReto(Base):
    __tablename__ = "criterio_reto"
    
    id = Column(Integer, primary_key=True, index=True)
    id_reto_usuario = Column(Integer, ForeignKey("reto_usuario.id"), nullable=True)
    id_criterio = Column(Integer, ForeignKey("criterio.id"), nullable=True)
    completado = Column(Binary(50), nullable=True)  # 0x00 = no completado, 0x01 = completado
    fecha_ul_modif = Column(Date, nullable=True)  # fecha última modificación
    fecha_prim_ra = Column(Date, nullable=True)  # fecha primer registro
    
    # Relaciones
    reto_usuario = relationship("RetoUsuario", back_populates="criterios_reto")
    criterio = relationship("Criterio", back_populates="criterios_reto")

# Modelo basado en la tabla 'reto_usuario' de tu base de datos
class RetoUsuario(Base):
    __tablename__ = "reto_usuario"
    
    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    id_reto = Column(Integer, ForeignKey("reto.id"), nullable=False)
    progreso_reto = Column(Float, default=0.0, nullable=False)
    
    # Relaciones
    usuario = relationship("User", back_populates="retos_usuario")
    reto = relationship("Reto", back_populates="retos_usuario")
    criterios_reto = relationship("CriterioReto", back_populates="reto_usuario")

# Modelo basado en la tabla 'logros' de tu base de datos
class Logro(Base):
    __tablename__ = "logros"
    
    id = Column(Integer, primary_key=True, index=True)
    id_reto_usuario = Column(Integer, ForeignKey("reto_usuario.id"), nullable=True)
    
    # Relaciones
    reto_usuario = relationship("RetoUsuario", back_populates="logros")
    usuario = relationship("User", back_populates="logros")

# Modelos adicionales para compatibilidad con la API existente
class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    habit_type = Column(Enum(HabitType), default=HabitType.DAILY)
    target_value = Column(Float, default=1.0)
    unit = Column(String)
    icon = Column(String)
    color = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", foreign_keys=[user_id])
    progress_records = relationship("ProgressRecord", back_populates="habit")

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    challenge_type = Column(Enum(ChallengeType), default=ChallengeType.SIMPLE)
    status = Column(Enum(ChallengeStatus), default=ChallengeStatus.PENDING)
    target_value = Column(Float)
    current_value = Column(Float, default=0.0)
    unit = Column(String)
    icon = Column(String)
    color = Column(String)
    checklist_items = Column(Text)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", foreign_keys=[user_id])

class ProgressRecord(Base):
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=True)
    date = Column(DateTime(timezone=True), nullable=False)
    value = Column(Float, default=1.0)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    user = relationship("User", foreign_keys=[user_id])
    habit = relationship("Habit", back_populates="progress_records")