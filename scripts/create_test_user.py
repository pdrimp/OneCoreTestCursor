"""
Script para crear un usuario de prueba en la base de datos.

Este script crea un usuario de prueba que puede ser utilizado
para testing y desarrollo.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.domain.entities.user import User
from app.infrastructure.services.password_service import PasswordService
from app.infrastructure.repositories.user_repository_impl import UserRepository


def create_test_user():
    """
    Crea un usuario de prueba en la base de datos.
    
    Usuario creado:
    - Username: demo_user
    - Password: demo_password
    - Email: demo@example.com
    - Role: user
    """
    db: Session = SessionLocal()
    try:
        user_repository = UserRepository(db)
        password_service = PasswordService()
        
        # Verificar si el usuario ya existe
        existing_user = user_repository.get_by_username("demo_user")
        if existing_user:
            print("El usuario 'demo_user' ya existe en la base de datos.")
            return
        
        # Crear nuevo usuario
        new_user = User(
            username="demo_user",
            email="demo@example.com",
            password_hash=password_service.hash_password("demo_password"),
            role="user",
            is_active=True
        )
        
        created_user = user_repository.create(new_user)
        print(f"Usuario de prueba creado exitosamente:")
        print(f"  - ID: {created_user.id}")
        print(f"  - Username: {created_user.username}")
        print(f"  - Email: {created_user.email}")
        print(f"  - Role: {created_user.role}")
        
    except Exception as e:
        print(f"Error al crear usuario de prueba: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_user()

