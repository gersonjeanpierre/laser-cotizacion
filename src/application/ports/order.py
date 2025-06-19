# src/application/ports/order.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.order import Order

class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> Optional[Order]:
        pass