# src/application/dtos/extra_option.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateExtraOptionDto(BaseModel):
    name: str = Field(..., max_length=255, description="Nombre único de la opción extra")
    price_modifier: float = Field(..., description="Modificador de precio (ej. 10.50 para un costo adicional de 10.50)")
    description: Optional[str] = Field(None, description="Descripción de la opción extra")

class UpdateExtraOptionDto(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Nombre único de la opción extra")
    price_modifier: Optional[float] = Field(None, description="Modificador de precio")
    description: Optional[str] = Field(None, description="Descripción de la opción extra")

class ExtraOptionResponseDto(BaseModel):
    id: int
    name: str
    price_modifier: float
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True