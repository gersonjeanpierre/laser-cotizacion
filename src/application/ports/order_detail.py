# src/application/ports/order_detail.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.order_detail import OrderDetail

class OrderDetailRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_detail_id: int) -> Optional[OrderDetail]:
        pass
    
    @abstractmethod
    def get_by_order_id(self, order_id: int) -> List[OrderDetail]:
        pass

    @abstractmethod
    def save(self, order_detail: OrderDetail) -> OrderDetail:
        pass

    @abstractmethod
    def delete(self, order_detail_id: int) -> Optional[OrderDetail]:
        pass

    @abstractmethod
    def add_extra_option_to_detail(self, order_detail_id: int, extra_option_id: int, price_at_order: float):
        """Asocia una opción extra a un detalle de pedido."""
        pass
    
    @abstractmethod
    def remove_extra_option_from_detail(self, order_detail_id: int, extra_option_id: int):
        """Desasocia (lógicamente) una opción extra de un detalle de pedido."""
        pass