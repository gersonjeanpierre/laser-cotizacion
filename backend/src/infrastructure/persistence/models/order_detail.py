from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, func, ForeignKey, DECIMAL, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.database import Base

class OrderDetailExtraOptionORM(Base):
    """
    Modelo ORM para la tabla de unión 'order_detail_extra_options'.
    """
    __tablename__ = "order_detail_extra_options"

    order_detail_id: Mapped[int] = mapped_column(ForeignKey("order_details.id"), primary_key=True)
    extra_option_id: Mapped[int] = mapped_column(ForeignKey("extra_options.id"), primary_key=True)
    quantity: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    linear_meter: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    width: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    giga_select: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)  # Select gigantografía
    
    # Definición de relaciones con los otros modelos ORM
    order_detail: Mapped["OrderDetailORM"] = relationship(back_populates="extra_options")
    extra_option: Mapped["ExtraOptionORM"] = relationship() # type: ignore

    def __repr__(self) -> str:
        return f"<OrderDetailExtraOptionORM(order_detail_id={self.order_detail_id}, extra_option_id={self.extra_option_id})>"

class OrderDetailORM(Base):
    """
    Modelo ORM para la tabla 'order_details'.
    """
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False) # Clave foránea al pedido
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    height: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    width: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    linear_meter: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    subtotal: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    total_extra_options: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.00)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Definición de relaciones con los otros modelos ORM
    order: Mapped["OrderORM"] = relationship(back_populates="details") # type: ignore
    product: Mapped["ProductORM"] = relationship() # type: ignore
    extra_options: Mapped[List[OrderDetailExtraOptionORM]] = relationship(back_populates="order_detail", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<OrderDetailORM(id={self.id}, product_id={self.product_id}, order_id={self.order_id})>"