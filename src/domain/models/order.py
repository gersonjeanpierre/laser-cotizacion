# src/domain/models/order.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from src.domain.models.customer import Customer
from src.domain.models.store import Store
from src.domain.models.order_status import OrderStatus
from src.domain.models.order_detail import OrderDetail

@dataclass
class Order:
    customer_id: int
    store_id: int
    order_status_id: int
    total_amount: float
    profit_margin: float
    final_amount: float
    id: Optional[int] = None
    discount_applied: float = 0.00
    payment_method: Optional[str] = None
    shipping_address: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    # Relaciones de dominio para enriquecer el objeto
    customer: Optional[Customer] = None
    store: Optional[Store] = None
    status: Optional[OrderStatus] = None
    details: List[OrderDetail] = field(default_factory=list)

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()