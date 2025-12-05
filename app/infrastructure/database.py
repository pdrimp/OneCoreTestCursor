"""
Módulo de configuración de base de datos.

Este módulo configura la conexión a SQL Server utilizando SQLAlchemy,
incluyendo la creación de la sesión de base de datos y la configuración
de la base declarativa.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.infrastructure.config import settings

# Crear motor de base de datos
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Crear sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para modelos
Base = declarative_base()


def get_db():
    """
    Generador de dependencia para obtener sesión de base de datos.

    Yields:
        Session: Sesión de SQLAlchemy para operaciones de base de datos

    Usage:
        Se utiliza como dependencia en FastAPI:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
