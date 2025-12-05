"""
Caso de uso de archivos.

Implementa la lógica de negocio para la carga y validación de archivos CSV.
"""

import csv
import io
from typing import List, Dict, Any
from datetime import datetime
from app.domain.entities.file import File, FileStatus
from app.domain.repositories.file_repository import IFileRepository
from app.infrastructure.services.s3_service import S3Service


class FileUseCase:
    """
    Caso de uso para gestión de archivos CSV.
    
    Implementa la lógica de negocio para:
    - Subir archivos a S3
    - Validar contenido de archivos CSV
    - Almacenar información en base de datos
    """
    
    def __init__(self, file_repository: IFileRepository):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            file_repository: Repositorio de archivos para acceso a datos
        """
        self.file_repository = file_repository
        self.s3_service = S3Service()
    
    def upload_and_validate_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        user_id: int,
        param1: str,
        param2: str
    ) -> Dict[str, Any]:
        """
        Sube un archivo CSV a S3, lo valida y almacena en la base de datos.
        
        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre original del archivo
            content_type: Tipo MIME del archivo
            user_id: ID del usuario que carga el archivo
            param1: Primer parámetro adicional
            param2: Segundo parámetro adicional
            
        Returns:
            Dict[str, Any]: Diccionario con:
                - file_id: ID del archivo creado
                - s3_url: URL del archivo en S3
                - validations: Lista de validaciones aplicadas
        """
        # Generar clave única para S3
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        s3_key = f"uploads/{user_id}/{timestamp}_{filename}"
        
        # Subir archivo a S3
        file_obj = io.BytesIO(file_content)
        s3_url = self.s3_service.upload_file(file_obj, s3_key, content_type)
        
        if not s3_url:
            raise Exception("Error al subir archivo a S3")
        
        # Validar contenido del CSV
        validations = self._validate_csv(file_content)
        
        # Crear entidad File
        file_entity = File(
            filename=filename,
            s3_key=s3_key,
            s3_url=s3_url,
            file_size=len(file_content),
            content_type=content_type,
            status=FileStatus.COMPLETED if not validations else FileStatus.PENDING,
            validations=validations,
            user_id=user_id
        )
        
        # Guardar en base de datos
        saved_file = self.file_repository.create(file_entity)
        
        return {
            "file_id": saved_file.id,
            "s3_url": saved_file.s3_url,
            "validations": saved_file.validations,
            "param1": param1,
            "param2": param2
        }
    
    def _validate_csv(self, file_content: bytes) -> List[Dict[str, Any]]:
        """
        Valida el contenido de un archivo CSV.
        
        Args:
            file_content: Contenido del archivo en bytes
            
        Returns:
            List[Dict[str, Any]]: Lista de validaciones encontradas.
                                 Lista vacía si no hay errores.
        """
        validations = []
        
        try:
            # Decodificar contenido
            content = file_content.decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(content))
            
            rows = list(csv_reader)
            seen_rows = set()
            
            for row_num, row in enumerate(rows, start=2):  # Empezar en 2 (después del header)
                row_key = tuple(row.values())
                
                # Validar valores vacíos
                for col, value in row.items():
                    if not value or value.strip() == "":
                        validations.append({
                            "type": "empty_value",
                            "row": row_num,
                            "column": col,
                            "message": f"Valor vacío en fila {row_num}, columna {col}"
                        })
                
                # Validar duplicados
                if row_key in seen_rows:
                    validations.append({
                        "type": "duplicate",
                        "row": row_num,
                        "message": f"Fila duplicada en la línea {row_num}"
                    })
                else:
                    seen_rows.add(row_key)
                
                # Validar tipos de datos (ejemplo: números)
                for col, value in row.items():
                    if value and value.strip():
                        # Intentar validar como número si el nombre de columna sugiere que debería ser numérico
                        if any(keyword in col.lower() for keyword in ['precio', 'cantidad', 'total', 'amount', 'price', 'quantity']):
                            try:
                                float(value.replace(',', '.'))
                            except ValueError:
                                validations.append({
                                    "type": "invalid_type",
                                    "row": row_num,
                                    "column": col,
                                    "message": f"Valor no numérico en fila {row_num}, columna {col}: {value}"
                                })
        
        except Exception as e:
            validations.append({
                "type": "parse_error",
                "message": f"Error al procesar el archivo CSV: {str(e)}"
            })
        
        return validations

