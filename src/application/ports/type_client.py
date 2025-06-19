# src/application/ports/type_client.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.type_client import TypeClient

class TypeClientRepository(ABC):
    @abstractmethod
    def get_by_id(self, type_client_id: int) -> Optional[TypeClient]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[TypeClient]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[TypeClient]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[TypeClient]:
        pass

    @abstractmethod
    def save(self, type_client: TypeClient) -> TypeClient:
        pass

    @abstractmethod
    def delete(self, type_client_id: int) -> Optional[TypeClient]:
        pass