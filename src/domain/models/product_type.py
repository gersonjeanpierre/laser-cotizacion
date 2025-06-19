# src/domain/models/product_type.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ProductType:
    # Campos obligatorios sin valor por defecto (primero)
    name: str

    # Campos opcionales o con valores por defecto (después)
    id: Optional[int] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()