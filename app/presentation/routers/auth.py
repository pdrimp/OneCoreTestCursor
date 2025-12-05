"""
Router de autenticación.

Define los endpoints relacionados con autenticación de usuarios.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.repositories.user_repository_impl import UserRepository
from app.application.use_cases.auth_use_case import AuthUseCase
from app.presentation.schemas.auth_schemas import LoginRequest, TokenResponse

router = APIRouter()


def get_auth_use_case(db: Session = Depends(get_db)) -> AuthUseCase:
    """
    Dependencia para obtener una instancia de AuthUseCase.

    Args:
        db: Sesión de base de datos

    Returns:
        AuthUseCase: Instancia del caso de uso de autenticación
    """
    user_repository: IUserRepository = UserRepository(db)
    return AuthUseCase(user_repository)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    login_request: LoginRequest,
    use_case: AuthUseCase = Depends(get_auth_use_case)
):
    """
    Endpoint para iniciar sesión.

    Permite a usuarios anónimos iniciar sesión con username y password.
    Devuelve un JWT firmado con id_usuario, rol y tiempo de expiración de 15 minutos.

    Args:
        login_request: Datos de inicio de sesión (username y password)
        use_case: Caso de uso de autenticación

    Returns:
        TokenResponse: Token JWT y tipo de token

    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    result = use_case.login(login_request.username, login_request.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    return TokenResponse(**result)
