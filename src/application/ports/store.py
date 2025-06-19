# src/application/ports/store.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.store import Store

class StoreRepository(ABC):
    @abstractmethod
    def get_by_id(self, store_id: int) -> Optional[Store]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Store]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Store]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Store]:
        pass

    @abstractmethod
    def save(self, store: Store) -> Store:
        pass

    @abstractmethod
    def delete(self, store_id: int) -> Optional[Store]:
        pass