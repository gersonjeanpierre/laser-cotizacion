from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CreateStoreDto(BaseModel):
    name: str = Field(..., max_length=100, description="Nombre de la tienda")
    code: Optional[str] = Field(None, max_length=10, description="Código único de la tienda")
    address: Optional[str] = Field(None, max_length=255, description="Dirección de la tienda")
    phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono de la tienda")
    phone_number_secondary: Optional[str] = Field(None, max_length=15, description="Número de teléfono secundario")
    yape_phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono para Yape")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico de la tienda")
    bcp_cta: Optional[str] = Field(None, max_length=16, description="Número de cuenta BCP")
    bcp_cci: Optional[str] = Field(None, max_length=20, description="Número CCI BCP")

class UpdateStoreDto(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Nombre de la tienda")
    code: Optional[str] = Field(None, max_length=10, description="Código único de la tienda")
    address: Optional[str] = Field(None, max_length=255, description="Dirección de la tienda")
    phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono de la tienda")
    phone_number_secondary: Optional[str] = Field(None, max_length=15, description="Número de teléfono secundario")
    yape_phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono para Yape")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico de la tienda")
    bcp_cta: Optional[str] = Field(None, max_length=16, description="Número de cuenta BCP")
    bcp_cci: Optional[str] = Field(None, max_length=20, description="Número CCI BCP")

class StoreResponseDto(BaseModel):
    id: int
    code: Optional[str]
    name: str
    address: Optional[str]
    phone_number: Optional[str]
    phone_number_secondary: Optional[str]
    yape_phone_number: Optional[str]
    email: Optional[str]
    bcp_cta: Optional[str]
    bcp_cci: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True