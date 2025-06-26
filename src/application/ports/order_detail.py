# src/application/ports/order_detail.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.order_detail import OrderDetail

class OrderDetailRepository(ABC):
    """
    Puerto (interfaz) para interactuar con los datos de los detalles de pedido.
    """
    @abstractmethod
    def get_by_id(self, detail_id: int) -> Optional[OrderDetail]:
        """Obtiene un detalle de pedido por su ID."""
        pass

    @abstractmethod
    def get_all_by_order_id(self, order_id: int) -> List[OrderDetail]:
        """Obtiene todos los detalles de pedido para un pedido específico."""
        pass

    @abstractmethod
    def save(self, order_detail: OrderDetail) -> OrderDetail:
        """Guarda o actualiza un detalle de pedido en la base de datos."""
        pass

    @abstractmethod
    def delete(self, detail_id: int) -> Optional[OrderDetail]:
        """Elimina lógicamente un detalle de pedido por su ID."""
        pass