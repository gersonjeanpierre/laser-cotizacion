# src/infrastructure/persistence/models/customer.py
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, func, ForeignKey, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.database import Base
from src.infrastructure.persistence.models.type_client import TypeClientORM # Importa TypeClientORM

class CustomerORM(Base):
    """
    Modelo ORM para la tabla 'customers'.
    """
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_client_id: Mapped[int] = mapped_column(ForeignKey("type_clients.id"), nullable=False)
    entity_type: Mapped[str] = mapped_column(CHAR(1), nullable=False) # 'N' or 'J'
    ruc: Mapped[Optional[str]] = mapped_column(String(11), unique=True, nullable=True) # Unique if not null
    dni: Mapped[Optional[str]] = mapped_column(String(8), unique=True, nullable=True) # Unique if not null
    name: Mapped[Optional[str]] = mapped_column(String(35), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    business_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False) # Unique and not null
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relación Many-to-One con TypeClientORM
    # lazy='joined' para cargar el tipo de cliente con el cliente en la misma consulta
    type_client: Mapped["TypeClientORM"] = relationship(back_populates="customers", lazy="joined")

    def __repr__(self) -> str:
        return f"<CustomerORM(id={self.id}, name='{self.name or self.business_name}', email='{self.email}')>"