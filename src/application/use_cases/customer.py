# src/application/use_cases/customer.py
from typing import List, Optional
from src.domain.models.customer import Customer
from src.application.ports.customer import CustomerRepository
from src.application.ports.type_client import TypeClientRepository # Necesario para buscar TypeClients
from src.application.dtos.customer import CreateCustomerDto, UpdateCustomerDto, CustomerResponseDto
from src.application.exceptions import NotFoundException, ConflictException
from datetime import datetime

class CustomerUseCases:
    """
    Casos de uso para la gestión de Clientes.
    """
    def __init__(
        self,
        customer_repository: CustomerRepository,
        type_client_repository: TypeClientRepository
    ):
        self.customer_repository = customer_repository
        self.type_client_repository = type_client_repository

    def create_customer(self, customer_dto: CreateCustomerDto) -> CustomerResponseDto:
        """Crea un nuevo cliente."""
        # 1. Validar unicidad (RUC, DNI, Email)
        if customer_dto.ruc and self.customer_repository.get_by_ruc(customer_dto.ruc):
            raise ConflictException(f"Ya existe un cliente con el RUC '{customer_dto.ruc}'.")
        if customer_dto.dni and self.customer_repository.get_by_dni(customer_dto.dni):
            raise ConflictException(f"Ya existe un cliente con el DNI '{customer_dto.dni}'.")
        if self.customer_repository.get_by_email(customer_dto.email):
            raise ConflictException(f"Ya existe un cliente con el email '{customer_dto.email}'.")

        # 2. Obtener y validar el TypeClient
        type_client = self.type_client_repository.get_by_id(customer_dto.type_client_id)
        if not type_client or not type_client.is_active():
            raise NotFoundException(f"Tipo de cliente con ID {customer_dto.type_client_id} no encontrado o inactivo.")

        # 3. Crear el modelo de dominio Customer
        new_customer = Customer(
            entity_type=customer_dto.entity_type,
            ruc=customer_dto.ruc,
            dni=customer_dto.dni,
            name=customer_dto.name,
            last_name=customer_dto.last_name,
            business_name=customer_dto.business_name,
            phone_number=customer_dto.phone_number,
            email=customer_dto.email,
            created_at=datetime.now(),
            type_client_id=customer_dto.type_client_id, # Asigna el ID del TypeClient
            type_client=type_client # Asigna el objeto de dominio TypeClient
        )
        
        created_customer = self.customer_repository.save(new_customer)
        
        return CustomerResponseDto.model_validate(created_customer)

    def get_customer_by_id(self, customer_id: int) -> CustomerResponseDto:
        """Recupera un cliente por su ID, incluyendo su tipo de cliente."""
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer or not customer.is_active():
            raise NotFoundException(f"Cliente con ID {customer_id} no encontrado o eliminado.")
        return CustomerResponseDto.model_validate(customer)

    def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[CustomerResponseDto]:
        """Recupera todos los clientes activos paginados, incluyendo sus tipos de cliente."""
        customers = self.customer_repository.get_all(skip, limit)
        active_customers = [c for c in customers if c.is_active()]
        return [CustomerResponseDto.model_validate(customer) for customer in active_customers]

    def update_customer(self, customer_id: int, customer_dto: UpdateCustomerDto) -> CustomerResponseDto:
        """Actualiza un cliente existente."""
        existing_customer = self.customer_repository.get_by_id(customer_id)
        if not existing_customer or not existing_customer.is_active():
            raise NotFoundException(f"Cliente con ID {customer_id} no encontrado o eliminado.")

        # Validar unicidad si se actualizan campos únicos
        if customer_dto.ruc and customer_dto.ruc != existing_customer.ruc:
            if self.customer_repository.get_by_ruc(customer_dto.ruc):
                raise ConflictException(f"Ya existe otro cliente con el RUC '{customer_dto.ruc}'.")
        if customer_dto.dni and customer_dto.dni != existing_customer.dni:
            if self.customer_repository.get_by_dni(customer_dto.dni):
                raise ConflictException(f"Ya existe otro cliente con el DNI '{customer_dto.dni}'.")
        if customer_dto.email and customer_dto.email != existing_customer.email:
            if self.customer_repository.get_by_email(customer_dto.email):
                raise ConflictException(f"Ya existe otro cliente con el email '{customer_dto.email}'.")

        # Actualizar TypeClient si se proporciona
        current_type_client_id = existing_customer.type_client.id if existing_customer.type_client else None

        if customer_dto.type_client_id is not None and customer_dto.type_client_id != current_type_client_id:
            new_type_client = self.type_client_repository.get_by_id(customer_dto.type_client_id)
            if not new_type_client or not new_type_client.is_active():
                raise NotFoundException(f"Nuevo tipo de cliente con ID {customer_dto.type_client_id} no encontrado o inactivo.")
            existing_customer.type_client = new_type_client
        
        # Validar la consistencia de los campos de entidad si entity_type se está actualizando o si los campos se proporcionan
        # y no coinciden con el entity_type actual.
        target_entity_type = customer_dto.entity_type if customer_dto.entity_type else existing_customer.entity_type
        
        if target_entity_type == 'N':
            # Si se actualiza a Natural, o si es Natural y se envían campos incorrectos
            if customer_dto.ruc is not None and customer_dto.ruc != existing_customer.ruc:
                raise ValueError("Para Persona Natural, el RUC no debe ser proporcionado.")
            if (customer_dto.name is not None and not customer_dto.name) or \
               (customer_dto.last_name is not None and not customer_dto.last_name):
                raise ValueError("Para Persona Natural, nombre y apellido no pueden ser vacíos si se proporcionan.")
            if customer_dto.business_name is not None and customer_dto.business_name != existing_customer.business_name:
                raise ValueError("Para Persona Natural, la razón social no debe ser proporcionada.")
            if customer_dto.dni is not None and not customer_dto.dni:
                raise ValueError("Para Persona Natural, el DNI no puede ser vacío si se proporciona.")

        elif target_entity_type == 'J':
            # Si se actualiza a Jurídica, o si es Jurídica y se envían campos incorrectos
            if customer_dto.dni is not None and customer_dto.dni != existing_customer.dni:
                raise ValueError("Para Persona Jurídica, el DNI no debe ser proporcionado.")
            if (customer_dto.business_name is not None and not customer_dto.business_name):
                raise ValueError("Para Persona Jurídica, la razón social no puede ser vacía si se proporciona.")
            if customer_dto.ruc is not None and not customer_dto.ruc:
                raise ValueError("Para Persona Jurídica, el RUC no puede ser vacío si se proporciona.")
            if (customer_dto.name is not None and customer_dto.name != existing_customer.name) or \
               (customer_dto.last_name is not None and customer_dto.last_name != existing_customer.last_name):
                raise ValueError("Para Persona Jurídica, el nombre y apellido no deben ser proporcionados.")

        # Actualizar los campos del modelo de dominio
        # Excluir 'type_client_id' ya que se maneja por separado
        update_data = customer_dto.model_dump(exclude_unset=True, exclude={'type_client_id'})
        existing_customer.update(**update_data)

        updated_customer = self.customer_repository.save(existing_customer)
        return CustomerResponseDto.model_validate(updated_customer)

    def delete_customer(self, customer_id: int) -> CustomerResponseDto:
        """Elimina lógicamente un cliente."""
        customer_to_delete = self.customer_repository.get_by_id(customer_id)
        if not customer_to_delete or not customer_to_delete.is_active():
            raise NotFoundException(f"Cliente con ID {customer_id} no encontrado o ya eliminado.")
        
        customer_to_delete.mark_as_deleted()
        
        deleted_customer = self.customer_repository.save(customer_to_delete)
        return CustomerResponseDto.model_validate(deleted_customer)