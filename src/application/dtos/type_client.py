# src/application/dtos/type_client.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateTypeClientDto(BaseModel):
    code: str = Field(..., max_length=10, description="Código único del tipo de cliente")
    name: str = Field(..., max_length=50, description="Nombre del tipo de cliente")
    margin: float = Field(..., ge=0, le=1, description="Margen de descuento (0.00 a 1.00, ej. 0.05 para 5%)")

class UpdateTypeClientDto(BaseModel):
    code: Optional[str] = Field(None, max_length=10, description="Código único del tipo de cliente")
    name: Optional[str] = Field(None, max_length=50, description="Nombre del tipo de cliente")
    margin: Optional[float] = Field(None, ge=0, le=1, description="Margen de descuento")

class TypeClientResponseDto(BaseModel):
    id: int
    code: str
    name: str
    margin: float
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True