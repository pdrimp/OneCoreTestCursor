"""
Servicio de gestión de contraseñas.

Proporciona funcionalidades para hashear y verificar contraseñas.
"""

from passlib.context import CryptContext


class PasswordService:
    """
    Servicio para manejo de contraseñas.
    
    Proporciona métodos para hashear y verificar contraseñas
    utilizando bcrypt.
    """
    
    def __init__(self):
        """
        Inicializa el contexto de encriptación con bcrypt.
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """
        Genera un hash de una contraseña en texto plano.
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            str: Hash de la contraseña
        """
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con un hash.
        
        Args:
            plain_password: Contraseña en texto plano a verificar
            hashed_password: Hash de la contraseña almacenada
            
        Returns:
            bool: True si la contraseña coincide, False en caso contrario
        """
        return self.pwd_context.verify(plain_password, hashed_password)

