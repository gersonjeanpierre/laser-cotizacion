# src/application/ports/product.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.product import Product

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Guarda un producto (crea o actualiza)."""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> Optional[Product]:
        """Elimina lógicamente un producto por su ID."""
        pass

    # Métodos para manejar relaciones many-to-many
    @abstractmethod
    def add_product_type(self, product_id: int, product_type_id: int):
        """Asocia un tipo de producto a un producto."""
        pass

    @abstractmethod
    def remove_product_type(self, product_id: int, product_type_id: int):
        """Desasocia (lógicamente) un tipo de producto de un producto."""
        pass

    @abstractmethod
    def add_extra_option(self, product_id: int, extra_option_id: int):
        """Asocia una opción extra a un producto."""
        pass

    @abstractmethod
    def remove_extra_option(self, product_id: int, extra_option_id: int):
        """Desasocia (lógicamente) una opción extra de un producto."""
        pass