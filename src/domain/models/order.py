# src/domain/models/order.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Order:
    # Campos obligatorios sin valor por defecto (primero)
    customer_id: int
    store_id: int
    order_status_id: int
    order_date: datetime
    total_amount: float
    profit_margin: float
    final_amount: float

    # Campos opcionales o con valores por defecto (después)
    id: Optional[int] = None
    discount_applied: float = 0.00
    payment_method: Optional[str] = None
    shipping_address: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None