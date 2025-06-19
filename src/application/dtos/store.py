# src/application/dtos/store.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CreateStoreDto(BaseModel):
    name: str = Field(..., max_length=100, description="Nombre de la tienda")
    code: Optional[str] = Field(None, max_length=10, description="Código único de la tienda")
    address: Optional[str] = Field(None, max_length=255, description="Dirección de la tienda")
    phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono de la tienda")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico de la tienda")

class UpdateStoreDto(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Nombre de la tienda")
    code: Optional[str] = Field(None, max_length=10, description="Código único de la tienda")
    address: Optional[str] = Field(None, max_length=255, description="Dirección de la tienda")
    phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono de la tienda")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico de la tienda")

class StoreResponseDto(BaseModel):
    id: int
    code: Optional[str]
    name: str
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True