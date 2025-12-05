"""
Modelo de base de datos para documentos.

Mapea la entidad Document del dominio a la tabla 'documents' en SQL Server.
"""

from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class DocumentModel(Base):
    """
    Modelo SQLAlchemy para la tabla de documentos.

    Representa la estructura de la tabla 'documents' en la base de datos.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False, default="unknown")
    file_path = Column(String(1000), nullable=False)
    extracted_data = Column(JSON, nullable=True)
    sentiment = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
