# src/infrastructure/persistence/repositories/order.py
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from src.application.ports.order import OrderRepository
from src.domain.models.order import Order as DomainOrder
from src.domain.models.order_detail import OrderDetail as DomainOrderDetail, OrderDetailExtraOption as DomainOrderDetailExtraOption
from src.infrastructure.persistence.models.order import OrderORM
from src.infrastructure.persistence.models.order_detail import OrderDetailORM, OrderDetailExtraOptionORM

class SQLAlchemyOrderRepository(OrderRepository):
    """
    Implementación del puerto OrderRepository usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_model(self, orm_model: Optional[OrderORM]) -> Optional[DomainOrder]:
        """Convierte un modelo ORM de pedido a un modelo de dominio."""
        if orm_model is None:
            return None
        
        domain_details = []
        if orm_model.details:
            for detail_orm in orm_model.details:
                domain_extra_options = [
                    DomainOrderDetailExtraOption(
                        extra_option_id=eo.extra_option_id,
                        quantity=float(eo.quantity),
                        linear_meter=float(eo.linear_meter) if eo.linear_meter is not None else None,
                    ) for eo in detail_orm.extra_options
                ]
                
                domain_details.append(
                    DomainOrderDetail(
                        id=detail_orm.id,
                        order_id=detail_orm.order_id,
                        product_id=detail_orm.product_id,
                        height=float(detail_orm.height) if detail_orm.height is not None else None,
                        width=float(detail_orm.width) if detail_orm.width is not None else None,
                        quantity=detail_orm.quantity,
                        linear_meter=float(detail_orm.linear_meter) if detail_orm.linear_meter is not None else None,
                        subtotal=float(detail_orm.subtotal),
                        total_extra_options=float(detail_orm.total_extra_options),
                        created_at=detail_orm.created_at,
                        deleted_at=detail_orm.deleted_at,
                        extra_options=domain_extra_options
                    )
                )
         # Lógica para mapear el Customer, Store y OrderStatus (NUEVO)
        # Verificamos si las relaciones fueron cargadas por el joinedload
        domain_customer = orm_model.customer if orm_model.customer is not None else None
        domain_store = orm_model.store if orm_model.store is not None else None
        domain_status = orm_model.order_status if orm_model.order_status is not None else None


        return DomainOrder(
            id=orm_model.id,
            customer_id=orm_model.customer_id,
            store_id=orm_model.store_id,
            order_status_id=orm_model.order_status_id,
            total_amount=float(orm_model.total_amount),
            profit_margin=float(orm_model.profit_margin),
            discount_applied=float(orm_model.discount_applied),
            final_amount=float(orm_model.final_amount),
            payment_method=orm_model.payment_method,
            shipping_address=orm_model.shipping_address,
            notes=orm_model.notes,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
            deleted_at=orm_model.deleted_at,
            details=domain_details,
            # Asignamos los objetos de dominio mapeados (NUEVO)
            customer=domain_customer,
            store=domain_store,
            status=domain_status
        )

    def _to_orm_model(self, domain_model: DomainOrder, orm_model: Optional[OrderORM] = None) -> OrderORM:
        """Convierte un modelo de dominio de pedido a un modelo ORM."""
        if orm_model is None:
            orm_model = OrderORM()
        
        orm_model.customer_id = domain_model.customer_id
        orm_model.store_id = domain_model.store_id
        orm_model.order_status_id = domain_model.order_status_id
        orm_model.total_amount = domain_model.total_amount
        orm_model.profit_margin = domain_model.profit_margin
        orm_model.discount_applied = domain_model.discount_applied
        orm_model.final_amount = domain_model.final_amount
        orm_model.payment_method = domain_model.payment_method
        orm_model.shipping_address = domain_model.shipping_address
        orm_model.notes = domain_model.notes
        orm_model.deleted_at = domain_model.deleted_at
        
        # Manejar los detalles del pedido
        orm_model.details = [] # Limpiamos la lista para reconstruirla
        for detail_domain in domain_model.details:
            detail_orm = OrderDetailORM(
                product_id=detail_domain.product_id,
                height=detail_domain.height,
                width=detail_domain.width,
                quantity=detail_domain.quantity,
                linear_meter=detail_domain.linear_meter,
                subtotal=detail_domain.subtotal,
                total_extra_options=detail_domain.total_extra_options
            )
            # Manejar las opciones extra del detalle
            detail_orm.extra_options = [
                OrderDetailExtraOptionORM(
                    extra_option_id=eo_domain.extra_option_id,
                    quantity=eo_domain.quantity,
                    linear_meter=eo_domain.linear_meter
                ) for eo_domain in detail_domain.extra_options
            ]
            orm_model.details.append(detail_orm)
        
        return orm_model

    def get_by_id(self, order_id: int) -> Optional[DomainOrder]:
        orm_order = self.db.query(OrderORM).options(
            joinedload(OrderORM.details).joinedload(OrderDetailORM.extra_options),
            joinedload(OrderORM.customer),  # Cargar Customer
            joinedload(OrderORM.store),     # Cargar Store
            joinedload(OrderORM.order_status)  # Cargar OrderStatus
        ).filter(OrderORM.id == order_id).first()
        return self._to_domain_model(orm_order)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainOrder]:
        orm_orders = self.db.query(OrderORM).options(
            joinedload(OrderORM.details).joinedload(OrderDetailORM.extra_options),
            joinedload(OrderORM.customer),  # Cargar Customer
            joinedload(OrderORM.store),     # Cargar Store
            joinedload(OrderORM.order_status)  # Cargar OrderStatus
        ).offset(skip).limit(limit).all()
        domain_orders = [self._to_domain_model(order) for order in orm_orders ]
        return [d for d in domain_orders if d is not None]  # Filtrar None

    def save(self, order: DomainOrder) -> DomainOrder:
        if order.id is None:
            # Crear un nuevo pedido
            orm_order = self._to_orm_model(order)
            self.db.add(orm_order)
            self.db.flush() # Para obtener el ID del pedido antes de commitear
            
            # Asignar el order_id a cada detalle
            for detail_orm in orm_order.details:
                detail_orm.order_id = orm_order.id
                
            self.db.commit()
            self.db.refresh(orm_order)
        else:
            # Actualizar un pedido existente
            orm_order = self.db.query(OrderORM).filter(OrderORM.id == order.id).first()
            if not orm_order:
                raise ValueError(f"Order with ID {order.id} not found for update in repository.")
            
            # Borrar los detalles existentes para reconstruirlos con la nueva lista
            orm_order.details.clear() 
            self.db.flush() # Aplica el borrado
            
            orm_order = self._to_orm_model(order, orm_order)
            self.db.commit()
            self.db.refresh(orm_order)

        domain_order = self._to_domain_model(orm_order)
        if domain_order is None:
            raise ValueError("Failed to convert ORM model to domain model after saving.")
        return domain_order

    def delete(self, order_id: int) -> Optional[DomainOrder]:
        orm_order = self.db.query(OrderORM).filter(OrderORM.id == order_id).first()
        if orm_order:
            orm_order.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_order)
            return self._to_domain_model(orm_order)
        return None