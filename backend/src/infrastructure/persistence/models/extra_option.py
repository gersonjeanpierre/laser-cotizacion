# src/infrastructure/persistence/models/extra_option.py (ACTUALIZADO - CORRECCIÓN CIRCULAR IMPORT)
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.database import Base
# NO IMPORTES product_extra_options_table desde product.py aquí.

class ExtraOptionORM(Base):
    __tablename__ = "extra_options"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relación Many-to-Many con ProductORM usando CADENA DE TEXTO
    products: Mapped[List["ProductORM"]] = relationship( # type: ignore
        secondary="product_extra_options", # Usa el nombre de la tabla de asociación como cadena
        back_populates="extra_options"
    )

    def __repr__(self) -> str:
        return f"<ExtraOptionORM(id={self.id}, name='{self.name}', price={self.price})>"