# src/domain/models/order_detail.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class OrderDetail:
    # Campos obligatorios sin valor por defecto (primero)
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    # Campos opcionales o con valores por defecto (después)
    id: Optional[int] = None
    total_extra_options: float = 0.00
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def calculate_subtotal(self):
        self.subtotal = self.quantity * (self.unit_price + self.total_extra_options)

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()