"""
Caso de uso de autenticación.

Implementa la lógica de negocio para el inicio de sesión de usuarios.
"""

from typing import Optional, Dict
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.services.password_service import PasswordService
from app.infrastructure.services.jwt_service import JWTService


class AuthUseCase:
    """
    Caso de uso para autenticación de usuarios.

    Implementa la lógica de negocio para:
    - Validar credenciales de usuario
    - Generar tokens JWT
    """

    def __init__(self, user_repository: IUserRepository):
        """
        Inicializa el caso de uso con sus dependencias.

        Args:
            user_repository: Repositorio de usuarios para acceso a datos
        """
        self.user_repository = user_repository
        self.password_service = PasswordService()
        self.jwt_service = JWTService()

    def login(self, username: str, password: str) -> Optional[Dict[str, str]]:
        """
        Autentica un usuario y genera un token JWT.

        Args:
            username: Nombre de usuario
            password: Contraseña en texto plano

        Returns:
            Optional[Dict[str, str]]: Diccionario con el token JWT y tipo si la autenticación es exitosa,
                                     None si las credenciales son inválidas
        """
        # Buscar usuario por username
        user = self.user_repository.get_by_username(username)

        if not user:
            return None

        # Verificar si el usuario está activo
        if not user.is_active:
            return None

        # Verificar contraseña
        if not self.password_service.verify_password(password, user.password_hash):
            return None

        # Generar token JWT
        token_data = {
            "id_usuario": user.id,
            "rol": user.role,
            "sub": username
        }
        token = self.jwt_service.create_token(token_data)

        return {
            "access_token": token,
            "token_type": "bearer"
        }
