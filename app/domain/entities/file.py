"""
Entidad de Archivo.

Define la estructura y comportamiento de los archivos cargados en el sistema.
"""

from typing import Optional, List
from datetime import datetime
from enum import Enum


class FileStatus(str, Enum):
    """Enum para el estado de procesamiento del archivo."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class File:
    """
    Entidad que representa un archivo cargado en el sistema.

    Attributes:
        id: Identificador único del archivo
        filename: Nombre original del archivo
        s3_key: Clave del archivo en S3
        s3_url: URL del archivo en S3
        file_size: Tamaño del archivo en bytes
        content_type: Tipo MIME del archivo
        status: Estado del procesamiento del archivo
        validations: Lista de validaciones aplicadas al archivo
        user_id: ID del usuario que cargó el archivo
        created_at: Fecha y hora de carga del archivo
        updated_at: Fecha y hora de última actualización
    """

    def __init__(
        self,
        id_: Optional[int] = None,
        filename: str = "",
        s3_key: str = "",
        s3_url: str = "",
        file_size: int = 0,
        content_type: str = "",
        status: FileStatus = FileStatus.PENDING,
        validations: Optional[List[dict]] = None,
        user_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Inicializa una instancia de File.

        Args:
            id_: Identificador único del archivo
            filename: Nombre original del archivo
            s3_key: Clave del archivo en S3
            s3_url: URL del archivo en S3
            file_size: Tamaño del archivo en bytes
            content_type: Tipo MIME del archivo
            status: Estado del procesamiento
            validations: Lista de validaciones aplicadas
            user_id: ID del usuario que cargó el archivo
            created_at: Fecha de creación
            updated_at: Fecha de actualización
        """
        self.id = id_
        self.filename = filename
        self.s3_key = s3_key
        self.s3_url = s3_url
        self.file_size = file_size
        self.content_type = content_type
        self.status = status
        self.validations = validations or []
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        """Representación en string del archivo."""
        return f"<File(id={self.id}, filename={self.filename}, status={self.status})>"
