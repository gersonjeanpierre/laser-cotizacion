from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.database import Base
# from src.infrastructure.persistence.models.type_client import TypeClientORM

class CustomerORM(Base):
    """
    Modelo ORM para la tabla 'customers'.
    """
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_client_id: Mapped[int] = mapped_column(ForeignKey("type_clients.id"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(1), nullable=False) # 'N' or 'J'
    
    # Campos para documentos de identificación
    ruc: Mapped[Optional[str]] = mapped_column(String(11), unique=True, nullable=True)
    dni: Mapped[Optional[str]] = mapped_column(String(8), unique=True, nullable=True)
    doc_foreign: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True) # <-- Nueva columna para extranjeros
    
    # Campos de nombre/razón social
    name: Mapped[Optional[str]] = mapped_column(String(35), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    business_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relación One-to-One con TypeClient
    type_client: Mapped["TypeClientORM"] = relationship(lazy="joined") # type: ignore

    def __repr__(self) -> str:
        return f"<CustomerORM(id={self.id}, email={self.email})>"