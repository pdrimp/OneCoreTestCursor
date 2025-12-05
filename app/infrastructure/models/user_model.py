"""
Modelo de base de datos para usuarios.

Mapea la entidad User del dominio a la tabla 'users' en SQL Server.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class UserModel(Base):
    """
    Modelo SQLAlchemy para la tabla de usuarios.
    
    Representa la estructura de la tabla 'users' en la base de datos.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

