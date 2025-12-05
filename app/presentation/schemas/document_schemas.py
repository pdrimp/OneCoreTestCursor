"""
Esquemas de documentos.

Define los DTOs para las operaciones con documentos.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class DocumentAnalysisResponse(BaseModel):
    """
    Esquema para la respuesta de análisis de documento.
    
    Attributes:
        document_id: ID del documento creado
        document_type: Tipo de documento (invoice/information)
        extracted_data: Datos extraídos por IA
        sentiment: Sentimiento detectado (solo para documentos de información)
    """
    document_id: int = Field(..., description="ID del documento")
    document_type: str = Field(..., description="Tipo de documento")
    extracted_data: Dict[str, Any] = Field(..., description="Datos extraídos")
    sentiment: Optional[str] = Field(None, description="Sentimiento detectado")


class InvoiceData(BaseModel):
    """
    Esquema para datos de factura extraídos.
    
    Attributes:
        customer: Información del cliente
        vendor: Información del proveedor
        invoice_number: Número de factura
        invoice_date: Fecha de la factura
        items: Lista de productos/servicios
        total: Total de la factura
    """
    customer: Dict[str, Any] = Field(..., description="Datos del cliente")
    vendor: Dict[str, Any] = Field(..., description="Datos del proveedor")
    invoice_number: Optional[str] = Field(None, description="Número de factura")
    invoice_date: Optional[str] = Field(None, description="Fecha de factura")
    items: list = Field(default_factory=list, description="Items de la factura")
    total: Optional[float] = Field(None, description="Total de la factura")


class InformationData(BaseModel):
    """
    Esquema para datos de documento de información extraídos.
    
    Attributes:
        description: Descripción del contenido
        summary: Resumen del contenido
        sentiment: Análisis de sentimiento (positivo, negativo, neutral)
    """
    description: str = Field(..., description="Descripción del contenido")
    summary: str = Field(..., description="Resumen del contenido")
    sentiment: str = Field(..., description="Sentimiento detectado")

