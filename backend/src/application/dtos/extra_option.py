# src/application/dtos/extra_option.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateExtraOptionDto(BaseModel):
    name: str = Field(..., max_length=255, description="Nombre único de la opción extra")
    price: float = Field(..., ge=0, description="Precio adicional de la opción extra")
    description: Optional[str] = Field(None, description="Descripción de la opción extra")

class UpdateExtraOptionDto(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Nombre único de la opción extra")
    price: Optional[float] = Field(None, ge=0, description="Precio adicional de la opción extra")
    description: Optional[str] = Field(None, description="Descripción de la opción extra")

class ExtraOptionResponseDto(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True