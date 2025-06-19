# src/domain/models/product.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Product:
    # Campos obligatorios sin valor por defecto (primero)
    sku: str
    name: str
    unity_measure: str
    price: float # Usamos float para simplicidad en el dominio

    # Campos opcionales o con valores por defecto (después)
    id: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    # Relaciones para el dominio (Listas vacías por defecto)
    product_type_ids: List[int] = field(default_factory=list)
    extra_option_ids: List[int] = field(default_factory=list)

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()

    def update(self, **kwargs):
        """
        Actualiza los atributos del producto desde un diccionario.
        Ignora 'id' y campos de fecha.
        """
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                if key not in ['id', 'created_at', 'updated_at', 'deleted_at', 'product_type_ids', 'extra_option_ids']:
                    setattr(self, key, value)
        
        if self.id is not None and self.is_active():
            self.updated_at = datetime.now()