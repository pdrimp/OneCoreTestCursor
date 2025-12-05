"""
Módulo principal de la aplicación FastAPI.

Este módulo configura e inicia la aplicación FastAPI, incluyendo:
- Configuración de CORS
- Registro de routers
- Middleware de autenticación
- Manejo de excepciones globales
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.routers import auth, files, tokens, documents, history, web
from app.infrastructure.database import engine, Base
from app.infrastructure.config import settings

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API para análisis de documentos con IA utilizando Azure Cognitive Services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(files.router, prefix="/api/files", tags=["Archivos"])
app.include_router(tokens.router, prefix="/api/tokens", tags=["Tokens"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documentos"])
app.include_router(history.router, prefix="/api/history", tags=["Historial"])
app.include_router(web.router, tags=["Web"])


@app.get("/")
async def root():
    """
    Endpoint raíz de la API.

    Returns:
        dict: Mensaje de bienvenida con información de la API
    """
    return {
        "message": "API de Análisis de Documentos con IA",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud de la API.

    Returns:
        dict: Estado de la API
    """
    return {"status": "healthy"}
