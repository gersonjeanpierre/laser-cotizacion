# src/domain/models/customer.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Literal

# Importa el modelo de dominio TypeClient
from src.domain.models.type_client import TypeClient

@dataclass
class Customer:
    entity_type: Literal['N', 'J'] # 'N' para Persona Natural, 'J' para Persona Jurídica
    phone_number: str
    email: str
    type_client_id: int # ID del tipo de cliente
    
    id: Optional[int] = None
    doc_foreign: Optional[str] = None # Número de documento, para CE 
    ruc: Optional[str] = None # RUC es opcional, pero único si está presente
    dni: Optional[str] = None # DNI es opcional, pero único si está presente
    name: Optional[str] = None
    last_name: Optional[str] = None
    business_name: Optional[str] = None # Razón social para Persona Jurídica
    shipping_address: Optional[str] = None # Nueva adición para dirección de envío
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    # Relación: Un cliente tiene un tipo de cliente
    type_client: Optional[TypeClient] = field(default=None, repr=False) # repr=False para evitar recursión en __repr__

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()

    def update(self, **kwargs):
        """
        Actualiza los atributos del cliente.
        Nota: `id`, `created_at`, `deleted_at`, `type_client` y `type_client_id` no se actualizan directamente aquí.
        La actualización de `type_client_id` será manejada en el caso de uso si es necesario.
        """
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                if key not in ['id', 'created_at', 'updated_at', 'deleted_at', 'type_client', 'type_client_id']:
                    setattr(self, key, value)
        
        if self.id is not None and self.is_active():
            self.updated_at = datetime.now()