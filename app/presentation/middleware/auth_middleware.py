"""
Middleware de autenticación.

Proporciona funciones de dependencia para validar tokens JWT
y verificar roles de usuario.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.services.jwt_service import JWTService
from app.infrastructure.database import get_db
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.repositories.user_repository_impl import UserRepository
from sqlalchemy.orm import Session

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> dict:
    """
    Dependencia de FastAPI para obtener el usuario actual desde el token JWT.
    
    Args:
        credentials: Credenciales HTTP con el token Bearer
        db: Sesión de base de datos
        
    Returns:
        dict: Payload del token JWT con información del usuario
        
    Raises:
        HTTPException: Si el token es inválido o no está presente
    """
    token = credentials.credentials
    payload = JWTService.decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload


def require_role(required_role: str):
    """
    Factory function que crea una dependencia para verificar roles de usuario.
    
    Args:
        required_role: Rol requerido para acceder al endpoint
        
    Returns:
        function: Función de dependencia de FastAPI
    """
    def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        """
        Verifica que el usuario tenga el rol requerido.
        
        Args:
            current_user: Payload del token JWT del usuario actual
            
        Returns:
            dict: Payload del usuario si tiene el rol requerido
            
        Raises:
            HTTPException: Si el usuario no tiene el rol requerido
        """
        user_role = current_user.get("rol")
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol: {required_role}"
            )
        return current_user
    
    return role_checker

