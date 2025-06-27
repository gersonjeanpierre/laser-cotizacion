# src/application/dtos/customer.py (VERSION ACTUALIZADA Y FINAL)
from pydantic import BaseModel, Field, EmailStr, BeforeValidator, model_validator
from typing import Optional, Literal, Annotated
from datetime import datetime
import re

# Importa el DTO de TypeClient para la respuesta
from src.application.dtos.type_client import TypeClientResponseDto

# Custom validators
def validate_ruc(v: Optional[str]) -> Optional[str]:
    if v is not None and not re.fullmatch(r"^\d{11}$", v):
        raise ValueError("RUC debe tener 11 dígitos numéricos.")
    return v

def validate_dni(v: Optional[str]) -> Optional[str]:
    if v is not None and not re.fullmatch(r"^\d{8}$", v):
        raise ValueError("DNI debe tener 8 dígitos numéricos.")
    return v
    
# Validador para el documento de extranjero (Carnet de Extranjería, Pasaporte, etc.)
def validate_doc_foreign(v: Optional[str]) -> Optional[str]:
    if v is not None and not (6 <= len(v) <= 20):
        raise ValueError("El documento de extranjero debe tener entre 6 y 20 caracteres.")
    return v


class CreateCustomerDto(BaseModel):
    # type_client_id es mandatorio para crear un cliente
    type_client_id: int = Field(..., description="ID del tipo de cliente asociado")
    entity_type: Literal['N', 'J'] = Field(..., description="Tipo de entidad: 'N' (Natural) o 'J' (Jurídica)")
    
    # Documentos de identidad. Son opcionales a nivel de campo,
    # pero la validación de negocio los hará obligatorios según el entity_type.
    ruc: Optional[Annotated[str, BeforeValidator(validate_ruc)]] = Field(None, max_length=11, description="Número de RUC (11 dígitos)")
    dni: Optional[Annotated[str, BeforeValidator(validate_dni)]] = Field(None, max_length=8, description="Número de DNI (8 dígitos)")
    doc_foreign: Optional[Annotated[str, BeforeValidator(validate_doc_foreign)]] = Field(None, max_length=20, description="Carnet de Extranjería, Pasaporte, etc.") # <-- Nuevo campo
    
    # Campos de nombre/razón social
    name: Optional[str] = Field(None, max_length=35, description="Nombre(s) del cliente (para Persona Natural o representante)")
    last_name: Optional[str] = Field(None, max_length=40, description="Apellido(s) del cliente (para Persona Natural o representante)")
    business_name: Optional[str] = Field(None, max_length=150, description="Razón social (para Persona Jurídica o Natural)")
    
    phone_number: str = Field(..., max_length=15, description="Número de teléfono del cliente")
    email: EmailStr = Field(..., max_length=100, description="Correo electrónico único del cliente")

    @model_validator(mode='after')
    def validate_entity_fields(self) -> 'CreateCustomerDto':
        # Validación para Persona Natural ('N')
        if self.entity_type == 'N':
            # 1. Nombre y apellido son obligatorios para una persona natural.
            if not self.name or not self.last_name:
                raise ValueError("Para Persona Natural, el nombre y el apellido son obligatorios.")
            
            # 2. Razón social es opcional, no se valida si está presente.
            #    El campo 'business_name' puede ser llenado si es una 'Persona Natural con Negocio'.
            
            # 3. Se requiere al menos un documento de identificación (DNI, RUC o doc_foreign).
            if not self.dni and not self.ruc and not self.doc_foreign:
                 raise ValueError("Para Persona Natural, se requiere DNI, RUC o un documento de extranjero.")
            
            # 4. Consistencia de documentos: Un cliente es peruano (DNI) o extranjero. No ambos.
            if self.dni is not None and self.doc_foreign is not None:
                raise ValueError("No se puede proporcionar DNI y un documento de extranjero a la vez.")
            
            # 5. El RUC es opcional y puede coexistir con DNI o doc_foreign (caso 'Persona Natural con Negocio').
            #    No se necesita validación adicional aquí, ya que el 'BeforeValidator' ya verifica el formato.
            
        # Validación para Persona Jurídica ('J')
        elif self.entity_type == 'J':
            # 1. RUC y razón social son obligatorios.
            if not self.ruc:
                raise ValueError("Para Persona Jurídica, el RUC es obligatorio.")
            if not self.business_name:
                raise ValueError("Para Persona Jurídica, la razón social es obligatoria.")
            
            # 2. Nombre, apellido, DNI y documento de extranjero son opcionales
            #    y pueden ser proporcionados para el representante legal.
            #    No se levanta error si están presentes.
            
        return self
    
