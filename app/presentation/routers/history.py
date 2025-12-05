"""
Router de historial.

Define los endpoints relacionados con consulta y exportación de eventos.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import Response
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.domain.repositories.event_repository import IEventRepository
from app.infrastructure.repositories.event_repository_impl import EventRepository
from app.application.use_cases.event_use_case import EventUseCase
from app.domain.entities.event import EventType
from app.presentation.schemas.event_schemas import EventResponse, EventFilter
from app.presentation.middleware.auth_middleware import get_current_user

router = APIRouter()


def get_event_use_case(db: Session = Depends(get_db)) -> EventUseCase:
    """
    Dependencia para obtener una instancia de EventUseCase.
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        EventUseCase: Instancia del caso de uso de eventos
    """
    event_repository: IEventRepository = EventRepository(db)
    return EventUseCase(event_repository)


@router.get("/events", response_model=list[EventResponse], status_code=status.HTTP_200_OK)
async def get_events(
    event_type: Optional[str] = Query(None, description="Filtrar por tipo de evento"),
    description: Optional[str] = Query(None, description="Buscar en descripciones"),
    start_date: Optional[datetime] = Query(None, description="Fecha de inicio"),
    end_date: Optional[datetime] = Query(None, description="Fecha de fin"),
    current_user: dict = Depends(get_current_user),
    use_case: EventUseCase = Depends(get_event_use_case)
):
    """
    Endpoint para obtener eventos con filtros opcionales.
    
    Permite filtrar eventos por tipo, descripción o rango de fechas.
    
    Args:
        event_type: Tipo de evento a filtrar (opcional)
        description: Texto a buscar en descripciones (opcional)
        start_date: Fecha de inicio del rango (opcional)
        end_date: Fecha de fin del rango (opcional)
        current_user: Usuario actual autenticado
        use_case: Caso de uso de eventos
        
    Returns:
        list[EventResponse]: Lista de eventos que cumplen los filtros
    """
    # Convertir event_type string a EventType enum si se proporciona
    event_type_enum = None
    if event_type:
        try:
            event_type_enum = EventType(event_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de evento inválido: {event_type}"
            )
    
    events = use_case.get_events(
        event_type=event_type_enum,
        description=description,
        start_date=start_date,
        end_date=end_date
    )
    
    return [EventResponse(
        id=event.id,
        event_type=event.event_type.value,
        description=event.description,
        user_id=event.user_id,
        metadata=event.metadata,
        created_at=event.created_at
    ) for event in events]


@router.get("/events/export", status_code=status.HTTP_200_OK)
async def export_events(
    event_type: Optional[str] = Query(None, description="Filtrar por tipo de evento"),
    description: Optional[str] = Query(None, description="Buscar en descripciones"),
    start_date: Optional[datetime] = Query(None, description="Fecha de inicio"),
    end_date: Optional[datetime] = Query(None, description="Fecha de fin"),
    current_user: dict = Depends(get_current_user),
    use_case: EventUseCase = Depends(get_event_use_case)
):
    """
    Endpoint para exportar eventos a Excel.
    
    Genera un archivo Excel con los eventos filtrados.
    
    Args:
        event_type: Tipo de evento a filtrar (opcional)
        description: Texto a buscar en descripciones (opcional)
        start_date: Fecha de inicio del rango (opcional)
        end_date: Fecha de fin del rango (opcional)
        current_user: Usuario actual autenticado
        use_case: Caso de uso de eventos
        
    Returns:
        Response: Archivo Excel con los eventos
    """
    # Obtener eventos con filtros
    event_type_enum = None
    if event_type:
        try:
            event_type_enum = EventType(event_type)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de evento inválido: {event_type}"
            )
    
    events = use_case.get_events(
        event_type=event_type_enum,
        description=description,
        start_date=start_date,
        end_date=end_date
    )
    
    # Exportar a Excel
    excel_content = use_case.export_to_excel(events)
    
    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=eventos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        }
    )

