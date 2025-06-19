# src/domain/models/store.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Store:
    name: str
    id: Optional[int] = None
    code: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()

    def update(self, **kwargs):
        """
        Actualiza los atributos del producto desde un diccionario.
        Ignora 'id' y campos de fecha por defecto.
        """
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                # Evitar actualizar id o timestamps directamente desde kwargs
                if key not in ['id', 'created_at', 'updated_at', 'deleted_at']:
                    setattr(self, key, value)
        
        # Siempre actualiza updated_at si el objeto existe y no está eliminado lógicamente
        if self.id is not None and self.is_active():
            self.updated_at = datetime.now()