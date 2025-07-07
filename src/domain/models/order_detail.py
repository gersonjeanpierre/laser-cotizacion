# src/domain/models/order_detail.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from src.domain.models.extra_option import ExtraOption
from src.domain.models.product import Product

@dataclass
class OrderDetailExtraOption:
    extra_option_id: int
    quantity: float
    linear_meter: Optional[float] = None
    width: Optional[float] = None
    giga_select: Optional[str] = None # select gigantografia
    extra_option: Optional[ExtraOption] = None # Para la relación de dominio
    created_at: Optional[datetime] = None

@dataclass
class OrderDetail:
    order_id: int
    product_id: int
    quantity: int
    subtotal: float
    id: Optional[int] = None
    height: Optional[float] = None
    width: Optional[float] = None
    linear_meter: Optional[float] = None
    total_extra_options: float = 0.00
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    # Relaciones de dominio para enriquecer el objeto
    product: Optional[Product] = None
    extra_options: List[OrderDetailExtraOption] = field(default_factory=list)

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()