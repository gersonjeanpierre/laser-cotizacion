# src/application/ports/customer.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.customer import Customer

class CustomerRepository(ABC):
    @abstractmethod
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_by_ruc(self, ruc: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_by_dni(self, dni: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        pass

    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> Optional[Customer]:
        pass