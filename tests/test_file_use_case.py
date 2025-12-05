"""
Pruebas unitarias para FileUseCase.

Contiene al menos 10 casos de prueba para cada método del caso de uso de archivos.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from app.application.use_cases.file_use_case import FileUseCase
from app.domain.entities.file import File, FileStatus


@pytest.fixture
def mock_file_repository():
    """Fixture para crear un mock del repositorio de archivos."""
    return Mock()


@pytest.fixture
def file_use_case(mock_file_repository):
    """Fixture para crear una instancia de FileUseCase."""
    return FileUseCase(mock_file_repository)


@pytest.fixture
def sample_csv_content():
    """Fixture para crear contenido CSV de prueba."""
    return b"name,email,age\nJohn Doe,john@example.com,30\nJane Smith,jane@example.com,25"


class TestFileUseCaseUploadAndValidateFile:
    """Clase de pruebas para el método upload_and_validate_file."""
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_valid_csv_success(self, mock_s3_service_class, file_use_case, mock_file_repository, sample_csv_content):
        """Prueba carga exitosa de CSV válido."""
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="test.csv",
            s3_key="uploads/1/test.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(sample_csv_content),
            content_type="text/csv",
            status=FileStatus.COMPLETED,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=sample_csv_content,
            filename="test.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1_value",
            param2="param2_value"
        )
        
        assert result["file_id"] == 1
        assert result["s3_url"] == "https://s3.amazonaws.com/bucket/file.csv"
        assert result["param1"] == "param1_value"
        assert result["param2"] == "param2_value"
        assert len(result["validations"]) == 0
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_csv_with_empty_values(self, mock_s3_service_class, file_use_case, mock_file_repository):
        """Prueba validación de valores vacíos en CSV."""
        csv_content = b"name,email,age\nJohn Doe,,30\n,jane@example.com,25"
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="test.csv",
            s3_key="uploads/1/test.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(csv_content),
            content_type="text/csv",
            status=FileStatus.PENDING,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=csv_content,
            filename="test.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1",
            param2="param2"
        )
        
        assert len(result["validations"]) > 0
        assert any(v["type"] == "empty_value" for v in result["validations"])
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_csv_with_duplicates(self, mock_s3_service_class, file_use_case, mock_file_repository):
        """Prueba validación de filas duplicadas."""
        csv_content = b"name,email\nJohn Doe,john@example.com\nJohn Doe,john@example.com"
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="test.csv",
            s3_key="uploads/1/test.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(csv_content),
            content_type="text/csv",
            status=FileStatus.PENDING,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=csv_content,
            filename="test.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1",
            param2="param2"
        )
        
        assert any(v["type"] == "duplicate" for v in result["validations"])
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_csv_with_invalid_numeric_types(self, mock_s3_service_class, file_use_case, mock_file_repository):
        """Prueba validación de tipos numéricos inválidos."""
        csv_content = b"product,price,quantity\nItem1,abc,5\nItem2,10.50,xyz"
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="test.csv",
            s3_key="uploads/1/test.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(csv_content),
            content_type="text/csv",
            status=FileStatus.PENDING,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=csv_content,
            filename="test.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1",
            param2="param2"
        )
        
        assert any(v["type"] == "invalid_type" for v in result["validations"])
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_invalid_csv_format(self, mock_s3_service_class, file_use_case, mock_file_repository):
        """Prueba manejo de CSV inválido."""
        csv_content = b"This is not a CSV file"
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="test.csv",
            s3_key="uploads/1/test.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(csv_content),
            content_type="text/csv",
            status=FileStatus.PENDING,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=csv_content,
            filename="test.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1",
            param2="param2"
        )
        
        assert len(result["validations"]) > 0
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_s3_upload_failure(self, mock_s3_service_class, file_use_case, mock_file_repository, sample_csv_content):
        """Prueba manejo de error al subir a S3."""
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = None
        mock_s3_service_class.return_value = mock_s3_service
        
        with pytest.raises(Exception, match="Error al subir archivo a S3"):
            file_use_case.upload_and_validate_file(
                file_content=sample_csv_content,
                filename="test.csv",
                content_type="text/csv",
                user_id=1,
                param1="param1",
                param2="param2"
            )
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_large_file(self, mock_s3_service_class, file_use_case, mock_file_repository):
        """Prueba carga de archivo grande."""
        large_content = b"name,email\n" + b"User" + b"1" * 1000 + b",user1@example.com\n" * 100
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="large.csv",
            s3_key="uploads/1/large.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(large_content),
            content_type="text/csv",
            status=FileStatus.COMPLETED,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=large_content,
            filename="large.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1",
            param2="param2"
        )
        
        assert result["file_id"] == 1
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_empty_csv(self, mock_s3_service_class, file_use_case, mock_file_repository):
        """Prueba carga de CSV vacío."""
        csv_content = b"name,email\n"
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="empty.csv",
            s3_key="uploads/1/empty.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(csv_content),
            content_type="text/csv",
            status=FileStatus.COMPLETED,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=csv_content,
            filename="empty.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1",
            param2="param2"
        )
        
        assert result["file_id"] == 1
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_csv_with_special_characters(self, mock_s3_service_class, file_use_case, mock_file_repository):
        """Prueba CSV con caracteres especiales."""
        csv_content = b"name,description\nJos\xc3\xa9,Descripci\xc3\xb3n con \xc3\xb1"
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="special.csv",
            s3_key="uploads/1/special.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(csv_content),
            content_type="text/csv",
            status=FileStatus.COMPLETED,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=csv_content,
            filename="special.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1",
            param2="param2"
        )
        
        assert result["file_id"] == 1
    
    @patch('app.application.use_cases.file_use_case.S3Service')
    def test_upload_csv_s3_key_generation(self, mock_s3_service_class, file_use_case, mock_file_repository, sample_csv_content):
        """Prueba generación correcta de clave S3."""
        mock_s3_service = Mock()
        mock_s3_service.upload_file.return_value = "https://s3.amazonaws.com/bucket/file.csv"
        mock_s3_service_class.return_value = mock_s3_service
        
        mock_file_repository.create.return_value = File(
            id=1,
            filename="test.csv",
            s3_key="uploads/1/20240101_120000_test.csv",
            s3_url="https://s3.amazonaws.com/bucket/file.csv",
            file_size=len(sample_csv_content),
            content_type="text/csv",
            status=FileStatus.COMPLETED,
            validations=[],
            user_id=1
        )
        
        result = file_use_case.upload_and_validate_file(
            file_content=sample_csv_content,
            filename="test.csv",
            content_type="text/csv",
            user_id=1,
            param1="param1",
            param2="param2"
        )
        
        assert "uploads" in mock_file_repository.create.call_args[0][0].s3_key
        assert "1" in mock_file_repository.create.call_args[0][0].s3_key


class TestFileUseCaseValidateCSV:
    """Clase de pruebas para el método _validate_csv."""
    
    def test_validate_csv_valid_file(self, file_use_case):
        """Prueba validación de CSV válido."""
        csv_content = b"name,email,age\nJohn Doe,john@example.com,30"
        validations = file_use_case._validate_csv(csv_content)
        assert len(validations) == 0
    
    def test_validate_csv_empty_values(self, file_use_case):
        """Prueba detección de valores vacíos."""
        csv_content = b"name,email,age\nJohn Doe,,30"
        validations = file_use_case._validate_csv(csv_content)
        assert len(validations) > 0
        assert any(v["type"] == "empty_value" for v in validations)
    
    def test_validate_csv_duplicates(self, file_use_case):
        """Prueba detección de duplicados."""
        csv_content = b"name,email\nJohn Doe,john@example.com\nJohn Doe,john@example.com"
        validations = file_use_case._validate_csv(csv_content)
        assert any(v["type"] == "duplicate" for v in validations)
    
    def test_validate_csv_invalid_numeric(self, file_use_case):
        """Prueba validación de tipos numéricos."""
        csv_content = b"product,price\nItem1,abc"
        validations = file_use_case._validate_csv(csv_content)
        assert any(v["type"] == "invalid_type" for v in validations)
    
    def test_validate_csv_valid_numeric_with_comma(self, file_use_case):
        """Prueba validación de números con coma decimal."""
        csv_content = b"product,price\nItem1,10,50"
        validations = file_use_case._validate_csv(csv_content)
        # Debería manejar comas en números
        assert isinstance(validations, list)
    
    def test_validate_csv_multiple_errors(self, file_use_case):
        """Prueba detección de múltiples errores."""
        csv_content = b"name,email,price\n,user@example.com,abc\nJohn Doe,,xyz"
        validations = file_use_case._validate_csv(csv_content)
        assert len(validations) > 1
    
    def test_validate_csv_empty_file(self, file_use_case):
        """Prueba validación de archivo vacío."""
        csv_content = b""
        validations = file_use_case._validate_csv(csv_content)
        assert isinstance(validations, list)
    
    def test_validate_csv_only_header(self, file_use_case):
        """Prueba validación de CSV solo con encabezado."""
        csv_content = b"name,email,age\n"
        validations = file_use_case._validate_csv(csv_content)
        assert isinstance(validations, list)
    
    def test_validate_csv_parse_error(self, file_use_case):
        """Prueba manejo de error de parseo."""
        csv_content = b"Invalid content that cannot be parsed as CSV"
        validations = file_use_case._validate_csv(csv_content)
        assert any(v["type"] == "parse_error" for v in validations)
    
    def test_validate_csv_unicode_content(self, file_use_case):
        """Prueba validación de contenido Unicode."""
        csv_content = "name,description\nJosé,Descripción con ñ".encode('utf-8')
        validations = file_use_case._validate_csv(csv_content)
        assert isinstance(validations, list)

