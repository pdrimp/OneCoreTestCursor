# Aplicación Web con FastAPI - Análisis de Documentos con IA

## Descripción

Aplicación web desarrollada con FastAPI que implementa Clean Architecture y Repository Pattern. Incluye APIs de autenticación, carga de archivos, y módulos de análisis de documentos utilizando Azure Cognitive Services.

## Características

- **Arquitectura**: Clean Architecture con Repository Pattern
- **APIs**: Login con JWT, carga de archivos CSV, renovación de tokens
- **Análisis de Documentos**: Clasificación automática con Azure Cognitive Services
- **Almacenamiento**: AWS S3 y SQL Server
- **Pruebas**: Suite completa de pruebas unitarias

## Estructura del Proyecto

```
.
├── app/
│   ├── domain/          # Entidades y lógica de negocio
│   ├── application/     # Casos de uso
│   ├── infrastructure/  # Implementaciones técnicas
│   ├── presentation/    # APIs y endpoints
│   └── web/            # Módulos web
├── tests/              # Pruebas unitarias
└── requirements.txt
```

## Instalación

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

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. Ejecutar la aplicación:
```bash
uvicorn app.main:app --reload
```

## Documentación

La documentación de la API está disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
