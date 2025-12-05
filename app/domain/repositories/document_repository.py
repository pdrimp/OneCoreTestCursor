"""
Interfaz del repositorio de documentos.

Define el contrato que deben cumplir las implementaciones
del repositorio de documentos.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.document import Document


class IDocumentRepository(ABC):
    """
    Interfaz abstracta para el repositorio de documentos.

    Define los métodos que deben implementar los repositorios
    de documentos sin especificar la implementación concreta.
    """

    @abstractmethod
    def create(self, document: Document) -> Document:
        """
        Crea un nuevo documento en el repositorio.

        Args:
            document: Instancia de Document a crear

        Returns:
            Document: Documento creado con ID asignado
        """
        pass

    @abstractmethod
    def get_by_id(self, document_id: int) -> Optional[Document]:
        """
        Obtiene un documento por su ID.

        Args:
            document_id: Identificador único del documento

        Returns:
            Optional[Document]: Documento encontrado o None si no existe
        """
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Document]:
        """
        Obtiene todos los documentos de un usuario.

        Args:
            user_id: Identificador único del usuario

        Returns:
            List[Document]: Lista de documentos del usuario
        """
        pass

    @abstractmethod
    def get_by_type(self, document_type: str) -> List[Document]:
        """
        Obtiene todos los documentos de un tipo específico.

        Args:
            document_type: Tipo de documento a filtrar

        Returns:
            List[Document]: Lista de documentos del tipo especificado
        """
        pass

    @abstractmethod
    def update(self, document: Document) -> Document:
        """
        Actualiza un documento existente.

        Args:
            document: Instancia de Document con los datos actualizados

        Returns:
            Document: Documento actualizado
        """
        pass

    @abstractmethod
    def delete(self, document_id: int) -> bool:
        """
        Elimina un documento del repositorio.

        Args:
            document_id: Identificador único del documento a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        pass
