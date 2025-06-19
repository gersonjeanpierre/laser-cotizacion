# src/domain/models/customer.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    # Campos obligatorios sin valor por defecto (primero)
    type_client_id: int
    entity_type: str # 'N' para Persona Natural, 'J' para Persona Jurídica

    # Campos opcionales o con valores por defecto (después)
    id: Optional[int] = None
    ruc: Optional[str] = None
    dni: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    business_name: Optional[str] = None # Razón social para Persona Jurídica
    phone_number: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()