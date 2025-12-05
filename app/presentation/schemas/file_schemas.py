"""
Esquemas de archivos.

Define los DTOs para las operaciones con archivos.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class FileUploadResponse(BaseModel):
    """
    Esquema para la respuesta de carga de archivo.
    
    Attributes:
        file_id: ID del archivo creado
        s3_url: URL del archivo en S3
        validations: Lista de validaciones aplicadas
        param1: Primer parámetro adicional
        param2: Segundo parámetro adicional
    """
    file_id: int = Field(..., description="ID del archivo")
    s3_url: str = Field(..., description="URL del archivo en S3")
    validations: List[Dict[str, Any]] = Field(default_factory=list, description="Lista de validaciones")
    param1: str = Field(..., description="Primer parámetro adicional")
    param2: str = Field(..., description="Segundo parámetro adicional")


class ValidationItem(BaseModel):
    """
    Esquema para un item de validación.
    
    Attributes:
        type: Tipo de validación (empty_value, duplicate, invalid_type, etc.)
        row: Número de fila (opcional)
        column: Nombre de columna (opcional)
        message: Mensaje descriptivo de la validación
    """
    type: str = Field(..., description="Tipo de validación")
    row: Optional[int] = Field(None, description="Número de fila")
    column: Optional[str] = Field(None, description="Nombre de columna")
    message: str = Field(..., description="Mensaje de validación")

