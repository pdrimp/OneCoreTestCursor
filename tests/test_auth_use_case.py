"""
Pruebas unitarias para AuthUseCase.

Contiene al menos 10 casos de prueba para cada método del caso de uso de autenticación.
"""

import pytest
from unittest.mock import Mock, MagicMock
from app.application.use_cases.auth_use_case import AuthUseCase
from app.domain.entities.user import User
from app.infrastructure.services.password_service import PasswordService


@pytest.fixture
def mock_user_repository():
    """Fixture para crear un mock del repositorio de usuarios."""
    return Mock()


@pytest.fixture
def auth_use_case(mock_user_repository):
    """Fixture para crear una instancia de AuthUseCase."""
    return AuthUseCase(mock_user_repository)


@pytest.fixture
def sample_user():
    """Fixture para crear un usuario de prueba."""
    password_service = PasswordService()
    return User(
        id=1,
        username="test_user",
        email="test@example.com",
        password_hash=password_service.hash_password("password123"),
        role="user",
        is_active=True
    )


class TestAuthUseCaseLogin:
    """Clase de pruebas para el método login de AuthUseCase."""
    
    def test_login_success(self, auth_use_case, mock_user_repository, sample_user):
        """Prueba login exitoso con credenciales válidas."""
        mock_user_repository.get_by_username.return_value = sample_user
        result = auth_use_case.login("test_user", "password123")
        
        assert result is not None
        assert "access_token" in result
        assert "token_type" in result
        assert result["token_type"] == "bearer"
        mock_user_repository.get_by_username.assert_called_once_with("test_user")
    
    def test_login_invalid_username(self, auth_use_case, mock_user_repository):
        """Prueba login con username inválido."""
        mock_user_repository.get_by_username.return_value = None
        result = auth_use_case.login("invalid_user", "password123")
        
        assert result is None
        mock_user_repository.get_by_username.assert_called_once_with("invalid_user")
    
    def test_login_invalid_password(self, auth_use_case, mock_user_repository, sample_user):
        """Prueba login con contraseña inválida."""
        mock_user_repository.get_by_username.return_value = sample_user
        result = auth_use_case.login("test_user", "wrong_password")
        
        assert result is None
    
    def test_login_inactive_user(self, auth_use_case, mock_user_repository, sample_user):
        """Prueba login con usuario inactivo."""
        sample_user.is_active = False
        mock_user_repository.get_by_username.return_value = sample_user
        result = auth_use_case.login("test_user", "password123")
        
        assert result is None
    
    def test_login_empty_username(self, auth_use_case, mock_user_repository):
        """Prueba login con username vacío."""
        mock_user_repository.get_by_username.return_value = None
        result = auth_use_case.login("", "password123")
        
        assert result is None
    
    def test_login_empty_password(self, auth_use_case, mock_user_repository, sample_user):
        """Prueba login con contraseña vacía."""
        mock_user_repository.get_by_username.return_value = sample_user
        result = auth_use_case.login("test_user", "")
        
        assert result is None
    
    def test_login_token_contains_user_id(self, auth_use_case, mock_user_repository, sample_user):
        """Prueba que el token contiene el id_usuario."""
        mock_user_repository.get_by_username.return_value = sample_user
        result = auth_use_case.login("test_user", "password123")
        
        assert result is not None
        from app.infrastructure.services.jwt_service import JWTService
        jwt_service = JWTService()
        payload = jwt_service.decode_token(result["access_token"])
        assert payload["id_usuario"] == sample_user.id
    
    def test_login_token_contains_role(self, auth_use_case, mock_user_repository, sample_user):
        """Prueba que el token contiene el rol del usuario."""
        mock_user_repository.get_by_username.return_value = sample_user
        result = auth_use_case.login("test_user", "password123")
        
        assert result is not None
        from app.infrastructure.services.jwt_service import JWTService
        jwt_service = JWTService()
        payload = jwt_service.decode_token(result["access_token"])
        assert payload["rol"] == sample_user.role
    
    def test_login_different_roles(self, auth_use_case, mock_user_repository):
        """Prueba login con diferentes roles de usuario."""
        password_service = PasswordService()
        admin_user = User(
            id=2,
            username="admin_user",
            email="admin@example.com",
            password_hash=password_service.hash_password("admin123"),
            role="admin",
            is_active=True
        )
        mock_user_repository.get_by_username.return_value = admin_user
        result = auth_use_case.login("admin_user", "admin123")
        
        assert result is not None
        from app.infrastructure.services.jwt_service import JWTService
        jwt_service = JWTService()
        payload = jwt_service.decode_token(result["access_token"])
        assert payload["rol"] == "admin"
    
    def test_login_special_characters_in_password(self, auth_use_case, mock_user_repository):
        """Prueba login con caracteres especiales en la contraseña."""
        password_service = PasswordService()
        special_user = User(
            id=3,
            username="special_user",
            email="special@example.com",
            password_hash=password_service.hash_password("P@ssw0rd!#$"),
            role="user",
            is_active=True
        )
        mock_user_repository.get_by_username.return_value = special_user
        result = auth_use_case.login("special_user", "P@ssw0rd!#$")
        
        assert result is not None

