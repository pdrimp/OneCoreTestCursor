"""
Implementación del repositorio de eventos.

Implementa IEventRepository utilizando SQLAlchemy y SQL Server.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.domain.entities.event import Event, EventType
from app.domain.repositories.event_repository import IEventRepository
from app.infrastructure.models.event_model import EventModel


class EventRepository(IEventRepository):
    """
    Implementación concreta del repositorio de eventos.

    Utiliza SQLAlchemy para interactuar con la base de datos SQL Server.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db: Sesión de SQLAlchemy para operaciones de base de datos
        """
        self.db = db

    def _to_entity(self, model: EventModel) -> Event:
        """
        Convierte un modelo de SQLAlchemy a una entidad del dominio.

        Args:
            model: Instancia de EventModel

        Returns:
            Event: Instancia de Event del dominio
        """
        return Event(
            id_=model.id,
            event_type=EventType(model.event_type) if model.event_type else EventType.USER_INTERACTION,
            description=model.description,
            user_id=model.user_id,
            metadata=model.metadata,
            created_at=model.created_at
        )

    def _to_model(self, entity: Event) -> EventModel:
        """
        Convierte una entidad del dominio a un modelo de SQLAlchemy.

        Args:
            entity: Instancia de Event del dominio

        Returns:
            EventModel: Instancia de EventModel para base de datos
        """
        return EventModel(
            id=entity.id,
            event_type=entity.event_type.value if entity.event_type else "user_interaction",
            description=entity.description,
            user_id=entity.user_id,
            metadata=entity.metadata,
            created_at=entity.created_at
        )

    def create(self, event: Event) -> Event:
        """
        Crea un nuevo evento en la base de datos.

        Args:
            event: Instancia de Event a crear

        Returns:
            Event: Evento creado con ID asignado
        """
        db_event = self._to_model(event)
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return self._to_entity(db_event)

    def get_by_id(self, event_id: int) -> Optional[Event]:
        """
        Obtiene un evento por su ID.

        Args:
            event_id: Identificador único del evento

        Returns:
            Optional[Event]: Evento encontrado o None si no existe
        """
        db_event = self.db.query(EventModel).filter(EventModel.id == event_id).first()
        return self._to_entity(db_event) if db_event else None

    def get_by_type(self, event_type: EventType) -> List[Event]:
        """
        Obtiene todos los eventos de un tipo específico.

        Args:
            event_type: Tipo de evento a filtrar

        Returns:
            List[Event]: Lista de eventos del tipo especificado
        """
        db_events = self.db.query(EventModel).filter(EventModel.event_type == event_type.value).all()
        return [self._to_entity(db_event) for db_event in db_events]

    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Event]:
        """
        Obtiene eventos en un rango de fechas.

        Args:
            start_date: Fecha de inicio del rango
            end_date: Fecha de fin del rango

        Returns:
            List[Event]: Lista de eventos en el rango especificado
        """
        db_events = self.db.query(EventModel).filter(
            EventModel.created_at >= start_date,
            EventModel.created_at <= end_date
        ).all()
        return [self._to_entity(db_event) for db_event in db_events]

    def get_by_description(self, description: str) -> List[Event]:
        """
        Busca eventos por descripción (búsqueda parcial).

        Args:
            description: Texto a buscar en las descripciones

        Returns:
            List[Event]: Lista de eventos que coinciden con la descripción
        """
        db_events = self.db.query(EventModel).filter(
            EventModel.description.ilike(f"%{description}%")
        ).all()
        return [self._to_entity(db_event) for db_event in db_events]

    def get_all(self) -> List[Event]:
        """
        Obtiene todos los eventos del repositorio.

        Returns:
            List[Event]: Lista de todos los eventos
        """
        db_events = self.db.query(EventModel).all()
        return [self._to_entity(db_event) for db_event in db_events]
