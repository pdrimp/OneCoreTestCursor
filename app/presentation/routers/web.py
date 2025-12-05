"""
Router para páginas web.

Sirve las páginas HTML de la interfaz web.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Configurar directorio de plantillas
templates_dir = os.path.join(os.path.dirname(__file__), "..", "..", "web", "templates")
templates = Jinja2Templates(directory=templates_dir)


@router.get("/web/documents", response_class=HTMLResponse)
async def documents_page(request: Request):
    """
    Endpoint para la página de análisis de documentos.
    
    Args:
        request: Request de FastAPI
        
    Returns:
        HTMLResponse: Página HTML de análisis de documentos
    """
    return templates.TemplateResponse("documents.html", {"request": request})


@router.get("/web/history", response_class=HTMLResponse)
async def history_page(request: Request):
    """
    Endpoint para la página de historial de eventos.
    
    Args:
        request: Request de FastAPI
        
    Returns:
        HTMLResponse: Página HTML de historial
    """
    return templates.TemplateResponse("history.html", {"request": request})

