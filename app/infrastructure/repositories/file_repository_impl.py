"""
Implementación del repositorio de archivos.

Implementa IFileRepository utilizando SQLAlchemy y SQL Server.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.file import File
from app.domain.repositories.file_repository import IFileRepository
from app.infrastructure.models.file_model import FileModel


class FileRepository(IFileRepository):
    """
    Implementación concreta del repositorio de archivos.

    Utiliza SQLAlchemy para interactuar con la base de datos SQL Server.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db: Sesión de SQLAlchemy para operaciones de base de datos
        """
        self.db = db

    def _to_entity(self, model: FileModel) -> File:
        """
        Convierte un modelo de SQLAlchemy a una entidad del dominio.

        Args:
            model: Instancia de FileModel

        Returns:
            File: Instancia de File del dominio
        """
        from app.domain.entities.file import FileStatus
        return File(
            id_=model.id,
            filename=model.filename,
            s3_key=model.s3_key,
            s3_url=model.s3_url,
            file_size=model.file_size,
            content_type=model.content_type,
            status=FileStatus(model.status) if model.status else FileStatus.PENDING,
            validations=model.validations,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: File) -> FileModel:
        """
        Convierte una entidad del dominio a un modelo de SQLAlchemy.

        Args:
            entity: Instancia de File del dominio

        Returns:
            FileModel: Instancia de FileModel para base de datos
        """
        return FileModel(
            id=entity.id,
            filename=entity.filename,
            s3_key=entity.s3_key,
            s3_url=entity.s3_url,
            file_size=entity.file_size,
            content_type=entity.content_type,
            status=entity.status.value if entity.status else "pending",
            validations=entity.validations,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def create(self, file: File) -> File:
        """
        Crea un nuevo archivo en la base de datos.

        Args:
            file: Instancia de File a crear

        Returns:
            File: Archivo creado con ID asignado
        """
        db_file = self._to_model(file)
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)
        return self._to_entity(db_file)

    def get_by_id(self, file_id: int) -> Optional[File]:
        """
        Obtiene un archivo por su ID.

        Args:
            file_id: Identificador único del archivo

        Returns:
            Optional[File]: Archivo encontrado o None si no existe
        """
        db_file = self.db.query(FileModel).filter(FileModel.id == file_id).first()
        return self._to_entity(db_file) if db_file else None

    def get_by_user_id(self, user_id: int) -> List[File]:
        """
        Obtiene todos los archivos de un usuario.

        Args:
            user_id: Identificador único del usuario

        Returns:
            List[File]: Lista de archivos del usuario
        """
        db_files = self.db.query(FileModel).filter(FileModel.user_id == user_id).all()
        return [self._to_entity(db_file) for db_file in db_files]

    def update(self, file: File) -> File:
        """
        Actualiza un archivo existente.

        Args:
            file: Instancia de File con los datos actualizados

        Returns:
            File: Archivo actualizado
        """
        db_file = self.db.query(FileModel).filter(FileModel.id == file.id).first()
        if db_file:
            db_file.filename = file.filename
            db_file.s3_key = file.s3_key
            db_file.s3_url = file.s3_url
            db_file.file_size = file.file_size
            db_file.content_type = file.content_type
            db_file.status = file.status.value if file.status else "pending"
            db_file.validations = file.validations
            db_file.updated_at = file.updated_at
            self.db.commit()
            self.db.refresh(db_file)
            return self._to_entity(db_file)
        return file

    def delete(self, file_id: int) -> bool:
        """
        Elimina un archivo de la base de datos.

        Args:
            file_id: Identificador único del archivo a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        db_file = self.db.query(FileModel).filter(FileModel.id == file_id).first()
        if db_file:
            self.db.delete(db_file)
            self.db.commit()
            return True
        return False
