# src/infrastructure/persistence/repositories/product_type.py
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime # Necesario para datetime.now()

from src.application.ports.product_type import ProductTypeRepository
from src.domain.models.product_type import ProductType as DomainProductType # Alias
from src.infrastructure.persistence.models.product_type import ProductTypeORM

class SQLAlchemyProductTypeRepository(ProductTypeRepository):
    """
    Implementación del puerto ProductTypeRepository usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_model(self, orm_model: Optional[ProductTypeORM]) -> Optional[DomainProductType]:
        """Convierte un modelo ORM a un modelo de dominio."""
        if orm_model is None:
            return None
        return DomainProductType(
            id=orm_model.id,
            name=orm_model.name,
            description=orm_model.description,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
            deleted_at=orm_model.deleted_at
        )

    def _to_orm_model(self, domain_model: DomainProductType, orm_model: Optional[ProductTypeORM] = None) -> ProductTypeORM:
        """
        Convierte un modelo de dominio a un modelo ORM.
        Si se proporciona orm_model, actualiza la instancia existente.
        """
        if orm_model is None:
            orm_model = ProductTypeORM()
        
        orm_model.name = domain_model.name
        orm_model.description = domain_model.description
        orm_model.deleted_at = domain_model.deleted_at # Para la eliminación lógica
        
        return orm_model

    def get_by_id(self, product_type_id: int) -> Optional[DomainProductType]:
        orm_product_type = self.db.query(ProductTypeORM).filter(ProductTypeORM.id == product_type_id).first()
        return self._to_domain_model(orm_product_type)

    def get_by_name(self, name: str) -> Optional[DomainProductType]:
        orm_product_type = self.db.query(ProductTypeORM).filter(ProductTypeORM.name == name).first()
        return self._to_domain_model(orm_product_type)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainProductType]:
        orm_product_types = self.db.query(ProductTypeORM).offset(skip).limit(limit).all()
        domain_product_types = [self._to_domain_model(pt) for pt in orm_product_types]
        return [pt for pt in domain_product_types if pt is not None]  # Filtrar None

    def save(self, product_type: DomainProductType) -> DomainProductType:
        if product_type.id is None:
            # Crear nuevo tipo de producto
            orm_product_type = self._to_orm_model(product_type)
            self.db.add(orm_product_type)
            self.db.commit()
            self.db.refresh(orm_product_type)
        else:
            # Actualizar tipo de producto existente
            orm_product_type = self.db.query(ProductTypeORM).filter(ProductTypeORM.id == product_type.id).first()
            if not orm_product_type:
                raise ValueError(f"ProductType with ID {product_type.id} not found for update in repository.")
            
            orm_product_type = self._to_orm_model(product_type, orm_product_type)

            self.db.commit()
            self.db.refresh(orm_product_type)

        domain_product_type = self._to_domain_model(orm_product_type)
        if domain_product_type is None:
            raise ValueError("Failed to convert ORM model to domain model after saving.")
        return domain_product_type

    def delete(self, product_type_id: int) -> Optional[DomainProductType]:
        orm_product_type = self.db.query(ProductTypeORM).filter(ProductTypeORM.id == product_type_id).first()
        if orm_product_type:
            orm_product_type.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_product_type)
            return self._to_domain_model(orm_product_type)
        return None