"""
Interfaz del repositorio de usuarios.

Define el contrato que deben cumplir las implementaciones
del repositorio de usuarios.
"""

from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User


class IUserRepository(ABC):
    """
    Interfaz abstracta para el repositorio de usuarios.

    Define los métodos que deben implementar los repositorios
    de usuarios sin especificar la implementación concreta.
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """
        Crea un nuevo usuario en el repositorio.

        Args:
            user: Instancia de User a crear

        Returns:
            User: Usuario creado con ID asignado
        """
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: Identificador único del usuario

        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Obtiene un usuario por su nombre de usuario.

        Args:
            username: Nombre de usuario

        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su correo electrónico.

        Args:
            email: Correo electrónico del usuario

        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Actualiza un usuario existente.

        Args:
            user: Instancia de User con los datos actualizados

        Returns:
            User: Usuario actualizado
        """
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario del repositorio.

        Args:
            user_id: Identificador único del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        pass
