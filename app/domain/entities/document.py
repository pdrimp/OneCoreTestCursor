"""
Entidad de Documento.

Define la estructura y comportamiento de los documentos analizados con IA.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    """Enum para el tipo de documento."""
    INVOICE = "invoice"
    INFORMATION = "information"
    UNKNOWN = "unknown"


class Document:
    """
    Entidad que representa un documento analizado con IA.
    
    Attributes:
        id: Identificador único del documento
        filename: Nombre del archivo del documento
        document_type: Tipo de documento (Factura o Información)
        file_path: Ruta del archivo en el sistema
        extracted_data: Datos extraídos por IA (estructura varía según tipo)
        sentiment: Análisis de sentimiento (solo para documentos de información)
        user_id: ID del usuario que cargó el documento
        created_at: Fecha y hora de carga del documento
        updated_at: Fecha y hora de última actualización
    """
    
    def __init__(
        self,
        id: Optional[int] = None,
        filename: str = "",
        document_type: DocumentType = DocumentType.UNKNOWN,
        file_path: str = "",
        extracted_data: Optional[Dict[str, Any]] = None,
        sentiment: Optional[str] = None,
        user_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Inicializa una instancia de Document.
        
        Args:
            id: Identificador único del documento
            filename: Nombre del archivo
            document_type: Tipo de documento
            file_path: Ruta del archivo
            extracted_data: Datos extraídos por IA
            sentiment: Análisis de sentimiento
            user_id: ID del usuario
            created_at: Fecha de creación
            updated_at: Fecha de actualización
        """
        self.id = id
        self.filename = filename
        self.document_type = document_type
        self.file_path = file_path
        self.extracted_data = extracted_data or {}
        self.sentiment = sentiment
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def __repr__(self) -> str:
        """Representación en string del documento."""
        return f"<Document(id={self.id}, filename={self.filename}, type={self.document_type})>"

