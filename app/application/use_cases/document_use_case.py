"""
Caso de uso de documentos.

Implementa la lógica de negocio para el análisis de documentos con IA.
"""

from typing import Dict, Any
import os
from app.domain.entities.document import Document, DocumentType
from app.domain.repositories.document_repository import IDocumentRepository
from app.infrastructure.services.azure_service import AzureService


class DocumentUseCase:
    """
    Caso de uso para análisis de documentos con IA.

    Implementa la lógica de negocio para:
    - Clasificar documentos (Factura/Información)
    - Extraer datos de documentos
    - Analizar sentimientos
    """

    def __init__(self, document_repository: IDocumentRepository):
        """
        Inicializa el caso de uso con sus dependencias.

        Args:
            document_repository: Repositorio de documentos para acceso a datos
        """
        self.document_repository = document_repository
        self.azure_service = AzureService()

    def analyze_document(
        self,
        file_path: str,
        filename: str,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Analiza un documento utilizando Azure Cognitive Services.

        Args:
            file_path: Ruta del archivo a analizar
            filename: Nombre original del archivo
            user_id: ID del usuario que carga el documento

        Returns:
            Dict[str, Any]: Diccionario con:
                - document_id: ID del documento creado
                - document_type: Tipo de documento detectado
                - extracted_data: Datos extraídos
                - sentiment: Sentimiento (solo para documentos de información)
        """
        # Analizar documento con Azure
        analysis_result = self.azure_service.analyze_document(file_path)

        # Determinar tipo de documento
        document_type = DocumentType.INVOICE if analysis_result.get("document_type") == "invoice" else DocumentType.INFORMATION

        # Extraer datos según el tipo
        extracted_data = analysis_result
        sentiment = analysis_result.get("sentiment") if document_type == DocumentType.INFORMATION else None

        # Crear entidad Document
        document = Document(
            filename=filename,
            document_type=document_type,
            file_path=file_path,
            extracted_data=extracted_data,
            sentiment=sentiment,
            user_id=user_id
        )

        # Guardar en base de datos
        saved_document = self.document_repository.create(document)

        return {
            "document_id": saved_document.id,
            "document_type": saved_document.document_type.value,
            "extracted_data": saved_document.extracted_data,
            "sentiment": saved_document.sentiment
        }
