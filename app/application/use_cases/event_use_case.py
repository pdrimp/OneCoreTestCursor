"""
Caso de uso de eventos.

Implementa la lógica de negocio para el registro y consulta de eventos.
"""

from typing import List, Optional
from datetime import datetime
from app.domain.entities.event import Event, EventType
from app.domain.repositories.event_repository import IEventRepository


class EventUseCase:
    """
    Caso de uso para gestión de eventos.
    
    Implementa la lógica de negocio para:
    - Registrar eventos del sistema
    - Consultar eventos con filtros
    - Exportar eventos a Excel
    """
    
    def __init__(self, event_repository: IEventRepository):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            event_repository: Repositorio de eventos para acceso a datos
        """
        self.event_repository = event_repository
    
    def create_event(
        self,
        event_type: EventType,
        description: str,
        user_id: Optional[int] = None,
        metadata: Optional[dict] = None
    ) -> Event:
        """
        Crea un nuevo evento en el sistema.
        
        Args:
            event_type: Tipo de evento
            description: Descripción del evento
            user_id: ID del usuario relacionado (opcional)
            metadata: Información adicional del evento (opcional)
            
        Returns:
            Event: Evento creado con ID asignado
        """
        event = Event(
            event_type=event_type,
            description=description,
            user_id=user_id,
            metadata=metadata or {}
        )
        return self.event_repository.create(event)
    
    def get_events(
        self,
        event_type: Optional[EventType] = None,
        description: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Event]:
        """
        Obtiene eventos aplicando filtros opcionales.
        
        Args:
            event_type: Filtrar por tipo de evento (opcional)
            description: Buscar en descripciones (opcional)
            start_date: Fecha de inicio del rango (opcional)
            end_date: Fecha de fin del rango (opcional)
            
        Returns:
            List[Event]: Lista de eventos que cumplen los filtros
        """
        if event_type:
            return self.event_repository.get_by_type(event_type)
        elif description:
            return self.event_repository.get_by_description(description)
        elif start_date and end_date:
            return self.event_repository.get_by_date_range(start_date, end_date)
        else:
            return self.event_repository.get_all()
    
    def export_to_excel(self, events: List[Event]) -> bytes:
        """
        Exporta una lista de eventos a formato Excel.
        
        Args:
            events: Lista de eventos a exportar
            
        Returns:
            bytes: Contenido del archivo Excel en bytes
        """
        import pandas as pd
        from io import BytesIO
        
        # Preparar datos
        data = []
        for event in events:
            data.append({
                "ID": event.id,
                "Tipo": event.event_type.value,
                "Descripción": event.description,
                "Usuario ID": event.user_id,
                "Fecha y Hora": event.created_at.strftime("%Y-%m-%d %H:%M:%S") if event.created_at else "",
                "Metadata": str(event.metadata) if event.metadata else ""
            })
        
        # Crear DataFrame
        df = pd.DataFrame(data)
        
        # Crear archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Eventos')
        
        output.seek(0)
        return output.getvalue()

