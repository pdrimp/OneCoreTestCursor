# Documentación Técnica y de Uso

## Índice

1. [Arquitectura](#arquitectura)
2. [APIs](#apis)
3. [Módulos Web](#módulos-web)
4. [Configuración](#configuración)
5. [Pruebas](#pruebas)

## Arquitectura

### Clean Architecture

La aplicación sigue los principios de Clean Architecture, dividida en las siguientes capas:

#### 1. Domain (Dominio)
- **Entidades**: Representan los objetos de negocio puros
  - `User`: Usuario del sistema
  - `File`: Archivo cargado
  - `Document`: Documento analizado
  - `Event`: Evento registrado

- **Repositorios (Interfaces)**: Contratos que definen las operaciones de acceso a datos
  - `IUserRepository`
  - `IFileRepository`
  - `IDocumentRepository`
  - `IEventRepository`

#### 2. Application (Aplicación)
- **Casos de Uso**: Implementan la lógica de negocio
  - `AuthUseCase`: Autenticación de usuarios
  - `FileUseCase`: Gestión de archivos CSV
  - `TokenUseCase`: Renovación de tokens
  - `DocumentUseCase`: Análisis de documentos con IA
  - `EventUseCase`: Gestión de eventos

#### 3. Infrastructure (Infraestructura)
- **Modelos**: Modelos de SQLAlchemy para base de datos
- **Repositorios (Implementaciones)**: Implementaciones concretas de los repositorios
- **Servicios**: Servicios técnicos
  - `JWTService`: Manejo de tokens JWT
  - `S3Service`: Almacenamiento en AWS S3
  - `AzureService`: Integración con Azure Cognitive Services
  - `PasswordService`: Gestión de contraseñas

#### 4. Presentation (Presentación)
- **Routers**: Endpoints de la API
- **Schemas**: DTOs para validación y serialización
- **Middleware**: Autenticación y autorización

### Repository Pattern

Todos los repositorios siguen el patrón Repository, separando la lógica de acceso a datos de la lógica de negocio. Las interfaces están en el dominio y las implementaciones en la infraestructura.

## APIs

### 1. API de Inicio de Sesión

**Endpoint**: `POST /api/auth/login`

**Descripción**: Permite a usuarios anónimos iniciar sesión y obtener un token JWT.

**Parámetros**:
- `username` (string): Nombre de usuario
- `password` (string): Contraseña

**Respuesta**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token JWT contiene**:
- `id_usuario`: ID del usuario
- `rol`: Rol del usuario
- `exp`: Tiempo de expiración (15 minutos)

### 2. API de Carga y Validación de Archivos

**Endpoint**: `POST /api/files/upload`

**Descripción**: Sube un archivo CSV a S3, lo valida y almacena en SQL Server.

**Autenticación**: Requerida (rol específico)

**Parámetros**:
- `file` (file): Archivo CSV
- `param1` (string): Primer parámetro adicional
- `param2` (string): Segundo parámetro adicional

**Respuesta**:
```json
{
  "file_id": 1,
  "s3_url": "https://s3.amazonaws.com/bucket/file.csv",
  "validations": [
    {
      "type": "empty_value",
      "row": 2,
      "column": "email",
      "message": "Valor vacío en fila 2, columna email"
    }
  ],
  "param1": "valor1",
  "param2": "valor2"
}
```

**Validaciones aplicadas**:
- Valores vacíos
- Tipos de datos incorrectos
- Filas duplicadas

### 3. API de Renovación de Token

**Endpoint**: `POST /api/tokens/renew`

**Descripción**: Renueva un token JWT generando uno nuevo con tiempo adicional.

**Autenticación**: Requerida (token válido)

**Respuesta**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 4. API de Análisis de Documentos

**Endpoint**: `POST /api/documents/analyze`

**Descripción**: Analiza un documento (PDF, JPG, PNG) con Azure Cognitive Services.

**Autenticación**: Requerida

**Parámetros**:
- `file` (file): Documento a analizar

**Respuesta**:
```json
{
  "document_id": 1,
  "document_type": "invoice",
  "extracted_data": {
    "customer": {
      "name": "Cliente S.A.",
      "address": "Calle 123"
    },
    "vendor": {
      "name": "Proveedor S.A.",
      "address": "Avenida 456"
    },
    "invoice_number": "INV-001",
    "invoice_date": "2024-01-15",
    "items": [
      {
        "quantity": 2,
        "name": "Producto A",
        "unit_price": 100.00,
        "total": 200.00
      }
    ],
    "total": 200.00
  },
  "sentiment": null
}
```

### 5. API de Historial

**Endpoints**:
- `GET /api/history/events`: Obtiene eventos con filtros
- `GET /api/history/events/export`: Exporta eventos a Excel

**Filtros disponibles**:
- `event_type`: Tipo de evento
- `description`: Búsqueda en descripciones
- `start_date`: Fecha de inicio
- `end_date`: Fecha de fin

## Módulos Web

### 1. Módulo de Análisis de Documentos

**URL**: `/web/documents`

**Funcionalidades**:
- Carga de documentos (PDF, JPG, PNG)
- Clasificación automática (Factura/Información)
- Extracción de datos con IA
- Visualización de resultados

**Clasificación**:
- **Factura**: Extrae cliente, proveedor, número de factura, fecha, productos, total
- **Información**: Extrae descripción, resumen, análisis de sentimientos

### 2. Módulo Histórico

**URL**: `/web/history`

**Funcionalidades**:
- Visualización de eventos registrados
- Filtros por tipo, descripción, rango de fechas
- Exportación a Excel

**Tipos de eventos**:
- `document_upload`: Carga de documento
- `ai_processing`: Procesamiento con IA
- `user_interaction`: Interacción del usuario
- `file_upload`: Carga de archivo
- `token_renewal`: Renovación de token

## Configuración

### Variables de Entorno

Crear archivo `.env` con las siguientes variables:

```env
# Database
DATABASE_URL=mssql+pyodbc://user:password@server/database?driver=ODBC+Driver+17+for+SQL+Server

# JWT
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=15

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name

# Azure Cognitive Services
AZURE_FORM_RECOGNIZER_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_FORM_RECOGNIZER_KEY=your-azure-key
AZURE_TEXT_ANALYTICS_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_TEXT_ANALYTICS_KEY=your-azure-key

# Application
APP_NAME=Document Analysis API
DEBUG=True
```

### Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Crear usuario de prueba:
```bash
python scripts/create_test_user.py
```

4. Ejecutar aplicación:
```bash
uvicorn app.main:app --reload
```

## Pruebas

### Ejecutar Pruebas

```bash
pytest
```

### Cobertura

```bash
pytest --cov=app --cov-report=html
```

### Estructura de Pruebas

Las pruebas están organizadas por módulo:
- `tests/test_auth_use_case.py`: Pruebas de autenticación
- `tests/test_file_use_case.py`: Pruebas de archivos
- `tests/test_token_use_case.py`: Pruebas de tokens
- `tests/test_jwt_service.py`: Pruebas del servicio JWT

Cada método tiene al menos 10 casos de prueba.

## Documentación de Funciones

Todas las funciones están documentadas con:
- **¿Qué hace la función?**: Descripción del propósito
- **¿Qué parámetros recibe y de qué tipo?**: Lista de parámetros con tipos
- **¿Qué dato regresa y de qué tipo?**: Tipo de retorno y descripción

Ejemplo:
```python
def login(self, username: str, password: str) -> Optional[Dict[str, str]]:
    """
    Autentica un usuario y genera un token JWT.
    
    Args:
        username: Nombre de usuario
        password: Contraseña en texto plano
        
    Returns:
        Optional[Dict[str, str]]: Diccionario con el token JWT y tipo si la autenticación es exitosa,
                                 None si las credenciales son inválidas
    """
```

