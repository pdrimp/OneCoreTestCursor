"""
Implementación del repositorio de documentos.

Implementa IDocumentRepository utilizando SQLAlchemy y SQL Server.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.document import Document
from app.domain.repositories.document_repository import IDocumentRepository
from app.infrastructure.models.document_model import DocumentModel


class DocumentRepository(IDocumentRepository):
    """
    Implementación concreta del repositorio de documentos.
    
    Utiliza SQLAlchemy para interactuar con la base de datos SQL Server.
    """
    
    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        
        Args:
            db: Sesión de SQLAlchemy para operaciones de base de datos
        """
        self.db = db
    
    def _to_entity(self, model: DocumentModel) -> Document:
        """
        Convierte un modelo de SQLAlchemy a una entidad del dominio.
        
        Args:
            model: Instancia de DocumentModel
            
        Returns:
            Document: Instancia de Document del dominio
        """
        from app.domain.entities.document import DocumentType
        return Document(
            id=model.id,
            filename=model.filename,
            document_type=DocumentType(model.document_type) if model.document_type else DocumentType.UNKNOWN,
            file_path=model.file_path,
            extracted_data=model.extracted_data,
            sentiment=model.sentiment,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, entity: Document) -> DocumentModel:
        """
        Convierte una entidad del dominio a un modelo de SQLAlchemy.
        
        Args:
            entity: Instancia de Document del dominio
            
        Returns:
            DocumentModel: Instancia de DocumentModel para base de datos
        """
        return DocumentModel(
            id=entity.id,
            filename=entity.filename,
            document_type=entity.document_type.value if entity.document_type else "unknown",
            file_path=entity.file_path,
            extracted_data=entity.extracted_data,
            sentiment=entity.sentiment,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def create(self, document: Document) -> Document:
        """
        Crea un nuevo documento en la base de datos.
        
        Args:
            document: Instancia de Document a crear
            
        Returns:
            Document: Documento creado con ID asignado
        """
        db_document = self._to_model(document)
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return self._to_entity(db_document)
    
    def get_by_id(self, document_id: int) -> Optional[Document]:
        """
        Obtiene un documento por su ID.
        
        Args:
            document_id: Identificador único del documento
            
        Returns:
            Optional[Document]: Documento encontrado o None si no existe
        """
        db_document = self.db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
        return self._to_entity(db_document) if db_document else None
    
    def get_by_user_id(self, user_id: int) -> List[Document]:
        """
        Obtiene todos los documentos de un usuario.
        
        Args:
            user_id: Identificador único del usuario
            
        Returns:
            List[Document]: Lista de documentos del usuario
        """
        db_documents = self.db.query(DocumentModel).filter(DocumentModel.user_id == user_id).all()
        return [self._to_entity(db_doc) for db_doc in db_documents]
    
    def get_by_type(self, document_type: str) -> List[Document]:
        """
        Obtiene todos los documentos de un tipo específico.
        
        Args:
            document_type: Tipo de documento a filtrar
            
        Returns:
            List[Document]: Lista de documentos del tipo especificado
        """
        db_documents = self.db.query(DocumentModel).filter(DocumentModel.document_type == document_type).all()
        return [self._to_entity(db_doc) for db_doc in db_documents]
    
    def update(self, document: Document) -> Document:
        """
        Actualiza un documento existente.
        
        Args:
            document: Instancia de Document con los datos actualizados
            
        Returns:
            Document: Documento actualizado
        """
        db_document = self.db.query(DocumentModel).filter(DocumentModel.id == document.id).first()
        if db_document:
            db_document.filename = document.filename
            db_document.document_type = document.document_type.value if document.document_type else "unknown"
            db_document.file_path = document.file_path
            db_document.extracted_data = document.extracted_data
            db_document.sentiment = document.sentiment
            db_document.updated_at = document.updated_at
            self.db.commit()
            self.db.refresh(db_document)
            return self._to_entity(db_document)
        return document
    
    def delete(self, document_id: int) -> bool:
        """
        Elimina un documento de la base de datos.
        
        Args:
            document_id: Identificador único del documento a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        db_document = self.db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
        if db_document:
            self.db.delete(db_document)
            self.db.commit()
            return True
        return False

