# src/application/ports/product.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.product import Product
from src.domain.models.product_type import ProductType
from src.domain.models.extra_option import ExtraOption

class ProductRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def add_product_types(self, product: Product, product_types: List[ProductType]) -> Product:
        pass

    @abstractmethod
    def set_product_types(self, product: Product, product_types: List[ProductType]) -> Product:
        pass

    @abstractmethod
    def remove_product_types(self, product: Product, product_type_ids: List[int]) -> Product:
        pass

    @abstractmethod
    def add_extra_options(self, product: Product, extra_options: List[ExtraOption]) -> Product:
        pass

    @abstractmethod
    def set_extra_options(self, product: Product, extra_options: List[ExtraOption]) -> Product:
        pass

    @abstractmethod
    def remove_extra_options(self, product: Product, extra_option_ids: List[int]) -> Product:
        pass