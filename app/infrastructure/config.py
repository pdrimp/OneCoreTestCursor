"""
Módulo de configuración de la aplicación.

Este módulo carga y gestiona todas las variables de entorno necesarias
para el funcionamiento de la aplicación, incluyendo:
- Configuración de base de datos
- Configuración de JWT
- Configuración de AWS S3
- Configuración de Azure Cognitive Services
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Clase de configuración que hereda de BaseSettings de Pydantic.
    
    Esta clase gestiona todas las variables de entorno de la aplicación.
    Utiliza Pydantic para validación automática de tipos.
    """
    
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 15
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str
    
    # Azure Cognitive Services
    AZURE_FORM_RECOGNIZER_ENDPOINT: str
    AZURE_FORM_RECOGNIZER_KEY: str
    AZURE_TEXT_ANALYTICS_ENDPOINT: str
    AZURE_TEXT_ANALYTICS_KEY: str
    
    # Application
    APP_NAME: str = "Document Analysis API"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

