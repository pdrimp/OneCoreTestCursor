"""
Entidad de Evento.

Define la estructura y comportamiento de los eventos registrados en el sistema.
"""

from typing import Optional
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    """Enum para el tipo de evento."""
    DOCUMENT_UPLOAD = "document_upload"
    AI_PROCESSING = "ai_processing"
    USER_INTERACTION = "user_interaction"
    FILE_UPLOAD = "file_upload"
    TOKEN_RENEWAL = "token_renewal"

class Event:
    """
    Entidad que representa un evento registrado en el sistema.

    Attributes:
        id: Identificador único del evento
        event_type: Tipo de evento
        description: Descripción del evento
        user_id: ID del usuario relacionado (opcional)
        metadata: Información adicional del evento en formato JSON
        created_at: Fecha y hora del evento
    """
    def __init__(
        self,
        id_: Optional[int] = None,
        event_type: EventType = EventType.USER_INTERACTION,
        description: str = "",
        user_id: Optional[int] = None,
        metadata: Optional[dict] = None,
        created_at: Optional[datetime] = None
    ):
        """
        Inicializa una instancia de Event.

        Args:
            id_: Identificador único del evento
            event_type: Tipo de evento
            description: Descripción del evento
            user_id: ID del usuario relacionado
            metadata: Información adicional del evento
            created_at: Fecha y hora del evento
        """
        self.id = id_
        self.event_type = event_type
        self.description = description
        self.user_id = user_id
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.utcnow()

    def __repr__(self) -> str:
        """Representación en string del evento."""
        return f"<Event(id={self.id}, type={self.event_type}, description={self.description})>"
