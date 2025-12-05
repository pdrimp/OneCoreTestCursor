"""
Entidad de Usuario.

Define la estructura y comportamiento del usuario en el dominio de la aplicación.
"""

from typing import Optional
from datetime import datetime


class User:
    """
    Entidad que representa un usuario en el sistema.

    Attributes:
        id: Identificador único del usuario
        username: Nombre de usuario para autenticación
        email: Correo electrónico del usuario
        password_hash: Hash de la contraseña (nunca se almacena en texto plano)
        role: Rol del usuario en el sistema (ej: 'admin', 'user', 'uploader')
        is_active: Indica si el usuario está activo
        created_at: Fecha y hora de creación del usuario
        updated_at: Fecha y hora de última actualización
    """

    def __init__(
        self,
        id_: Optional[int] = None,
        username: str = "",
        email: str = "",
        password_hash: str = "",
        role: str = "user",
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        """
        Inicializa una instancia de User.

        Args:
            id_: Identificador único del usuario
            username: Nombre de usuario
            email: Correo electrónico
            password_hash: Hash de la contraseña
            role: Rol del usuario
            is_active: Estado activo del usuario
            created_at: Fecha de creación
            updated_at: Fecha de actualización
        """
        self.id = id_
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self) -> str:
        """Representación en string del usuario."""
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
