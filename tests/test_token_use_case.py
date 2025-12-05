"""
Pruebas unitarias para TokenUseCase.

Contiene al menos 10 casos de prueba para cada método del caso de uso de tokens.
"""

import pytest
from datetime import timedelta
from app.application.use_cases.token_use_case import TokenUseCase
from app.infrastructure.services.jwt_service import JWTService
from app.infrastructure.config import settings


@pytest.fixture
def token_use_case():
    """Fixture para crear una instancia de TokenUseCase."""
    return TokenUseCase()


@pytest.fixture
def valid_token():
    """Fixture para crear un token JWT válido."""
    jwt_service = JWTService()
    token_data = {
        "id_usuario": 1,
        "rol": "user",
        "sub": "test_user"
    }
    return jwt_service.create_token(token_data)


class TestTokenUseCaseRenewToken:
    """Clase de pruebas para el método renew_token."""

    def test_renew_valid_token_success(self, token_use_case, valid_token):
        """Prueba renovación exitosa de token válido."""
        result = token_use_case.renew_token(valid_token)

        assert result is not None
        assert "access_token" in result
        assert "token_type" in result
        assert result["token_type"] == "bearer"

    def test_renew_token_different_token(self, token_use_case, valid_token):
        """Prueba que el nuevo token es diferente al original."""
        result = token_use_case.renew_token(valid_token)
        new_token = result["access_token"]

        assert new_token != valid_token

    def test_renew_token_contains_same_data(self, token_use_case, valid_token):
        """Prueba que el nuevo token contiene los mismos datos del usuario."""
        jwt_service = JWTService()
        original_payload = jwt_service.decode_token(valid_token)

        result = token_use_case.renew_token(valid_token)
        new_payload = jwt_service.decode_token(result["access_token"])

        assert new_payload["id_usuario"] == original_payload["id_usuario"]
        assert new_payload["rol"] == original_payload["rol"]
        assert new_payload["sub"] == original_payload["sub"]

    def test_renew_token_custom_minutes(self, token_use_case, valid_token):
        """Prueba renovación con minutos personalizados."""
        result = token_use_case.renew_token(valid_token, additional_minutes=30)

        assert result is not None
        jwt_service = JWTService()
        payload = jwt_service.decode_token(result["access_token"])
        assert payload is not None

    def test_renew_invalid_token(self, token_use_case):
        """Prueba renovación de token inválido."""
        invalid_token = "invalid.token.here"
        result = token_use_case.renew_token(invalid_token)

        assert result is None

    def test_renew_expired_token(self, token_use_case):
        """Prueba renovación de token expirado."""
        jwt_service = JWTService()
        # Crear token con expiración inmediata
        token_data = {
            "id_usuario": 1,
            "rol": "user",
            "sub": "test_user"
        }
        expired_token = jwt_service.create_token(token_data, timedelta(seconds=-1))

        result = token_use_case.renew_token(expired_token)

        assert result is None

    def test_renew_empty_token(self, token_use_case):
        """Prueba renovación con token vacío."""
        result = token_use_case.renew_token("")

        assert result is None

    def test_renew_token_none(self, token_use_case):
        """Prueba renovación con None."""
        result = token_use_case.renew_token(None)

        assert result is None

    def test_renew_token_zero_minutes(self, token_use_case, valid_token):
        """Prueba renovación con 0 minutos adicionales."""
        result = token_use_case.renew_token(valid_token, additional_minutes=0)

        assert result is not None

    def test_renew_token_negative_minutes(self, token_use_case, valid_token):
        """Prueba renovación con minutos negativos."""
        result = token_use_case.renew_token(valid_token, additional_minutes=-10)

        # Aunque los minutos sean negativos, el token se renueva
        # pero con expiración inmediata o muy corta
        assert result is not None

    def test_renew_token_large_minutes(self, token_use_case, valid_token):
        """Prueba renovación con muchos minutos adicionales."""
        result = token_use_case.renew_token(valid_token, additional_minutes=1000)

        assert result is not None
        jwt_service = JWTService()
        payload = jwt_service.decode_token(result["access_token"])
        assert payload is not None

    def test_renew_token_multiple_roles(self, token_use_case):
        """Prueba renovación de tokens con diferentes roles."""
        jwt_service = JWTService()

        for role in ["user", "admin", "uploader"]:
            token_data = {
                "id_usuario": 1,
                "rol": role,
                "sub": "test_user"
            }
            token = jwt_service.create_token(token_data)
            result = token_use_case.renew_token(token)

            assert result is not None
            new_payload = jwt_service.decode_token(result["access_token"])
            assert new_payload["rol"] == role
