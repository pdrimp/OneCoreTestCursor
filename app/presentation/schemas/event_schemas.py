"""
Esquemas de eventos.

Define los DTOs para las operaciones con eventos.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class EventResponse(BaseModel):
    """
    Esquema para la respuesta de evento.
    
    Attributes:
        id: ID del evento
        event_type: Tipo de evento
        description: Descripción del evento
        user_id: ID del usuario relacionado
        metadata: Información adicional
        created_at: Fecha y hora del evento
    """
    id: int = Field(..., description="ID del evento")
    event_type: str = Field(..., description="Tipo de evento")
    description: str = Field(..., description="Descripción del evento")
    user_id: Optional[int] = Field(None, description="ID del usuario")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata del evento")
    created_at: datetime = Field(..., description="Fecha y hora del evento")
    
    class Config:
        from_attributes = True


class EventFilter(BaseModel):
    """
    Esquema para filtros de eventos.
    
    Attributes:
        event_type: Filtrar por tipo de evento (opcional)
        description: Buscar en descripciones (opcional)
        start_date: Fecha de inicio del rango (opcional)
        end_date: Fecha de fin del rango (opcional)
    """
    event_type: Optional[str] = Field(None, description="Tipo de evento a filtrar")
    description: Optional[str] = Field(None, description="Texto a buscar en descripciones")
    start_date: Optional[datetime] = Field(None, description="Fecha de inicio")
    end_date: Optional[datetime] = Field(None, description="Fecha de fin")

