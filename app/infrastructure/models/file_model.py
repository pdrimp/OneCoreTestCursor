"""
Modelo de base de datos para archivos.

Mapea la entidad File del dominio a la tabla 'files' en SQL Server.
"""

from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class FileModel(Base):
    """
    Modelo SQLAlchemy para la tabla de archivos.
    
    Representa la estructura de la tabla 'files' en la base de datos.
    """
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    s3_key = Column(String(500), nullable=False, unique=True)
    s3_url = Column(String(1000), nullable=True)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    validations = Column(JSON, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

