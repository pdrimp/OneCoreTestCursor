"""
Esquemas de autenticación.

Define los DTOs para las operaciones de autenticación.
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """
    Esquema para la solicitud de inicio de sesión.

    Attributes:
        username: Nombre de usuario
        password: Contraseña en texto plano
    """
    username: str = Field(..., description="Nombre de usuario")
    password: str = Field(..., description="Contraseña", min_length=6)


class TokenResponse(BaseModel):
    """
    Esquema para la respuesta de token JWT.

    Attributes:
        access_token: Token JWT generado
        token_type: Tipo de token (siempre "bearer")
    """
    access_token: str = Field(..., description="Token JWT")
    token_type: str = Field(default="bearer", description="Tipo de token")
