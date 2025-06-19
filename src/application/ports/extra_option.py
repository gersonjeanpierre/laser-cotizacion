# src/application/ports/extra_option.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.extra_option import ExtraOption

class ExtraOptionRepository(ABC):
    @abstractmethod
    def get_by_id(self, extra_option_id: int) -> Optional[ExtraOption]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[ExtraOption]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ExtraOption]:
        pass

    @abstractmethod
    def save(self, extra_option: ExtraOption) -> ExtraOption:
        pass

    @abstractmethod
    def delete(self, extra_option_id: int) -> Optional[ExtraOption]:
        pass