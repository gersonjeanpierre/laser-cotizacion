# src/infrastructure/persistence/repositories/order_detail.py
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from src.application.ports.order_detail import OrderDetailRepository
from src.domain.models.order_detail import OrderDetail as DomainOrderDetail, OrderDetailExtraOption as DomainOrderDetailExtraOption
from src.infrastructure.persistence.models.order_detail import OrderDetailORM, OrderDetailExtraOptionORM

class SQLAlchemyOrderDetailRepository(OrderDetailRepository):
    """
    Implementación del puerto OrderDetailRepository usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_extra_option_model(self, orm_model: OrderDetailExtraOptionORM) -> DomainOrderDetailExtraOption:
        """Convierte un modelo ORM de extra opción a un modelo de dominio."""
        return DomainOrderDetailExtraOption(
            extra_option_id=orm_model.extra_option_id,
            quantity=float(orm_model.quantity),
            linear_meter=float(orm_model.linear_meter) if orm_model.linear_meter is not None else None,
        )

    def _to_orm_extra_option_model(self, domain_model: DomainOrderDetailExtraOption) -> OrderDetailExtraOptionORM:
        """Convierte un modelo de dominio de extra opción a un modelo ORM."""
        return OrderDetailExtraOptionORM(
            extra_option_id=domain_model.extra_option_id,
            quantity=domain_model.quantity,
            linear_meter=domain_model.linear_meter
        )

    def _to_domain_model(self, orm_model: Optional[OrderDetailORM]) -> Optional[DomainOrderDetail]:
        """Convierte un modelo ORM de detalle de pedido a un modelo de dominio."""
        if orm_model is None:
            return None
        
        domain_extra_options = [self._to_domain_extra_option_model(eo) for eo in orm_model.extra_options]
        
        return DomainOrderDetail(
            id=orm_model.id,
            order_id=orm_model.order_id,
            product_id=orm_model.product_id,
            height=float(orm_model.height) if orm_model.height is not None else None,
            width=float(orm_model.width) if orm_model.width is not None else None,
            quantity=orm_model.quantity,
            linear_meter=float(orm_model.linear_meter) if orm_model.linear_meter is not None else None,
            subtotal=float(orm_model.subtotal),
            total_extra_options=float(orm_model.total_extra_options),
            created_at=orm_model.created_at,
            deleted_at=orm_model.deleted_at,
            extra_options=domain_extra_options
        )

    def _to_orm_model(self, domain_model: DomainOrderDetail, orm_model: Optional[OrderDetailORM] = None) -> OrderDetailORM:
        """Convierte un modelo de dominio de detalle de pedido a un modelo ORM."""
        if orm_model is None:
            orm_model = OrderDetailORM()
            
        orm_model.order_id = domain_model.order_id
        orm_model.product_id = domain_model.product_id
        orm_model.height = domain_model.height
        orm_model.width = domain_model.width
        orm_model.quantity = domain_model.quantity
        orm_model.linear_meter = domain_model.linear_meter
        orm_model.subtotal = domain_model.subtotal
        orm_model.total_extra_options = domain_model.total_extra_options
        orm_model.deleted_at = domain_model.deleted_at
        
        # Manejar las opciones extra
        orm_model.extra_options = [
            self._to_orm_extra_option_model(eo) for eo in domain_model.extra_options
        ]
        
        return orm_model

    def get_by_id(self, detail_id: int) -> Optional[DomainOrderDetail]:
        orm_detail = self.db.query(OrderDetailORM).filter(OrderDetailORM.id == detail_id).first()
        return self._to_domain_model(orm_detail)

    def get_all_by_order_id(self, order_id: int) -> List[DomainOrderDetail]:
        orm_details = self.db.query(OrderDetailORM).filter(OrderDetailORM.order_id == order_id).all()
        domain_details = [self._to_domain_model(d) for d in orm_details]
        return [d for d in domain_details if d is not None]  # Filtrar None

    def save(self, order_detail: DomainOrderDetail) -> DomainOrderDetail:
        if order_detail.id is None:
            # Crear un nuevo detalle de pedido
            orm_detail = self._to_orm_model(order_detail)
            self.db.add(orm_detail)
            self.db.commit()
            self.db.refresh(orm_detail)
        else:
            # Actualizar un detalle de pedido existente (no muy común, pero útil)
            orm_detail = self.db.query(OrderDetailORM).filter(OrderDetailORM.id == order_detail.id).first()
            if not orm_detail:
                raise ValueError(f"OrderDetail with ID {order_detail.id} not found for update in repository.")
            
            # Actualiza el modelo ORM con los datos del modelo de dominio
            orm_detail = self._to_orm_model(order_detail, orm_detail)
            self.db.commit()
            self.db.refresh(orm_detail)

        domain_detail = self._to_domain_model(orm_detail)
        if domain_detail is None:
            raise ValueError("Failed to convert ORM model to domain model after saving.")
        return domain_detail

    def delete(self, detail_id: int) -> Optional[DomainOrderDetail]:
        orm_detail = self.db.query(OrderDetailORM).filter(OrderDetailORM.id == detail_id).first()
        if orm_detail:
            orm_detail.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_detail)
            return self._to_domain_model(orm_detail)
        return None