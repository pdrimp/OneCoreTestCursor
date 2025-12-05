"""
Modelo de base de datos para eventos.

Mapea la entidad Event del dominio a la tabla 'events' en SQL Server.
"""

from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.infrastructure.database import Base


class EventModel(Base):
    """
    Modelo SQLAlchemy para la tabla de eventos.

    Representa la estructura de la tabla 'events' en la base de datos.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    description = Column(String(1000), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
