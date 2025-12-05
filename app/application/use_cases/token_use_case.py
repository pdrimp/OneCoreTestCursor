"""
Caso de uso de tokens.

Implementa la lógica de negocio para la renovación de tokens JWT.
"""

from typing import Optional, Dict
from app.infrastructure.services.jwt_service import JWTService


class TokenUseCase:
    """
    Caso de uso para renovación de tokens JWT.
    
    Implementa la lógica de negocio para:
    - Validar tokens existentes
    - Renovar tokens con tiempo adicional de expiración
    """
    
    def __init__(self):
        """
        Inicializa el caso de uso con sus dependencias.
        """
        self.jwt_service = JWTService()
    
    def renew_token(self, token: str, additional_minutes: int = 15) -> Optional[Dict[str, str]]:
        """
        Renueva un token JWT generando uno nuevo con tiempo adicional.
        
        Args:
            token: Token JWT original a renovar
            additional_minutes: Minutos adicionales de expiración (por defecto 15)
            
        Returns:
            Optional[Dict[str, str]]: Diccionario con el nuevo token si el original es válido,
                                     None si el token es inválido o ha expirado
        """
        # Verificar que el token sea válido
        if not self.jwt_service.verify_token(token):
            return None
        
        # Renovar el token
        new_token = self.jwt_service.renew_token(token, additional_minutes)
        
        if not new_token:
            return None
        
        return {
            "access_token": new_token,
            "token_type": "bearer"
        }

