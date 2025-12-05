"""
Servicio de almacenamiento en AWS S3.

Proporciona funcionalidades para subir, descargar y gestionar archivos en S3.
"""

import boto3
from botocore.exceptions import ClientError
from typing import Optional, BinaryIO
from app.infrastructure.config import settings


class S3Service:
    """
    Servicio para interactuar con AWS S3.
    
    Proporciona métodos para subir archivos a S3 y obtener URLs de acceso.
    """
    
    def __init__(self):
        """
        Inicializa el cliente de S3 con las credenciales configuradas.
        """
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME
    
    def upload_file(self, file_obj: BinaryIO, s3_key: str, content_type: str) -> Optional[str]:
        """
        Sube un archivo a S3.
        
        Args:
            file_obj: Objeto de archivo a subir (file-like object)
            s3_key: Clave única del archivo en S3 (ruta/nombre)
            content_type: Tipo MIME del archivo
            
        Returns:
            Optional[str]: URL del archivo en S3 si la subida fue exitosa, None en caso contrario
        """
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs={'ContentType': content_type}
            )
            # Generar URL del archivo
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
            return url
        except ClientError as e:
            print(f"Error al subir archivo a S3: {e}")
            return None
    
    def delete_file(self, s3_key: str) -> bool:
        """
        Elimina un archivo de S3.
        
        Args:
            s3_key: Clave del archivo en S3 a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            print(f"Error al eliminar archivo de S3: {e}")
            return False
    
    def get_file_url(self, s3_key: str, expires_in: int = 3600) -> Optional[str]:
        """
        Genera una URL firmada temporal para acceder a un archivo en S3.
        
        Args:
            s3_key: Clave del archivo en S3
            expires_in: Tiempo de expiración de la URL en segundos (por defecto 1 hora)
            
        Returns:
            Optional[str]: URL firmada si el archivo existe, None en caso contrario
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            print(f"Error al generar URL de S3: {e}")
            return None

