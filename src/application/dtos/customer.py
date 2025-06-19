# src/application/dtos/customer.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class CreateCustomerDto(BaseModel):
    type_client_id: int = Field(..., description="ID del tipo de cliente asociado")
    entity_type: str = Field(..., pattern="^[NJ]$", max_length=1, description="Tipo de entidad: 'N' (Natural) o 'J' (Jurídica)")
    ruc: Optional[str] = Field(None, max_length=11, description="RUC (para Persona Jurídica o Natural con RUC)")
    dni: Optional[str] = Field(None, max_length=8, description="DNI (para Persona Natural)")
    name: Optional[str] = Field(None, max_length=35, description="Nombre del cliente")
    last_name: Optional[str] = Field(None, max_length=40, description="Apellido del cliente")
    business_name: Optional[str] = Field(None, max_length=150, description="Razón social (para Persona Jurídica)")
    phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico único del cliente")

class UpdateCustomerDto(BaseModel):
    type_client_id: Optional[int] = Field(None, description="ID del tipo de cliente asociado")
    entity_type: Optional[str] = Field(None, pattern="^[NJ]$", max_length=1, description="Tipo de entidad: 'N' (Natural) o 'J' (Jurídica)")
    ruc: Optional[str] = Field(None, max_length=11, description="RUC")
    dni: Optional[str] = Field(None, max_length=8, description="DNI")
    name: Optional[str] = Field(None, max_length=35, description="Nombre del cliente")
    last_name: Optional[str] = Field(None, max_length=40, description="Apellido del cliente")
    business_name: Optional[str] = Field(None, max_length=150, description="Razón social")
    phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico único del cliente")

class CustomerResponseDto(BaseModel):
    id: int
    type_client_id: int
    entity_type: str
    ruc: Optional[str]
    dni: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    business_name: Optional[str]
    phone_number: Optional[str]
    email: Optional[str] # EmailStr se convierte a str al serializar
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True