# src/application/ports/order_status.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.order_status import OrderStatus

class OrderStatusRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_status_id: int) -> Optional[OrderStatus]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[OrderStatus]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[OrderStatus]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[OrderStatus]:
        pass

    @abstractmethod
    def save(self, order_status: OrderStatus) -> OrderStatus:
        pass

    @abstractmethod
    def delete(self, order_status_id: int) -> Optional[OrderStatus]:
        pass