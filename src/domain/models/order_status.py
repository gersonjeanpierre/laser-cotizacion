# src/domain/models/order_status.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class OrderStatus:
    code: str
    name: str
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

    def update(self, **kwargs):
        """Actualiza los atributos del estado del pedido."""
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                if key not in ['id', 'created_at', 'updated_at', 'deleted_at']:
                    setattr(self, key, value)
        
        if self.id is not None and self.is_active():
            self.updated_at = datetime.now()