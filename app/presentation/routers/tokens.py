"""
Router de tokens.

Define los endpoints relacionados con renovación de tokens JWT.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from app.application.use_cases.token_use_case import TokenUseCase
from app.presentation.schemas.auth_schemas import TokenResponse
from app.presentation.middleware.auth_middleware import get_current_user, security

router = APIRouter()


def get_token_use_case() -> TokenUseCase:
    """
    Dependencia para obtener una instancia de TokenUseCase.
    
    Returns:
        TokenUseCase: Instancia del caso de uso de tokens
    """
    return TokenUseCase()


@router.post("/renew", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def renew_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: dict = Depends(get_current_user),
    use_case: TokenUseCase = Depends(get_token_use_case)
):
    """
    Endpoint para renovar un token JWT.
    
    Genera un nuevo token con tiempo de expiración adicional (15 minutos por defecto).
    Solo puede ser accedido si el token original aún no ha expirado.
    
    Args:
        credentials: Credenciales HTTP con el token Bearer
        current_user: Usuario actual autenticado (validado por middleware)
        use_case: Caso de uso de tokens
        
    Returns:
        TokenResponse: Nuevo token JWT y tipo de token
        
    Raises:
        HTTPException: Si el token es inválido o ha expirado
    """
    # Obtener el token original del header
    original_token = credentials.credentials
    
    # Renovar el token usando el caso de uso
    result = use_case.renew_token(original_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo renovar el token. El token puede haber expirado."
        )
    
    return TokenResponse(**result)

