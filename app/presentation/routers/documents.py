"""
Router de documentos.

Define los endpoints relacionados con análisis de documentos con IA.
"""

import os
import tempfile
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.domain.repositories.document_repository import IDocumentRepository
from app.infrastructure.repositories.document_repository_impl import DocumentRepository
from app.application.use_cases.document_use_case import DocumentUseCase
from app.presentation.schemas.document_schemas import DocumentAnalysisResponse
from app.presentation.middleware.auth_middleware import get_current_user

router = APIRouter()

# Directorio para almacenar archivos temporalmente
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_document_use_case(db: Session = Depends(get_db)) -> DocumentUseCase:
    """
    Dependencia para obtener una instancia de DocumentUseCase.

    Args:
        db: Sesión de base de datos

    Returns:
        DocumentUseCase: Instancia del caso de uso de documentos
    """
    document_repository: IDocumentRepository = DocumentRepository(db)
    return DocumentUseCase(document_repository)


@router.post("/analyze", response_model=DocumentAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_document(
    file: UploadFile = File(..., description="Documento a analizar (PDF, JPG, PNG)"),
    current_user: dict = Depends(get_current_user),
    use_case: DocumentUseCase = Depends(get_document_use_case)
):
    """
    Endpoint para analizar un documento con IA.

    Clasifica el documento como Factura o Información y extrae los datos correspondientes
    utilizando Azure Cognitive Services.

    Args:
        file: Archivo a analizar (PDF, JPG o PNG)
        current_user: Usuario actual autenticado
        use_case: Caso de uso de documentos

    Returns:
        DocumentAnalysisResponse: Resultado del análisis con datos extraídos

    Raises:
        HTTPException: Si hay error al procesar el documento
    """
    # Validar tipo de archivo
    allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido. Permitidos: {', '.join(allowed_extensions)}"
        )

    # Guardar archivo temporalmente
    file_content = await file.read()
    temp_file_path = os.path.join(UPLOAD_DIR, f"temp_{current_user['id_usuario']}_{file.filename}")

    try:
        with open(temp_file_path, "wb") as f:
            f.write(file_content)

        # Analizar documento
        result = use_case.analyze_document(
            file_path=temp_file_path,
            filename=file.filename,
            user_id=current_user["id_usuario"]
        )

        return DocumentAnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al analizar el documento: {str(e)}"
        )
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
