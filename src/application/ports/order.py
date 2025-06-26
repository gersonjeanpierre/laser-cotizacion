# src/application/ports/order.py
from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.models.order import Order

class OrderRepository(ABC):
    """
    Puerto (interfaz) para interactuar con los datos de los pedidos.
    """
    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Obtiene un pedido completo por su ID, incluyendo sus detalles."""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Obtiene todos los pedidos activos, paginados."""
        pass

    @abstractmethod
    def save(self, order: Order) -> Order:
        """
        Guarda o actualiza un pedido en la base de datos.
        Esto debe manejar la persistencia de los OrderDetail y OrderDetailExtraOption anidados.
        """
        pass

    @abstractmethod
    def delete(self, order_id: int) -> Optional[Order]:
        """Elimina lógicamente un pedido por su ID."""
        pass