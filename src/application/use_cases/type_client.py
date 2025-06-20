# src/application/use_cases/type_client.py
from typing import List, Optional
from src.domain.models.type_client import TypeClient
from src.application.ports.type_client import TypeClientRepository
from src.application.dtos.type_client import CreateTypeClientDto, UpdateTypeClientDto, TypeClientResponseDto
from src.application.exceptions import NotFoundException, ConflictException
from datetime import datetime

class TypeClientUseCases:
    """
    Casos de uso para la gestión de Tipos de Cliente.
    """
    def __init__(self, repository: TypeClientRepository):
        self.repository = repository

    def create_type_client(self, type_client_dto: CreateTypeClientDto) -> TypeClientResponseDto:
        """Crea un nuevo tipo de cliente."""
        # Verificar si ya existe un tipo de cliente con el mismo código o nombre
        if self.repository.get_by_code(type_client_dto.code):
            raise ConflictException(f"Ya existe un tipo de cliente con el código '{type_client_dto.code}'.")
        if self.repository.get_by_name(type_client_dto.name):
            raise ConflictException(f"Ya existe un tipo de cliente con el nombre '{type_client_dto.name}'.")

        # Mapear DTO a modelo de dominio
        new_type_client = TypeClient(
            code=type_client_dto.code,
            name=type_client_dto.name,
            margin=type_client_dto.margin,
            created_at=datetime.now()
        )
        
        created_type_client = self.repository.save(new_type_client)
        
        # Usar model_validate para la conversión a DTO de respuesta
        return TypeClientResponseDto.model_validate(created_type_client)

    def get_type_client_by_id(self, type_client_id: int) -> TypeClientResponseDto:
        """Recupera un tipo de cliente por su ID."""
        type_client = self.repository.get_by_id(type_client_id)
        if not type_client or not type_client.is_active():
            raise NotFoundException(f"Tipo de cliente con ID {type_client_id} no encontrado o eliminado.")
        return TypeClientResponseDto.model_validate(type_client)

    def get_all_type_clients(self, skip: int = 0, limit: int = 100) -> List[TypeClientResponseDto]:
        """Recupera todos los tipos de cliente activos paginados."""
        type_clients = self.repository.get_all(skip, limit)
        active_type_clients = [tc for tc in type_clients if tc.is_active()]
        return [TypeClientResponseDto.model_validate(type_client) for type_client in active_type_clients]

    def update_type_client(self, type_client_id: int, type_client_dto: UpdateTypeClientDto) -> TypeClientResponseDto:
        """Actualiza un tipo de cliente existente."""
        existing_type_client = self.repository.get_by_id(type_client_id)
        if not existing_type_client or not existing_type_client.is_active():
            raise NotFoundException(f"Tipo de cliente con ID {type_client_id} no encontrado o eliminado.")

        # Verificar conflictos de código/nombre si se están actualizando
        if type_client_dto.code and type_client_dto.code != existing_type_client.code:
            if self.repository.get_by_code(type_client_dto.code):
                raise ConflictException(f"Ya existe otro tipo de cliente con el código '{type_client_dto.code}'.")
        if type_client_dto.name and type_client_dto.name != existing_type_client.name:
            if self.repository.get_by_name(type_client_dto.name):
                raise ConflictException(f"Ya existe otro tipo de cliente con el nombre '{type_client_dto.name}'.")

        # Actualizar el modelo de dominio con los datos del DTO
        update_data = type_client_dto.model_dump(exclude_unset=True) # exclude_unset=True para solo los campos proporcionados
        existing_type_client.update(**update_data) # Usa el método 'update' definido en el dominio

        updated_type_client = self.repository.save(existing_type_client)
        return TypeClientResponseDto.model_validate(updated_type_client)

    def delete_type_client(self, type_client_id: int) -> TypeClientResponseDto:
        """Elimina lógicamente un tipo de cliente."""
        type_client_to_delete = self.repository.get_by_id(type_client_id)
        if not type_client_to_delete or not type_client_to_delete.is_active():
            raise NotFoundException(f"Tipo de cliente con ID {type_client_id} no encontrado o ya eliminado.")
        
        type_client_to_delete.mark_as_deleted()
        
        deleted_type_client = self.repository.save(type_client_to_delete)
        return TypeClientResponseDto.model_validate(deleted_type_client)