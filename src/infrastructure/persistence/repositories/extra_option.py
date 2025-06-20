# src/infrastructure/persistence/repositories/extra_option.py
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from src.application.ports.extra_option import ExtraOptionRepository
from src.domain.models.extra_option import ExtraOption as DomainExtraOption # Alias
from src.infrastructure.persistence.models.extra_option import ExtraOptionORM

class SQLAlchemyExtraOptionRepository(ExtraOptionRepository):
    """
    Implementación del puerto ExtraOptionRepository usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_model(self, orm_model: Optional[ExtraOptionORM]) -> Optional[DomainExtraOption]:
        """Convierte un modelo ORM a un modelo de dominio."""
        if orm_model is None:
            return None
        return DomainExtraOption(
            id=orm_model.id,
            name=orm_model.name,
            price=float(orm_model.price), # Aseguramos que el precio sea float
            description=orm_model.description,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
            deleted_at=orm_model.deleted_at
        )

    def _to_orm_model(self, domain_model: DomainExtraOption, orm_model: Optional[ExtraOptionORM] = None) -> ExtraOptionORM:
        """
        Convierte un modelo de dominio a un modelo ORM.
        Si se proporciona orm_model, actualiza la instancia existente.
        """
        if orm_model is None:
            orm_model = ExtraOptionORM()
        
        orm_model.name = domain_model.name
        orm_model.price = domain_model.price # SQLAlchemy maneja la conversión a Numeric
        orm_model.description = domain_model.description
        orm_model.deleted_at = domain_model.deleted_at # Para la eliminación lógica
        
        return orm_model

    def get_by_id(self, extra_option_id: int) -> Optional[DomainExtraOption]:
        orm_extra_option = self.db.query(ExtraOptionORM).filter(ExtraOptionORM.id == extra_option_id).first()
        return self._to_domain_model(orm_extra_option)

    def get_by_name(self, name: str) -> Optional[DomainExtraOption]:
        orm_extra_option = self.db.query(ExtraOptionORM).filter(ExtraOptionORM.name == name).first()
        return self._to_domain_model(orm_extra_option)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainExtraOption]:
        orm_extra_options = self.db.query(ExtraOptionORM).offset(skip).limit(limit).all()
        domain_extra_options = [self._to_domain_model(orm_option) for orm_option in orm_extra_options]
        return [option for option in domain_extra_options if option is not None]  

    def save(self, extra_option: DomainExtraOption) -> DomainExtraOption:
        if extra_option.id is None:
            # Crear nueva opción extra
            orm_extra_option = self._to_orm_model(extra_option)
            self.db.add(orm_extra_option)
            self.db.commit()
            self.db.refresh(orm_extra_option)
        else:
            # Actualizar opción extra existente
            orm_extra_option = self.db.query(ExtraOptionORM).filter(ExtraOptionORM.id == extra_option.id).first()
            if not orm_extra_option:
                raise ValueError(f"ExtraOption with ID {extra_option.id} not found for update in repository.")
            
            orm_extra_option = self._to_orm_model(extra_option, orm_extra_option)

            self.db.commit()
            self.db.refresh(orm_extra_option)
            
        domain_extra_option = self._to_domain_model(orm_extra_option)
        if domain_extra_option is None:
            raise ValueError("Failed to convert ORM model to domain model after saving.")
        return domain_extra_option

    def delete(self, extra_option_id: int) -> Optional[DomainExtraOption]:
        orm_extra_option = self.db.query(ExtraOptionORM).filter(ExtraOptionORM.id == extra_option_id).first()
        if orm_extra_option:
            orm_extra_option.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_extra_option)
            return self._to_domain_model(orm_extra_option)
        return None