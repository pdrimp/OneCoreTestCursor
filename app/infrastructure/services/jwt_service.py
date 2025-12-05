"""
Servicio de autenticación JWT.

Proporciona funcionalidades para crear, validar y renovar tokens JWT.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from app.infrastructure.config import settings


class JWTService:
    """
    Servicio para manejo de tokens JWT.

    Proporciona métodos para crear, decodificar y validar tokens JWT
    utilizados para autenticación en la API.
    """

    @staticmethod
    def create_token(data: Dict[str, any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Crea un token JWT firmado con los datos proporcionados.

        Args:
            data: Diccionario con los datos a incluir en el token (ej: id_usuario, rol)
            expires_delta: Tiempo de expiración del token. Si es None, usa el valor por defecto

        Returns:
            str: Token JWT codificado y firmado
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, any]]:
        """
        Decodifica y valida un token JWT.

        Args:
            token: Token JWT a decodificar

        Returns:
            Optional[Dict[str, any]]: Payload del token si es válido, None si es inválido o expirado
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    def verify_token(token: str) -> bool:
        """
        Verifica si un token JWT es válido y no ha expirado.

        Args:
            token: Token JWT a verificar

        Returns:
            bool: True si el token es válido, False en caso contrario
        """
        payload = JWTService.decode_token(token)
        return payload is not None

    @staticmethod
    def renew_token(token: str, additional_minutes: int = 15) -> Optional[str]:
        """
        Renueva un token JWT generando uno nuevo con tiempo de expiración adicional.

        Args:
            token: Token JWT original a renovar
            additional_minutes: Minutos adicionales de expiración para el nuevo token

        Returns:
            Optional[str]: Nuevo token JWT si el token original es válido, None en caso contrario
        """
        payload = JWTService.decode_token(token)
        if payload:
            # Remover la expiración del payload original
            payload.pop("exp", None)
            # Crear nuevo token con tiempo adicional
            new_expires_delta = timedelta(minutes=additional_minutes)
            return JWTService.create_token(payload, new_expires_delta)
        return None
