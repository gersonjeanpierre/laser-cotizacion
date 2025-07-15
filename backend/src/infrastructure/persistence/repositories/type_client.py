# src/infrastructure/persistence/repositories/type_client.py
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime # Para el deleted_at si se maneja aquí

from src.application.ports.type_client import TypeClientRepository
from src.domain.models.type_client import TypeClient as DomainTypeClient # Alias para evitar conflicto
from src.infrastructure.persistence.models.type_client import TypeClientORM

class SQLAlchemyTypeClientRepository(TypeClientRepository):
    """
    Implementación del puerto TypeClientRepository usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_model(self, orm_model: Optional[TypeClientORM]) -> Optional[DomainTypeClient]:
        """Convierte un modelo ORM a un modelo de dominio."""
        if orm_model is None:
            return None
        return DomainTypeClient(
            id=orm_model.id,
            code=orm_model.code,
            name=orm_model.name,
            margin=orm_model.margin,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
            deleted_at=orm_model.deleted_at
        )

    def _to_orm_model(self, domain_model: DomainTypeClient, orm_model: Optional[TypeClientORM] = None) -> TypeClientORM:
        """
        Convierte un modelo de dominio a un modelo ORM.
        Si se proporciona orm_model, actualiza la instancia existente.
        """
        if orm_model is None:
            orm_model = TypeClientORM()
        
        orm_model.code = domain_model.code
        orm_model.name = domain_model.name
        orm_model.margin = domain_model.margin
        orm_model.deleted_at = domain_model.deleted_at
        
        return orm_model

    def get_by_id(self, type_client_id: int) -> Optional[DomainTypeClient]:
        orm_type_client = self.db.query(TypeClientORM).filter(TypeClientORM.id == type_client_id).first()
        return self._to_domain_model(orm_type_client)

    def get_by_code(self, code: str) -> Optional[DomainTypeClient]:
        orm_type_client = self.db.query(TypeClientORM).filter(TypeClientORM.code == code).first()
        return self._to_domain_model(orm_type_client)

    def get_by_name(self, name: str) -> Optional[DomainTypeClient]:
        orm_type_client = self.db.query(TypeClientORM).filter(TypeClientORM.name == name).first()
        return self._to_domain_model(orm_type_client)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainTypeClient]:
        orm_type_clients = self.db.query(TypeClientORM).offset(skip).limit(limit).all()
        domain_clients = [self._to_domain_model(tc) for tc in orm_type_clients]
        return [dc for dc in domain_clients if dc is not None]

    def save(self, type_client: DomainTypeClient) -> DomainTypeClient:
        if type_client.id is None:
            # Crear nuevo tipo de cliente
            orm_type_client = self._to_orm_model(type_client)
            self.db.add(orm_type_client)
            self.db.commit()
            self.db.refresh(orm_type_client)
        else:
            # Actualizar tipo de cliente existente
            orm_type_client = self.db.query(TypeClientORM).filter(TypeClientORM.id == type_client.id).first()
            if not orm_type_client:
                raise ValueError(f"TypeClient with ID {type_client.id} not found for update in repository.")
            
            orm_type_client = self._to_orm_model(type_client, orm_type_client)

            self.db.commit()
            self.db.refresh(orm_type_client)

        domain_model = self._to_domain_model(orm_type_client)
        if domain_model is None:
            raise ValueError("Failed to convert ORM model to domain model after save.")
        return domain_model
    
    def delete(self, type_client_id: int) -> Optional[DomainTypeClient]:
        orm_type_client = self.db.query(TypeClientORM).filter(TypeClientORM.id == type_client_id).first()
        if orm_type_client:
            orm_type_client.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_type_client)
            return self._to_domain_model(orm_type_client)
        return None