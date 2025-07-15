# src/infrastructure/persistence/models/product_type.py (ACTUALIZADO - CORRECCIÓN CIRCULAR IMPORT)
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.database import Base
# NO IMPORTES product_product_types_table desde product.py aquí.

class ProductTypeORM(Base):
    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relación Many-to-Many con ProductORM usando CADENA DE TEXTO
    # SQLAlchemy buscará la tabla de asociación product_product_types_table definida en el metadata de Base
    # cuando los modelos se carguen.
    products: Mapped[List["ProductORM"]] = relationship( # type: ignore
        secondary="product_product_types", # Usa el nombre de la tabla de asociación como cadena
        back_populates="product_types"
    )

    def __repr__(self) -> str:
        return f"<ProductTypeORM(id={self.id}, name='{self.name}')>"