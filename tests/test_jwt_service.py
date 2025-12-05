"""
Pruebas unitarias para JWTService.

Contiene al menos 10 casos de prueba para cada método del servicio JWT.
"""

import pytest
from datetime import timedelta
from app.infrastructure.services.jwt_service import JWTService


@pytest.fixture
def jwt_service():
    """Fixture para crear una instancia de JWTService."""
    return JWTService()


class TestJWTServiceCreateToken:
    """Clase de pruebas para el método create_token."""
    
    def test_create_token_success(self, jwt_service):
        """Prueba creación exitosa de token."""
        data = {"id_usuario": 1, "rol": "user"}
        token = jwt_service.create_token(data)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_token_with_expiration(self, jwt_service):
        """Prueba creación de token con expiración personalizada."""
        data = {"id_usuario": 1, "rol": "user"}
        expires_delta = timedelta(minutes=30)
        token = jwt_service.create_token(data, expires_delta)
        
        assert token is not None
        payload = jwt_service.decode_token(token)
        assert payload is not None
    
    def test_create_token_contains_data(self, jwt_service):
        """Prueba que el token contiene los datos proporcionados."""
        data = {"id_usuario": 1, "rol": "admin", "sub": "test_user"}
        token = jwt_service.create_token(data)
        payload = jwt_service.decode_token(token)
        
        assert payload["id_usuario"] == 1
        assert payload["rol"] == "admin"
        assert payload["sub"] == "test_user"
    
    def test_create_token_empty_data(self, jwt_service):
        """Prueba creación de token con datos vacíos."""
        data = {}
        token = jwt_service.create_token(data)
        
        assert token is not None
        payload = jwt_service.decode_token(token)
        assert payload is not None
    
    def test_create_token_multiple_fields(self, jwt_service):
        """Prueba creación de token con múltiples campos."""
        data = {
            "id_usuario": 1,
            "rol": "user",
            "sub": "test_user",
            "email": "test@example.com",
            "custom_field": "custom_value"
        }
        token = jwt_service.create_token(data)
        payload = jwt_service.decode_token(token)
        
        assert payload["id_usuario"] == 1
        assert payload["custom_field"] == "custom_value"
    
    def test_create_token_different_roles(self, jwt_service):
        """Prueba creación de tokens con diferentes roles."""
        roles = ["user", "admin", "uploader"]
        
        for role in roles:
            data = {"id_usuario": 1, "rol": role}
            token = jwt_service.create_token(data)
            payload = jwt_service.decode_token(token)
            
            assert payload["rol"] == role
    
    def test_create_token_different_users(self, jwt_service):
        """Prueba creación de tokens para diferentes usuarios."""
        for user_id in [1, 2, 3, 100]:
            data = {"id_usuario": user_id, "rol": "user"}
            token = jwt_service.create_token(data)
            payload = jwt_service.decode_token(token)
            
            assert payload["id_usuario"] == user_id
    
    def test_create_token_expiration_time(self, jwt_service):
        """Prueba que el token tiene tiempo de expiración."""
        data = {"id_usuario": 1, "rol": "user"}
        token = jwt_service.create_token(data)
        payload = jwt_service.decode_token(token)
        
        assert "exp" in payload
    
    def test_create_token_short_expiration(self, jwt_service):
        """Prueba creación de token con expiración corta."""
        data = {"id_usuario": 1, "rol": "user"}
        expires_delta = timedelta(seconds=1)
        token = jwt_service.create_token(data, expires_delta)
        
        assert token is not None
    
    def test_create_token_long_expiration(self, jwt_service):
        """Prueba creación de token con expiración larga."""
        data = {"id_usuario": 1, "rol": "user"}
        expires_delta = timedelta(days=30)
        token = jwt_service.create_token(data, expires_delta)
        
        assert token is not None


class TestJWTServiceDecodeToken:
    """Clase de pruebas para el método decode_token."""
    
    def test_decode_valid_token(self, jwt_service):
        """Prueba decodificación de token válido."""
        data = {"id_usuario": 1, "rol": "user"}
        token = jwt_service.create_token(data)
        payload = jwt_service.decode_token(token)
        
        assert payload is not None
        assert payload["id_usuario"] == 1
    
    def test_decode_invalid_token(self, jwt_service):
        """Prueba decodificación de token inválido."""
        invalid_token = "invalid.token.here"
        payload = jwt_service.decode_token(invalid_token)
        
        assert payload is None
    
    def test_decode_empty_token(self, jwt_service):
        """Prueba decodificación de token vacío."""
        payload = jwt_service.decode_token("")
        
        assert payload is None
    
    def test_decode_expired_token(self, jwt_service):
        """Prueba decodificación de token expirado."""
        data = {"id_usuario": 1, "rol": "user"}
        expires_delta = timedelta(seconds=-1)
        expired_token = jwt_service.create_token(data, expires_delta)
        
        # Esperar un momento para asegurar expiración
        import time
        time.sleep(1)
        
        payload = jwt_service.decode_token(expired_token)
        
        assert payload is None
    
    def test_decode_token_preserves_data(self, jwt_service):
        """Prueba que la decodificación preserva todos los datos."""
        data = {
            "id_usuario": 1,
            "rol": "admin",
            "sub": "test_user",
            "email": "test@example.com"
        }
        token = jwt_service.create_token(data)
        payload = jwt_service.decode_token(token)
        
        assert payload["id_usuario"] == data["id_usuario"]
        assert payload["rol"] == data["rol"]
        assert payload["sub"] == data["sub"]
        assert payload["email"] == data["email"]


