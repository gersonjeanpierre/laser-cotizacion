# src/application/dtos/product.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# DTO para crear un nuevo producto
class CreateProductDto(BaseModel):
    sku: str = Field(..., max_length=20, description="SKU único del producto")
    name: str = Field(..., max_length=150, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=150, description="Descripción detallada del producto")
    unity_measure: str = Field(..., max_length=40, description="Unidad de medida (ej. kg, unidad)")
    price: float = Field(..., gt=0, description="Precio base del producto") # gt=0 asegura que sea mayor que cero
    image_url: Optional[str] = Field(None, max_length=150, description="URL de la imagen del producto")
    
    # Para manejar la asignación inicial de tipos y opciones extras
    product_type_ids: Optional[List[int]] = Field(None, description="Lista de IDs de los tipos de producto asociados")
    extra_option_ids: Optional[List[int]] = Field(None, description="Lista de IDs de las opciones extras asociadas")

# DTO para actualizar un producto existente (todos los campos son opcionales)
class UpdateProductDto(BaseModel):
    sku: Optional[str] = Field(None, max_length=20, description="SKU único del producto")
    name: Optional[str] = Field(None, max_length=150, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=150, description="Descripción detallada del producto")
    unity_measure: Optional[str] = Field(None, max_length=40, description="Unidad de medida (ej. kg, unidad)")
    price: Optional[float] = Field(None, gt=0, description="Precio base del producto")
    image_url: Optional[str] = Field(None, max_length=150, description="URL de la imagen del producto")
    
    # Para manejar la actualización de tipos y opciones extras.
    # Podrías querer un endpoint separado para esto o un manejo más granular.
    # Por ahora, simplemente las IDs que se quieren asociar/desasociar.
    product_type_ids: Optional[List[int]] = Field(None, description="Lista de IDs de los tipos de producto a asociar/reemplazar")
    extra_option_ids: Optional[List[int]] = Field(None, description="Lista de IDs de las opciones extras a asociar/reemplazar")

# DTO para la respuesta de un producto (incluye ID y timestamps)
class ProductResponseDto(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    unity_measure: str
    price: float
    image_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    # Opcionalmente, puedes incluir DTOs anidados si necesitas los detalles completos
    # de tipos de producto y opciones extras en la respuesta. Por ahora, solo los IDs.
    product_type_ids: List[int] = Field(default_factory=list)
    extra_option_ids: List[int] = Field(default_factory=list)

    class Config:
        from_attributes = True # Equivalente a orm_mode = True en Pydantic v1.x