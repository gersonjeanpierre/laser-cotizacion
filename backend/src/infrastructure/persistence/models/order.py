# src/infrastructure/persistence/models/order.py
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, func, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.database import Base

# Importa los modelos ORM con los que se relaciona

class OrderORM(Base):
    """
    Modelo ORM para la tabla 'orders'.
    """
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    order_status_id: Mapped[int] = mapped_column(ForeignKey("order_status.id"), nullable=False)
    total_amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    profit_margin: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    discount_applied: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.00)
    final_amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    shipping_address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relaciones One-to-Many
    customer: Mapped['CustomerORM'] = relationship() # type: ignore
    store: Mapped['StoreORM'] = relationship() # type: ignore
    order_status: Mapped['OrderStatusORM'] = relationship() # type: ignore
    
    # Relación One-to-Many con los detalles del pedido
    details: Mapped[List['OrderDetailORM']] = relationship( # type: ignore
        back_populates="order",
        cascade="all, delete-orphan", # Para que los detalles se eliminen con el pedido
        lazy="joined" # Carga los detalles automáticamente al consultar un pedido
    )

    def __repr__(self) -> str:
        return f"<OrderORM(id={self.id}, final_amount={self.final_amount})>"