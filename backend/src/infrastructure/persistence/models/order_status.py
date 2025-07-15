# src/infrastructure/persistence/models/order_status.py
from datetime import datetime
from typing import Optional, List # Importa List
from sqlalchemy import String, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.database import Base

class OrderStatusORM(Base):
    """
    Modelo ORM para la tabla 'order_status'.
    """
    __tablename__ = "order_status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relación One-to-Many con OrderORM (se añadirá después)
    # orders: Mapped[List["OrderORM"]] = relationship(back_populates="order_status")

    def __repr__(self) -> str:
        return f"<OrderStatusORM(id={self.id}, name='{self.name}', code='{self.code}')>"