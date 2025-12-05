# Instrucciones de Uso

## Configuración Inicial

### 1. Configurar Variables de Entorno

Copiar el archivo `.env.example` a `.env` y completar con tus credenciales:

```bash
cp .env.example .env
```

Editar `.env` con:
- Credenciales de SQL Server
- Clave secreta JWT (generar una segura)
- Credenciales de AWS S3
- Credenciales de Azure Cognitive Services

### 2. Instalar Dependencias

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

Asegúrate de tener SQL Server configurado y accesible. Las tablas se crearán automáticamente al iniciar la aplicación.

### 4. Crear Usuario de Prueba

```bash
python scripts/create_test_user.py
```

Esto creará un usuario con:
- Username: `demo_user`
- Password: `demo_password`
- Role: `user`

## Ejecutar la Aplicación

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en:
- API: http://localhost:8000
- Documentación: http://localhost:8000/docs
- Web: http://localhost:8000/web/documents

## Uso de las APIs

### 1. Iniciar Sesión

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo_user",
    "password": "demo_password"
  }'
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Cargar Archivo CSV

**Nota**: Este endpoint requiere un rol específico. Por defecto está configurado para "uploader". 
Puedes cambiar el rol en `app/presentation/routers/files.py` línea 38.

```bash
curl -X POST "http://localhost:8000/api/files/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@archivo.csv" \
  -F "param1=valor1" \
  -F "param2=valor2"
```

### 3. Renovar Token

```bash
curl -X POST "http://localhost:8000/api/tokens/renew" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Analizar Documento

```bash
curl -X POST "http://localhost:8000/api/documents/analyze" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@documento.pdf"
```

### 5. Consultar Eventos

```bash
curl -X GET "http://localhost:8000/api/history/events?event_type=document_upload" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 6. Exportar Eventos a Excel

```bash
curl -X GET "http://localhost:8000/api/history/events/export" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o eventos.xlsx
```

## Uso de la Interfaz Web

### Análisis de Documentos

1. Navegar a http://localhost:8000/web/documents
2. Seleccionar un archivo (PDF, JPG, PNG)
3. Hacer clic en "Analizar Documento"
4. Ver los resultados del análisis

### Historial de Eventos

1. Navegar a http://localhost:8000/web/history
2. Aplicar filtros si es necesario
3. Ver la lista de eventos
4. Exportar a Excel si se desea

## Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=app --cov-report=html

# Ejecutar pruebas específicas
pytest tests/test_auth_use_case.py
```

## Notas Importantes

1. **Roles de Usuario**: El endpoint de carga de archivos requiere un rol específico. 
   Por defecto está configurado para "uploader". Ajusta según tus necesidades.

2. **Azure Cognitive Services**: Asegúrate de tener configurados los servicios:
   - Form Recognizer (para análisis de documentos)
   - Text Analytics (para análisis de sentimientos)

3. **AWS S3**: Configura un bucket S3 y las credenciales correspondientes.

4. **SQL Server**: Asegúrate de tener el driver ODBC instalado y configurado.

5. **Tokens JWT**: Los tokens expiran en 15 minutos por defecto. 
   Usa el endpoint de renovación para extender la sesión.

## Solución de Problemas

### Error de conexión a base de datos
- Verificar que SQL Server esté ejecutándose
- Verificar la cadena de conexión en `.env`
- Verificar que el driver ODBC esté instalado

### Error al subir a S3
- Verificar credenciales de AWS
- Verificar que el bucket exista
- Verificar permisos del bucket

### Error con Azure Cognitive Services
- Verificar endpoints y claves en `.env`
- Verificar que los servicios estén habilitados en Azure

### Error de autenticación
- Verificar que el token no haya expirado
- Verificar que el token esté en el header Authorization
- Verificar formato: `Bearer YOUR_TOKEN`

