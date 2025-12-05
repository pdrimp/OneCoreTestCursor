"""
Servicio de Azure Cognitive Services.

Proporciona funcionalidades para análisis de documentos utilizando
Azure Form Recognizer y Text Analytics.
"""

from typing import Dict, Any, Optional
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from app.infrastructure.config import settings


class AzureService:
    """
    Servicio para interactuar con Azure Cognitive Services.

    Proporciona métodos para:
    - Analizar documentos con Form Recognizer
    - Analizar sentimientos con Text Analytics
    """

    def __init__(self):
        """
        Inicializa los clientes de Azure Cognitive Services.
        """
        self.form_recognizer_client = DocumentAnalysisClient(
            endpoint=settings.AZURE_FORM_RECOGNIZER_ENDPOINT,
            credential=AzureKeyCredential(settings.AZURE_FORM_RECOGNIZER_KEY)
        )
        self.text_analytics_client = TextAnalyticsClient(
            endpoint=settings.AZURE_TEXT_ANALYTICS_ENDPOINT,
            credential=AzureKeyCredential(settings.AZURE_TEXT_ANALYTICS_KEY)
        )

    def analyze_document(self, file_path: str) -> Dict[str, Any]:
        """
        Analiza un documento utilizando Azure Form Recognizer.

        Determina si es una factura o documento de información y extrae
        los datos correspondientes.

        Args:
            file_path: Ruta del archivo a analizar

        Returns:
            Dict[str, Any]: Diccionario con:
                - document_type: Tipo de documento (invoice/information)
                - extracted_data: Datos extraídos según el tipo
        """
        try:
            with open(file_path, "rb") as f:
                poller = self.form_recognizer_client.begin_analyze_document(
                    "prebuilt-invoice",
                    document=f
                )
                result = poller.result()

            # Intentar analizar como factura
            if result.documents:
                return self._extract_invoice_data(result)
            else:
                # Si no es factura, analizar como documento de información
                return self._analyze_information_document(file_path)
        except Exception as e:
            # Si falla el análisis de factura, intentar como información
            print(f"Error analizando como factura: {e}")
            return self._analyze_information_document(file_path)

    def _extract_invoice_data(self, result) -> Dict[str, Any]:
        """
        Extrae datos de una factura analizada.

        Args:
            result: Resultado del análisis de Form Recognizer

        Returns:
            Dict[str, Any]: Datos extraídos de la factura
        """
        doc = result.documents[0]
        fields = doc.fields

        extracted_data = {
            "document_type": "invoice",
            "customer": {
                "name": fields.get("CustomerName", {}).value if fields.get("CustomerName") else None,
                "address": fields.get("CustomerAddress", {}).value if fields.get("CustomerAddress") else None
            },
            "vendor": {
                "name": fields.get("VendorName", {}).value if fields.get("VendorName") else None,
                "address": fields.get("VendorAddress", {}).value if fields.get("VendorAddress") else None
            },
            "invoice_number": fields.get("InvoiceId", {}).value if fields.get("InvoiceId") else None,
            "invoice_date": str(fields.get("InvoiceDate", {}).value) if fields.get("InvoiceDate") else None,
            "items": [],
            "total": float(fields.get("InvoiceTotal", {}).value) if fields.get("InvoiceTotal") else None
        }

        # Extraer items de la factura
        if fields.get("Items"):
            items = fields.get("Items").value
            for item in items:
                item_data = {
                    "quantity": float(item.value.get("Quantity", {}).value) if item.value.get("Quantity") else None,
                    "name": item.value.get("Description", {}).value if item.value.get("Description") else None,
                    "unit_price": float(item.value.get("UnitPrice", {}).value) if item.value.get("UnitPrice") else None,
                    "total": float(item.value.get("Amount", {}).value) if item.value.get("Amount") else None
                }
                extracted_data["items"].append(item_data)

        return extracted_data

    def _analyze_information_document(self, file_path: str) -> Dict[str, Any]:
        """
        Analiza un documento de información general.

        Args:
            file_path: Ruta del archivo a analizar

        Returns:
            Dict[str, Any]: Datos extraídos del documento de información
        """
        # Leer el contenido del documento
        # Nota: Para PDFs, necesitarías una librería adicional como PyPDF2
        # Por simplicidad, aquí se muestra la estructura

        with open(file_path, "rb") as f:
            # Analizar con modelo genérico
            poller = self.form_recognizer_client.begin_analyze_document(
                "prebuilt-read",
                document=f
            )
            result = poller.result()

        # Extraer texto
        text_content = ""
        for page in result.pages:
            for line in page.lines:
                text_content += line.content + "\n"

        # Analizar sentimiento
        sentiment = self._analyze_sentiment(text_content)

        return {
            "document_type": "information",
            "description": text_content[:500] if text_content else "",  # Primeros 500 caracteres
            "summary": text_content[:200] if text_content else "",  # Resumen corto
            "sentiment": sentiment
        }

    def _analyze_sentiment(self, text: str) -> str:
        """
        Analiza el sentimiento de un texto.

        Args:
            text: Texto a analizar

        Returns:
            str: Sentimiento detectado (positive, negative, neutral)
        """
        if not text or len(text.strip()) < 10:
            return "neutral"

        try:
            # Limitar el texto a 5120 caracteres (límite de Azure)
            text_to_analyze = text[:5120]
            documents = [text_to_analyze]

            response = self.text_analytics_client.analyze_sentiment(
                documents=documents,
                language="es"
            )

            if response and len(response) > 0:
                sentiment = response[0].sentiment
                return sentiment.lower()
            return "neutral"
        except Exception as e:
            print(f"Error analizando sentimiento: {e}")
            return "neutral"
