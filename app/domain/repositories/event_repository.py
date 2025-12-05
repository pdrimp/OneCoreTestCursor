"""
Interfaz del repositorio de eventos.

Define el contrato que deben cumplir las implementaciones
del repositorio de eventos.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from app.domain.entities.event import Event, EventType


class IEventRepository(ABC):
    """
    Interfaz abstracta para el repositorio de eventos.
    
    Define los métodos que deben implementar los repositorios
    de eventos sin especificar la implementación concreta.
    """
    
    @abstractmethod
    def create(self, event: Event) -> Event:
        """
        Crea un nuevo evento en el repositorio.
        
        Args:
            event: Instancia de Event a crear
            
        Returns:
            Event: Evento creado con ID asignado
        """
        pass
    
    @abstractmethod
    def get_by_id(self, event_id: int) -> Optional[Event]:
        """
        Obtiene un evento por su ID.
        
        Args:
            event_id: Identificador único del evento
            
        Returns:
            Optional[Event]: Evento encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    def get_by_type(self, event_type: EventType) -> List[Event]:
        """
        Obtiene todos los eventos de un tipo específico.
        
        Args:
            event_type: Tipo de evento a filtrar
            
        Returns:
            List[Event]: Lista de eventos del tipo especificado
        """
        pass
    
    @abstractmethod
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Event]:
        """
        Obtiene eventos en un rango de fechas.
        
        Args:
            start_date: Fecha de inicio del rango
            end_date: Fecha de fin del rango
            
        Returns:
            List[Event]: Lista de eventos en el rango especificado
        """
        pass
    
    @abstractmethod
    def get_by_description(self, description: str) -> List[Event]:
        """
        Busca eventos por descripción (búsqueda parcial).
        
        Args:
            description: Texto a buscar en las descripciones
            
        Returns:
            List[Event]: Lista de eventos que coinciden con la descripción
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Event]:
        """
        Obtiene todos los eventos del repositorio.
        
        Returns:
            List[Event]: Lista de todos los eventos
        """
        pass

