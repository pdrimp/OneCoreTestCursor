"""
Implementación del repositorio de usuarios.

Implementa IUserRepository utilizando SQLAlchemy y SQL Server.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.models.user_model import UserModel


class UserRepository(IUserRepository):
    """
    Implementación concreta del repositorio de usuarios.

    Utiliza SQLAlchemy para interactuar con la base de datos SQL Server.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db: Sesión de SQLAlchemy para operaciones de base de datos
        """
        self.db = db

    def _to_entity(self, model: UserModel) -> User:
        """
        Convierte un modelo de SQLAlchemy a una entidad del dominio.

        Args:
            model: Instancia de UserModel

        Returns:
            User: Instancia de User del dominio
        """
        return User(
            id_=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            role=model.role,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: User) -> UserModel:
        """
        Convierte una entidad del dominio a un modelo de SQLAlchemy.

        Args:
            entity: Instancia de User del dominio

        Returns:
            UserModel: Instancia de UserModel para base de datos
        """
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            password_hash=entity.password_hash,
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def create(self, user: User) -> User:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            user: Instancia de User a crear

        Returns:
            User: Usuario creado con ID asignado
        """
        db_user = self._to_model(user)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self._to_entity(db_user)

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: Identificador único del usuario

        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_entity(db_user) if db_user else None

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Obtiene un usuario por su nombre de usuario.

        Args:
            username: Nombre de usuario

        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        db_user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(db_user) if db_user else None

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su correo electrónico.

        Args:
            email: Correo electrónico del usuario

        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(db_user) if db_user else None

    def update(self, user: User) -> User:
        """
        Actualiza un usuario existente.

        Args:
            user: Instancia de User con los datos actualizados

        Returns:
            User: Usuario actualizado
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if db_user:
            db_user.username = user.username
            db_user.email = user.email
            db_user.password_hash = user.password_hash
            db_user.role = user.role
            db_user.is_active = user.is_active
            db_user.updated_at = user.updated_at
            self.db.commit()
            self.db.refresh(db_user)
            return self._to_entity(db_user)
        return user

    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario de la base de datos.

        Args:
            user_id: Identificador único del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False
