# Estructura del Proyecto

## Organización de Directorios

```
TestCursor/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Aplicación principal FastAPI
│   │
│   ├── domain/                    # Capa de Dominio (Clean Architecture)
│   │   ├── __init__.py
│   │   ├── entities/              # Entidades de negocio
│   │   │   ├── user.py
│   │   │   ├── file.py
│   │   │   ├── document.py
│   │   │   └── event.py
│   │   └── repositories/          # Interfaces de repositorios
│   │       ├── user_repository.py
│   │       ├── file_repository.py
│   │       ├── document_repository.py
│   │       └── event_repository.py
│   │
│   ├── application/                # Capa de Aplicación (Casos de Uso)
│   │   ├── __init__.py
│   │   └── use_cases/
│   │       ├── auth_use_case.py
│   │       ├── file_use_case.py
│   │       ├── token_use_case.py
│   │       ├── document_use_case.py
│   │       └── event_use_case.py
│   │
│   ├── infrastructure/              # Capa de Infraestructura
│   │   ├── __init__.py
│   │   ├── config.py             # Configuración (variables de entorno)
│   │   ├── database.py           # Configuración de base de datos
│   │   ├── models/                # Modelos SQLAlchemy
│   │   │   ├── user_model.py
│   │   │   ├── file_model.py
│   │   │   ├── document_model.py
│   │   │   └── event_model.py
│   │   ├── repositories/         # Implementaciones de repositorios
│   │   │   ├── user_repository_impl.py
│   │   │   ├── file_repository_impl.py
│   │   │   ├── document_repository_impl.py
│   │   │   └── event_repository_impl.py
│   │   └── services/              # Servicios técnicos
│   │       ├── jwt_service.py
│   │       ├── s3_service.py
│   │       ├── azure_service.py
│   │       └── password_service.py
│   │
│   ├── presentation/              # Capa de Presentación
│   │   ├── __init__.py
│   │   ├── routers/              # Endpoints de la API
│   │   │   ├── auth.py
│   │   │   ├── files.py
│   │   │   ├── tokens.py
│   │   │   ├── documents.py
│   │   │   ├── history.py
│   │   │   └── web.py
│   │   ├── schemas/              # DTOs (Pydantic)
│   │   │   ├── auth_schemas.py
│   │   │   ├── file_schemas.py
│   │   │   ├── document_schemas.py
│   │   │   └── event_schemas.py
│   │   └── middleware/           # Middleware de autenticación
│   │       └── auth_middleware.py
│   │
│   └── web/                      # Módulos Web
│       ├── __init__.py
│       └── templates/            # Plantillas HTML
│           ├── base.html
│           ├── documents.html
│           └── history.html
│
├── tests/                        # Pruebas Unitarias
│   ├── __init__.py
│   ├── test_auth_use_case.py
│   ├── test_file_use_case.py
│   ├── test_token_use_case.py
│   └── test_jwt_service.py
│
├── scripts/                      # Scripts de utilidad
│   ├── __init__.py
│   └── create_test_user.py
│
├── requirements.txt              # Dependencias Python
├── pytest.ini                   # Configuración de Pytest
├── .gitignore                   # Archivos ignorados por Git
├── .env.example                 # Ejemplo de variables de entorno
├── README.md                     # Documentación principal
├── DOCUMENTACION.md              # Documentación técnica detallada
└── ESTRUCTURA_PROYECTO.md        # Este archivo

```

## Principios Aplicados

### Clean Architecture
- **Domain**: Lógica de negocio pura, sin dependencias externas
- **Application**: Casos de uso que orquestan la lógica de negocio
- **Infrastructure**: Implementaciones técnicas (BD, servicios externos)
- **Presentation**: Interfaces (API, Web)

### Repository Pattern
- Interfaces definidas en el dominio
- Implementaciones en la infraestructura
- Permite cambiar la implementación sin afectar la lógica de negocio

### Separación de Responsabilidades
- Cada módulo tiene una responsabilidad única
- Dependencias apuntan hacia adentro (hacia el dominio)
- El dominio no depende de nada externo

## Flujo de Datos

1. **Request** → Router (Presentation)
2. **Router** → Use Case (Application)
3. **Use Case** → Repository Interface (Domain)
4. **Repository Interface** → Repository Implementation (Infrastructure)
5. **Repository Implementation** → Database/External Services

## Endpoints Disponibles

### APIs
- `POST /api/auth/login` - Inicio de sesión
- `POST /api/files/upload` - Carga de archivos CSV
- `POST /api/tokens/renew` - Renovación de token
- `POST /api/documents/analyze` - Análisis de documentos
- `GET /api/history/events` - Consulta de eventos
- `GET /api/history/events/export` - Exportación a Excel

### Web
- `GET /web/documents` - Página de análisis de documentos
- `GET /web/history` - Página de historial

### Documentación
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

