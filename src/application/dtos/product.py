# src/application/dtos/product.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Importa DTOs de entidades relacionadas para la respuesta
from src.application.dtos.product_type import ProductTypeResponseDto
from src.application.dtos.extra_option import ExtraOptionResponseDto

class CreateProductDto(BaseModel):
    sku: str = Field(..., max_length=20, description="SKU único del producto")
    name: str = Field(..., max_length=150, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=150, description="Descripción detallada del producto")
    unity_measure: str = Field(..., max_length=40, description="Unidad de medida (ej. 'unidad', 'kg')")
    price: float = Field(..., gt=0, description="Precio base del producto")
    image_url: Optional[str] = Field(None, max_length=150, description="URL de la imagen del producto")
    
    # IDs de los tipos de producto y opciones extra para la creación/asociación
    product_type_ids: List[int] = Field(default_factory=list, description="Lista de IDs de tipos de producto asociados")
    extra_option_ids: List[int] = Field(default_factory=list, description="Lista de IDs de opciones extra asociadas")

class UpdateProductDto(BaseModel):
    sku: Optional[str] = Field(None, max_length=20, description="SKU único del producto")
    name: Optional[str] = Field(None, max_length=150, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=150, description="Descripción detallada del producto")
    unity_measure: Optional[str] = Field(None, max_length=40, description="Unidad de medida")
    price: Optional[float] = Field(None, gt=0, description="Precio base del producto")
    image_url: Optional[str] = Field(None, max_length=150, description="URL de la imagen del producto")

    # Para actualizar relaciones: se sobrescribe la lista completa de IDs
    # Si quieres añadir/quitar individualmente, necesitarías endpoints separados.
    product_type_ids: Optional[List[int]] = Field(None, description="Lista de IDs de tipos de producto a asociar (sobrescribe existentes)")
    extra_option_ids: Optional[List[int]] = Field(None, description="Lista de IDs de opciones extra a asociar (sobrescribe existentes)")

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
    
    # Las relaciones se devuelven como DTOs completos para una respuesta útil
    product_types: List[ProductTypeResponseDto] = Field(default_factory=list)
    extra_options: List[ExtraOptionResponseDto] = Field(default_factory=list)

    class Config:
        from_attributes = True