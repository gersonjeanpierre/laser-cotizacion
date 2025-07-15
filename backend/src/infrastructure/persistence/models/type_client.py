# src/infrastructure/persistence/models/type_client.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, DateTime, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.database import Base

class TypeClientORM(Base):
    """
    Modelo ORM para la tabla 'type_clients'.
    """
    __tablename__ = "type_clients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    margin: Mapped[float] = mapped_column(Float, nullable=False) # Mapea directamente a Float
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    # Relación One-to-Many con CustomerORM
    # Usamos la cadena "CustomerORM" si CustomerORM ya importa TypeClientORM para evitar circularidad
    customers: Mapped[List["CustomerORM"]] = relationship(back_populates="type_client") # type: ignore


    def __repr__(self) -> str:
        return f"<TypeClientORM(id={self.id}, name='{self.name}', code='{self.code}')>"