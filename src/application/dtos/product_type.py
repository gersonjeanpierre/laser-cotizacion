# src/application/dtos/product_type.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# DTO para crear un nuevo tipo de producto
class CreateProductTypeDto(BaseModel):
    name: str = Field(..., max_length=255, description="Nombre único del tipo de producto")
    description: Optional[str] = Field(None, description="Descripción del tipo de producto")

# DTO para actualizar un tipo de producto existente
class UpdateProductTypeDto(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Nombre único del tipo de producto")
    description: Optional[str] = Field(None, description="Descripción del tipo de producto")

# DTO para la respuesta de un tipo de producto
class ProductTypeResponseDto(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] # Añadido updated_at para consistencia con DBML y model
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True # Permite crear el DTO directamente desde un objeto ORM o similar