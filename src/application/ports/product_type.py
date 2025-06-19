# src/application/ports/product_type.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.product_type import ProductType

class ProductTypeRepository(ABC):
    @abstractmethod
    def get_by_id(self, product_type_id: int) -> Optional[ProductType]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[ProductType]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductType]:
        pass

    @abstractmethod
    def save(self, product_type: ProductType) -> ProductType:
        pass

    @abstractmethod
    def delete(self, product_type_id: int) -> Optional[ProductType]:
        pass