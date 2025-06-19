# src/application/use_cases/store.py
from typing import List, Optional
from src.domain.models.store import Store
from src.application.ports.store import StoreRepository
from src.application.dtos.store import CreateStoreDto, UpdateStoreDto, StoreResponseDto
from src.application.exceptions import NotFoundException, ConflictException
from datetime import datetime

class StoreUseCases:
    """
    Casos de uso para la gestión de Tiendas.
    Orquesta la lógica de negocio y el acceso a la persistencia.
    """
    def __init__(self, repository: StoreRepository):
        self.repository = repository

    def create_store(self, store_dto: CreateStoreDto) -> StoreResponseDto:
        """Crea una nueva tienda."""
        # Verificar si ya existe una tienda con el mismo nombre o código (si se proporciona)
        if self.repository.get_by_name(store_dto.name):
            raise ConflictException(f"Ya existe una tienda con el nombre '{store_dto.name}'.")
        if store_dto.code and self.repository.get_by_code(store_dto.code):
            raise ConflictException(f"Ya existe una tienda con el código '{store_dto.code}'.")

        # Mapear DTO de entrada a modelo de dominio
        new_store = Store(
            name=store_dto.name,
            code=store_dto.code,
            address=store_dto.address,
            phone_number=store_dto.phone_number,
            email=store_dto.email,
            created_at=datetime.now() # Fecha de creación se asigna aquí o en el repositorio
        )
        
        # Guardar el modelo de dominio usando el repositorio (interfaz)
        created_store = self.repository.save(new_store)
        
        # Mapear modelo de dominio a DTO de respuesta
        return StoreResponseDto.model_validate(created_store) # <-- CAMBIO AQUÍ

    def get_store_by_id(self, store_id: int) -> StoreResponseDto:
        """Recupera una tienda por su ID."""
        store = self.repository.get_by_id(store_id)
        if not store or not store.is_active():
            raise NotFoundException(f"Tienda con ID {store_id} no encontrada o eliminada.")
        return StoreResponseDto.model_validate(store) # <-- CAMBIO AQUÍ

    def get_all_stores(self, skip: int = 0, limit: int = 100) -> List[StoreResponseDto]:
        """Recupera todas las tiendas activas paginadas."""
        stores = self.repository.get_all(skip, limit)
        # Filtrar solo las tiendas activas si el repositorio trae también las eliminadas lógicamente
        active_stores = [s for s in stores if s.is_active()]
        return [StoreResponseDto.model_validate(store) for store in active_stores] # <-- CAMBIO AQUÍ

    def update_store(self, store_id: int, store_dto: UpdateStoreDto) -> StoreResponseDto:
        """Actualiza una tienda existente."""
        existing_store = self.repository.get_by_id(store_id)
        if not existing_store or not existing_store.is_active():
            raise NotFoundException(f"Tienda con ID {store_id} no encontrada o eliminada.")

        # Verificar conflictos de nombre/código si se están actualizando
        if store_dto.name and store_dto.name != existing_store.name:
            if self.repository.get_by_name(store_dto.name):
                raise ConflictException(f"Ya existe otra tienda con el nombre '{store_dto.name}'.")
        if store_dto.code and store_dto.code != existing_store.code:
            if self.repository.get_by_code(store_dto.code):
                raise ConflictException(f"Ya existe otra tienda con el código '{store_dto.code}'.")

        # Actualizar el modelo de dominio con los datos del DTO
        update_data = store_dto.model_dump(exclude_unset=True) # exclude_unset=True para solo los campos proporcionados
        
        # El método update del dominio maneja la actualización y updated_at
        existing_store.update(**update_data) # Esto ahora es válido porque ya definimos el método 'update' en Store

        updated_store = self.repository.save(existing_store)
        return StoreResponseDto.model_validate(updated_store) # <-- CAMBIO AQUÍ

    def delete_store(self, store_id: int) -> StoreResponseDto:
        """Elimina lógicamente una tienda."""
        store_to_delete = self.repository.get_by_id(store_id)
        if not store_to_delete or not store_to_delete.is_active():
            raise NotFoundException(f"Tienda con ID {store_id} no encontrada o ya eliminada.")
        
        # La lógica de "mark_as_deleted" está en el modelo de dominio
        store_to_delete.mark_as_deleted()
        
        deleted_store = self.repository.save(store_to_delete) # Persistir el cambio de estado
        return StoreResponseDto.model_validate(deleted_store) # <-- CAMBIO AQUÍ