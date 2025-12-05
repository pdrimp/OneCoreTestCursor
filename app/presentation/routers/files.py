"""
Router de archivos.

Define los endpoints relacionados con carga y validación de archivos CSV.
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.domain.repositories.file_repository import IFileRepository
from app.infrastructure.repositories.file_repository_impl import FileRepository
from app.application.use_cases.file_use_case import FileUseCase
from app.presentation.schemas.file_schemas import FileUploadResponse
from app.presentation.middleware.auth_middleware import require_role

router = APIRouter()


def get_file_use_case(db: Session = Depends(get_db)) -> FileUseCase:
    """
    Dependencia para obtener una instancia de FileUseCase.

    Args:
        db: Sesión de base de datos

    Returns:
        FileUseCase: Instancia del caso de uso de archivos
    """
    file_repository: IFileRepository = FileRepository(db)
    return FileUseCase(file_repository)


@router.post("/upload", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(..., description="Archivo CSV a subir"),
    param1: str = Form(..., description="Primer parámetro adicional"),
    param2: str = Form(..., description="Segundo parámetro adicional"),
    current_user: dict = Depends(require_role("uploader")),  # Cambiar "uploader" por el rol requerido
    use_case: FileUseCase = Depends(get_file_use_case)
):
    """
    Endpoint para subir y validar un archivo CSV.

    Sube el archivo a AWS S3, procesa y guarda el contenido en SQL Server,
    y devuelve una lista de validaciones aplicadas al archivo.
    El acceso está limitado a usuarios con rol específico.

    Args:
        file: Archivo CSV a subir
        param1: Primer parámetro adicional
        param2: Segundo parámetro adicional
        current_user: Usuario actual autenticado (validado por middleware)
        use_case: Caso de uso de archivos

    Returns:
        FileUploadResponse: Información del archivo subido y validaciones

    Raises:
        HTTPException: Si hay error al procesar el archivo
    """
    # Validar que sea un archivo CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un CSV"
        )

    # Leer contenido del archivo
    file_content = await file.read()

    try:
        result = use_case.upload_and_validate_file(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type or "text/csv",
            user_id=current_user["id_usuario"],
            param1=param1,
            param2=param2
        )

        return FileUploadResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el archivo: {str(e)}"
        )