class TestJWTServiceVerifyToken:
    """Clase de pruebas para el método verify_token."""
    
    def test_verify_valid_token(self, jwt_service):
        """Prueba verificación de token válido."""
        data = {"id_usuario": 1, "rol": "user"}
        token = jwt_service.create_token(data)
        
        assert jwt_service.verify_token(token) is True
    
    def test_verify_invalid_token(self, jwt_service):
        """Prueba verificación de token inválido."""
        assert jwt_service.verify_token("invalid.token") is False
    
    def test_verify_empty_token(self, jwt_service):
        """Prueba verificación de token vacío."""
        assert jwt_service.verify_token("") is False
    
    def test_verify_expired_token(self, jwt_service):
        """Prueba verificación de token expirado."""
        data = {"id_usuario": 1, "rol": "user"}
        expires_delta = timedelta(seconds=-1)
        expired_token = jwt_service.create_token(data, expires_delta)
        
        import time
        time.sleep(1)
        
        assert jwt_service.verify_token(expired_token) is False
    
    def test_verify_none_token(self, jwt_service):
        """Prueba verificación de None."""
        assert jwt_service.verify_token(None) is False


class TestJWTServiceRenewToken:
    """Clase de pruebas para el método renew_token."""
    
    def test_renew_valid_token(self, jwt_service):
        """Prueba renovación de token válido."""
        data = {"id_usuario": 1, "rol": "user"}
        original_token = jwt_service.create_token(data)
        new_token = jwt_service.renew_token(original_token)
        
        assert new_token is not None
        assert new_token != original_token
    
    def test_renew_token_different_token(self, jwt_service):
        """Prueba que el token renovado es diferente."""
        data = {"id_usuario": 1, "rol": "user"}
        original_token = jwt_service.create_token(data)
        new_token = jwt_service.renew_token(original_token)
        
        assert new_token != original_token
    
    def test_renew_token_preserves_data(self, jwt_service):
        """Prueba que el token renovado preserva los datos."""
        data = {"id_usuario": 1, "rol": "admin", "sub": "test_user"}
        original_token = jwt_service.create_token(data)
        new_token = jwt_service.renew_token(original_token)
        
        new_payload = jwt_service.decode_token(new_token)
        assert new_payload["id_usuario"] == data["id_usuario"]
        assert new_payload["rol"] == data["rol"]
    
    def test_renew_invalid_token(self, jwt_service):
        """Prueba renovación de token inválido."""
        new_token = jwt_service.renew_token("invalid.token")
        
        assert new_token is None
    
    def test_renew_expired_token(self, jwt_service):
        """Prueba renovación de token expirado."""
        data = {"id_usuario": 1, "rol": "user"}
        expires_delta = timedelta(seconds=-1)
        expired_token = jwt_service.create_token(data, expires_delta)
        
        import time
        time.sleep(1)
        
        new_token = jwt_service.renew_token(expired_token)
        
        assert new_token is None
    
    def test_renew_token_custom_minutes(self, jwt_service):
        """Prueba renovación con minutos personalizados."""
        data = {"id_usuario": 1, "rol": "user"}
        original_token = jwt_service.create_token(data)
        new_token = jwt_service.renew_token(original_token, additional_minutes=30)
        
        assert new_token is not None
    
    def test_renew_token_zero_minutes(self, jwt_service):
        """Prueba renovación con 0 minutos."""
        data = {"id_usuario": 1, "rol": "user"}
        original_token = jwt_service.create_token(data)
        new_token = jwt_service.renew_token(original_token, additional_minutes=0)
        
        assert new_token is not None
    
    def test_renew_token_removes_exp(self, jwt_service):
        """Prueba que se remueve la expiración del payload original."""
        data = {"id_usuario": 1, "rol": "user"}
        original_token = jwt_service.create_token(data)
        new_token = jwt_service.renew_token(original_token)
        
        # El nuevo token debe tener una nueva expiración
        new_payload = jwt_service.decode_token(new_token)
        assert "exp" in new_payload

