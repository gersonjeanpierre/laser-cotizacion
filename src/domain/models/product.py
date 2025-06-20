# src/domain/models/product.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

# Importa los modelos de dominio relacionados
from src.domain.models.product_type import ProductType
from src.domain.models.extra_option import ExtraOption

@dataclass
class Product:
    sku: str
    name: str
    unity_measure: str
    price: float
    id: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    # Relaciones: Un producto puede tener muchos tipos y muchas opciones extra
    # Usamos field(default_factory=list) para asegurar que siempre haya una lista mutable
    product_types: List[ProductType] = field(default_factory=list)
    extra_options: List[ExtraOption] = field(default_factory=list)

    def is_active(self) -> bool:
        return self.deleted_at is None

    def mark_as_deleted(self):
        if self.is_active():
            self.deleted_at = datetime.now()

    def update(self, **kwargs):
        """
        Actualiza los atributos del producto.
        Nota: Las relaciones (product_types, extra_options) no se actualizan directamente aquí.
        Serán manejadas por métodos específicos en el caso de uso o repositorio.
        """
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                if key not in ['id', 'created_at', 'updated_at', 'deleted_at', 'product_types', 'extra_options']:
                    setattr(self, key, value)
        
        if self.id is not None and self.is_active():
            self.updated_at = datetime.now()