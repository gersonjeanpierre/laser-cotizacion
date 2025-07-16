# src/infrastructure/persistence/models/store.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

# Importa la Base Declarativa desde tu configuración de base de datos
from src.infrastructure.database.database import Base

class StoreORM(Base):
    """
    Modelo ORM para la tabla 'stores'.
    Representa el mapeo de la entidad Store a la base de datos.
    """
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[Optional[str]] = mapped_column(String(10), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    phone_number_secondary: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    yape_phone_number: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    bcp_cta: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    bcp_cci: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Timestamps con valores por defecto a nivel de la base de datos
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<StoreORM(id={self.id}, name='{self.name}', code='{self.code}')>"