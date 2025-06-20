# src/application/dtos/customer.py
from pydantic import BaseModel, Field, EmailStr, BeforeValidator, model_validator
from typing import Optional, Literal, Annotated
from datetime import datetime
import re

# Importa el DTO de TypeClient para la respuesta
from src.application.dtos.type_client import TypeClientResponseDto

# Custom validators for RUC and DNI if needed
def validate_ruc(v: Optional[str]) -> Optional[str]:
    if v is not None and not re.fullmatch(r"^\d{11}$", v):
        raise ValueError("RUC debe tener 11 dígitos numéricos.")
    return v

def validate_dni(v: Optional[str]) -> Optional[str]:
    if v is not None and not re.fullmatch(r"^\d{8}$", v):
        raise ValueError("DNI debe tener 8 dígitos numéricos.")
    return v

class CreateCustomerDto(BaseModel):
    # type_client_id es mandatorio para crear un cliente
    type_client_id: int = Field(..., description="ID del tipo de cliente asociado")
    entity_type: Literal['N', 'J'] = Field(..., description="Tipo de entidad: 'N' para Persona Natural, 'J' para Persona Jurídica")
    
    # Validadores custom si es necesario, o regex directamente en Field
    ruc: Optional[Annotated[str, BeforeValidator(validate_ruc)]] = Field(None, max_length=11, description="Número de RUC (solo para Persona Jurídica o si aplica a Natural)")
    dni: Optional[Annotated[str, BeforeValidator(validate_dni)]] = Field(None, max_length=8, description="Número de DNI (solo para Persona Natural)")
    
    name: Optional[str] = Field(None, max_length=35, description="Nombre(s) del cliente (para Persona Natural)")
    last_name: Optional[str] = Field(None, max_length=40, description="Apellido(s) del cliente (para Persona Natural)")
    business_name: Optional[str] = Field(None, max_length=150, description="Razón social (para Persona Jurídica)")
    
    phone_number: str = Field(..., max_length=15, description="Número de teléfono del cliente")
    email: EmailStr = Field(..., max_length=100, description="Correo electrónico único del cliente")

    @model_validator(mode='after')
    def validate_entity_fields(self) -> 'CreateCustomerDto':
        if self.entity_type == 'N':
            if not self.dni:
                raise ValueError("Para Persona Natural, el DNI es obligatorio.")
            if self.ruc:
                raise ValueError("Para Persona Natural, el RUC no debe ser proporcionado en la creación.")
            if not self.name or not self.last_name:
                raise ValueError("Para Persona Natural, el nombre y el apellido son obligatorios.")
            if self.business_name:
                raise ValueError("Para Persona Natural, la razón social no debe ser proporcionada.")
        elif self.entity_type == 'J':
            if not self.ruc:
                raise ValueError("Para Persona Jurídica, el RUC es obligatorio.")
            if self.dni:
                raise ValueError("Para Persona Jurídica, el DNI no debe ser proporcionado en la creación.")
            if not self.business_name:
                raise ValueError("Para Persona Jurídica, la razón social es obligatoria.")
            if self.name or self.last_name:
                raise ValueError("Para Persona Jurídica, el nombre y apellido no deben ser proporcionados.")
        return self

class UpdateCustomerDto(BaseModel):
    # type_client_id podría actualizarse, pero generalmente no es común cambiar el tipo de cliente con frecuencia
    type_client_id: Optional[int] = Field(None, description="ID del nuevo tipo de cliente asociado")
    
    entity_type: Optional[Literal['N', 'J']] = Field(None, description="Tipo de entidad: 'N' para Persona Natural, 'J' para Persona Jurídica")
    
    ruc: Optional[Annotated[str, BeforeValidator(validate_ruc)]] = Field(None, max_length=11, description="Número de RUC")
    dni: Optional[Annotated[str, BeforeValidator(validate_dni)]] = Field(None, max_length=8, description="Número de DNI")
    
    name: Optional[str] = Field(None, max_length=35, description="Nombre(s) del cliente")
    last_name: Optional[str] = Field(None, max_length=40, description="Apellido(s) del cliente")
    business_name: Optional[str] = Field(None, max_length=150, description="Razón social")
    
    phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono del cliente")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico único del cliente")

    @model_validator(mode='after')
    def validate_entity_fields_for_update(self) -> 'UpdateCustomerDto':
        # En update, la validación es más laxa porque solo se actualizan los campos proporcionados.
        # Sin embargo, si se cambia entity_type, o se proveen campos contradictorios, debemos validar.
        
        # Si se proporciona entity_type, aplicar validación estricta para los campos relevantes.
        # Si no se proporciona, no podemos asumir el tipo y la validación es más compleja.
        # Para simplificar aquí, asumimos que si se envía entity_type, es una actualización completa de ese aspecto.
        
        # Lógica más compleja para actualizaciones:
        # Esto es un ejemplo, se puede refinar dependiendo de las reglas de negocio exactas.
        if self.entity_type == 'N':
            if self.dni is not None and not self.dni: # Si se envía vacío, es error
                raise ValueError("Para Persona Natural, el DNI no puede ser vacío si se proporciona.")
            if self.ruc is not None:
                raise ValueError("Para Persona Natural, el RUC no debe ser proporcionado.")
            if (self.name is not None and not self.name) or (self.last_name is not None and not self.last_name):
                 raise ValueError("Para Persona Natural, nombre y apellido no pueden ser vacíos si se proporcionan.")
            if self.business_name is not None:
                raise ValueError("Para Persona Natural, la razón social no debe ser proporcionada.")
        elif self.entity_type == 'J':
            if self.ruc is not None and not self.ruc:
                raise ValueError("Para Persona Jurídica, el RUC no puede ser vacío si se proporciona.")
            if self.dni is not None:
                raise ValueError("Para Persona Jurídica, el DNI no debe ser proporcionado.")
            if self.business_name is not None and not self.business_name:
                raise ValueError("Para Persona Jurídica, la razón social no puede ser vacía si se proporciona.")
            if self.name is not None or self.last_name is not None:
                raise ValueError("Para Persona Jurídica, el nombre y apellido no deben ser proporcionados.")
        
        # Considerar si se envían RUC/DNI sin entity_type. El caso de uso debe validar contra el entity_type existente.
        return self


class CustomerResponseDto(BaseModel):
    id: int
    type_client: TypeClientResponseDto # Incluye el DTO completo del tipo de cliente
    entity_type: Literal['N', 'J']
    ruc: Optional[str]
    dni: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    business_name: Optional[str]
    phone_number: str
    email: EmailStr
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True