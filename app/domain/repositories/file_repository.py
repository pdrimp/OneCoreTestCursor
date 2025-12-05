"""
Interfaz del repositorio de archivos.

Define el contrato que deben cumplir las implementaciones
del repositorio de archivos.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.file import File


class IFileRepository(ABC):
    """
    Interfaz abstracta para el repositorio de archivos.

    Define los métodos que deben implementar los repositorios
    de archivos sin especificar la implementación concreta.
    """

    @abstractmethod
    def create(self, file: File) -> File:
        """
        Crea un nuevo archivo en el repositorio.

        Args:
            file: Instancia de File a crear

        Returns:
            File: Archivo creado con ID asignado
        """
        pass

    @abstractmethod
    def get_by_id(self, file_id: int) -> Optional[File]:
        """
        Obtiene un archivo por su ID.

        Args:
            file_id: Identificador único del archivo

        Returns:
            Optional[File]: Archivo encontrado o None si no existe
        """
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[File]:
        """
        Obtiene todos los archivos de un usuario.

        Args:
            user_id: Identificador único del usuario

        Returns:
            List[File]: Lista de archivos del usuario
        """
        pass

    @abstractmethod
    def update(self, file: File) -> File:
        """
        Actualiza un archivo existente.

        Args:
            file: Instancia de File con los datos actualizados

        Returns:
            File: Archivo actualizado
        """
        pass

    @abstractmethod
    def delete(self, file_id: int) -> bool:
        """
        Elimina un archivo del repositorio.

        Args:
            file_id: Identificador único del archivo a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        pass