# ----------------------------------------------------
# Update DTO - más flexible
# ----------------------------------------------------
class UpdateCustomerDto(BaseModel):
    type_client_id: Optional[int] = Field(None, description="ID del nuevo tipo de cliente asociado")
    
    entity_type: Optional[Literal['N', 'J']] = Field(None, description="Tipo de entidad: 'N' (Natural) o 'J' (Jurídica)")
    
    ruc: Optional[Annotated[str, BeforeValidator(validate_ruc)]] = Field(None, max_length=11, description="Número de RUC")
    dni: Optional[Annotated[str, BeforeValidator(validate_dni)]] = Field(None, max_length=8, description="Número de DNI")
    doc_foreign: Optional[Annotated[str, BeforeValidator(validate_doc_foreign)]] = Field(None, max_length=20, description="Carnet de Extranjería, Pasaporte, etc.") # <-- Nuevo campo
    
    name: Optional[str] = Field(None, max_length=35, description="Nombre(s) del cliente")
    last_name: Optional[str] = Field(None, max_length=40, description="Apellido(s) del cliente")
    business_name: Optional[str] = Field(None, max_length=150, description="Razón social")
    
    phone_number: Optional[str] = Field(None, max_length=15, description="Número de teléfono del cliente")
    email: Optional[EmailStr] = Field(None, max_length=100, description="Correo electrónico único del cliente")
    
    @model_validator(mode='after')
    def validate_entity_fields_for_update(self) -> 'UpdateCustomerDto':
        # La validación en la actualización es más laxa.
        # Solo se valida si se envían campos que son inconsistentes con el entity_type
        # o si se envían campos vacíos que no deberían.
        
        # Si se especifica un nuevo entity_type, validamos los campos relacionados.
        if self.entity_type == 'N':
            # Consistencia de documentos: DNI y documento de extranjero no pueden coexistir.
            if self.dni is not None and self.doc_foreign is not None:
                raise ValueError("No se puede proporcionar DNI y un documento de extranjero a la vez en la actualización.")
            
            # Nombre y apellido no pueden ser vacíos si se proporcionan para actualizar.
            if (self.name is not None and not self.name) or (self.last_name is not None and not self.last_name):
                 raise ValueError("Para Persona Natural, nombre y apellido no pueden ser vacíos si se proporcionan.")
            
            # `business_name` es opcional, no se valida si se proporciona.

        elif self.entity_type == 'J':
            # RUC y razón social no pueden ser vacíos si se proporcionan para actualizar.
            if self.ruc is not None and not self.ruc:
                raise ValueError("Para Persona Jurídica, el RUC no puede ser vacío si se proporciona.")
            if self.business_name is not None and not self.business_name:
                raise ValueError("Para Persona Jurídica, la razón social no puede ser vacía si se proporciona.")
            
            # Nombre, apellido, DNI y documento de extranjero son opcionales para el representante
            # y no se valida si están presentes.

        return self


# ----------------------------------------------------
# Response DTO - Debe incluir el nuevo campo
# ----------------------------------------------------
class CustomerResponseDto(BaseModel):
    id: int
    type_client: TypeClientResponseDto
    entity_type: Literal['N', 'J']
    ruc: Optional[str]
    dni: Optional[str]
    doc_foreign: Optional[str] # <-- Nuevo campo en la respuesta
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