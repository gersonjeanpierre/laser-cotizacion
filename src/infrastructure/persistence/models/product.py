# src/infrastructure/persistence/models/product.py (ACTUALIZADO - CORRECCIÓN CIRCULAR IMPORT)
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, Numeric, Text, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func

from src.infrastructure.database.database import Base

# NO IMPORTES ProductTypeORM NI ExtraOptionORM AQUÍ.
# Las referencias se harán con cadenas de texto.

# Tablas de asociación para las relaciones Many-to-Many
# product_product_types
product_product_types_table = Table(
    "product_product_types",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("product_type_id", ForeignKey("product_types.id"), primary_key=True),
    Column("created_at", DateTime, default=func.now())
)

# product_extra_options
product_extra_options_table = Table(
    "product_extra_options",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("extra_option_id", ForeignKey("extra_options.id"), primary_key=True),
    Column("created_at", DateTime, default=func.now())
)


class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    unity_measure: Mapped[str] = mapped_column(String(40), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Definición de relaciones Many-to-Many usando CADENAS DE TEXTO
    # Esto le dice a SQLAlchemy que resuelva la referencia más tarde
    product_types: Mapped[List["ProductTypeORM"]] = relationship( # type: ignore
        secondary=product_product_types_table,
        back_populates="products"
    )
    
    extra_options: Mapped[List["ExtraOptionORM"]] = relationship( # type: ignore
        secondary=product_extra_options_table,
        back_populates="products"
    )

    def __repr__(self) -> str:
        return f"<ProductORM(id={self.id}, name='{self.name}', sku='{self.sku}')>"