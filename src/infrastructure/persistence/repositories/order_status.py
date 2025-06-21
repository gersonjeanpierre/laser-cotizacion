# src/infrastructure/persistence/repositories/order_status.py
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from src.application.ports.order_status import OrderStatusRepository
from src.domain.models.order_status import OrderStatus as DomainOrderStatus # Alias

from src.infrastructure.persistence.models.order_status import OrderStatusORM

class SQLAlchemyOrderStatusRepository(OrderStatusRepository):
    """
    Implementación del puerto OrderStatusRepository usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_model(self, orm_model: Optional[OrderStatusORM]) -> Optional[DomainOrderStatus]:
        """Convierte un modelo ORM a un modelo de dominio."""
        if orm_model is None:
            return None
        return DomainOrderStatus(
            id=orm_model.id,
            code=orm_model.code,
            name=orm_model.name,
            description=orm_model.description,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
            deleted_at=orm_model.deleted_at
        )

    def _to_orm_model(self, domain_model: DomainOrderStatus, orm_model: Optional[OrderStatusORM] = None) -> OrderStatusORM:
        """Convierte un modelo de dominio a un modelo ORM."""
        if orm_model is None:
            orm_model = OrderStatusORM()
        
        orm_model.code = domain_model.code
        orm_model.name = domain_model.name
        orm_model.description = domain_model.description
        orm_model.deleted_at = domain_model.deleted_at
        
        return orm_model

    def get_by_id(self, order_status_id: int) -> Optional[DomainOrderStatus]:
        orm_status = self.db.query(OrderStatusORM).filter(OrderStatusORM.id == order_status_id).first()
        return self._to_domain_model(orm_status)

    def get_by_code(self, code: str) -> Optional[DomainOrderStatus]:
        orm_status = self.db.query(OrderStatusORM).filter(OrderStatusORM.code == code).first()
        return self._to_domain_model(orm_status)

    def get_by_name(self, name: str) -> Optional[DomainOrderStatus]:
        orm_status = self.db.query(OrderStatusORM).filter(OrderStatusORM.name == name).first()
        return self._to_domain_model(orm_status)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainOrderStatus]:
        orm_statuses = self.db.query(OrderStatusORM).offset(skip).limit(limit).all()
        domain_statuses = [self._to_domain_model(status) for status in orm_statuses]
        return [ds for ds in domain_statuses if ds is not None]

    def save(self, order_status: DomainOrderStatus) -> DomainOrderStatus:
        if order_status.id is None:
            # Crear nuevo estado de pedido
            orm_status = self._to_orm_model(order_status)
            self.db.add(orm_status)
            self.db.commit()
            self.db.refresh(orm_status)
        else:
            # Actualizar estado de pedido existente
            orm_status = self.db.query(OrderStatusORM).filter(OrderStatusORM.id == order_status.id).first()
            if not orm_status:
                raise ValueError(f"OrderStatus with ID {order_status.id} not found for update in repository.")
            
            orm_status = self._to_orm_model(order_status, orm_status)
            self.db.commit()
            self.db.refresh(orm_status)

        domain_status = self._to_domain_model(orm_status)
        if domain_status is None:
            raise ValueError("Failed to convert ORM model to domain model after save.") 
        return domain_status

    def delete(self, order_status_id: int) -> Optional[DomainOrderStatus]:
        orm_status = self.db.query(OrderStatusORM).filter(OrderStatusORM.id == order_status_id).first()
        if orm_status:
            orm_status.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_status)
            return self._to_domain_model(orm_status)
        return None