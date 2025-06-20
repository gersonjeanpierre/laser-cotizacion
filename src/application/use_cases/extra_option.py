# src/application/use_cases/extra_option.py
from typing import List, Optional
from src.domain.models.extra_option import ExtraOption
from src.application.ports.extra_option import ExtraOptionRepository
from src.application.dtos.extra_option import CreateExtraOptionDto, UpdateExtraOptionDto, ExtraOptionResponseDto
from src.application.exceptions import NotFoundException, ConflictException
from datetime import datetime

class ExtraOptionUseCases:
    """
    Casos de uso para la gestión de Opciones Extra.
    """
    def __init__(self, repository: ExtraOptionRepository):
        self.repository = repository

    def create_extra_option(self, extra_option_dto: CreateExtraOptionDto) -> ExtraOptionResponseDto:
        """Crea una nueva opción extra."""
        if self.repository.get_by_name(extra_option_dto.name):
            raise ConflictException(f"Ya existe una opción extra con el nombre '{extra_option_dto.name}'.")

        new_extra_option = ExtraOption(
            name=extra_option_dto.name,
            price=extra_option_dto.price,
            description=extra_option_dto.description,
            created_at=datetime.now()
        )
        
        created_extra_option = self.repository.save(new_extra_option)
        
        return ExtraOptionResponseDto.model_validate(created_extra_option)

    def get_extra_option_by_id(self, extra_option_id: int) -> ExtraOptionResponseDto:
        """Recupera una opción extra por su ID."""
        extra_option = self.repository.get_by_id(extra_option_id)
        if not extra_option or not extra_option.is_active():
            raise NotFoundException(f"Opción extra con ID {extra_option_id} no encontrada o eliminada.")
        return ExtraOptionResponseDto.model_validate(extra_option)

    def get_all_extra_options(self, skip: int = 0, limit: int = 100) -> List[ExtraOptionResponseDto]:
        """Recupera todas las opciones extra activas paginadas."""
        extra_options = self.repository.get_all(skip, limit)
        active_extra_options = [eo for eo in extra_options if eo.is_active()]
        return [ExtraOptionResponseDto.model_validate(extra_option) for extra_option in active_extra_options]

    def update_extra_option(self, extra_option_id: int, extra_option_dto: UpdateExtraOptionDto) -> ExtraOptionResponseDto:
        """Actualiza una opción extra existente."""
        existing_extra_option = self.repository.get_by_id(extra_option_id)
        if not existing_extra_option or not existing_extra_option.is_active():
            raise NotFoundException(f"Opción extra con ID {extra_option_id} no encontrada o eliminada.")

        if extra_option_dto.name and extra_option_dto.name != existing_extra_option.name:
            if self.repository.get_by_name(extra_option_dto.name):
                raise ConflictException(f"Ya existe otra opción extra con el nombre '{extra_option_dto.name}'.")

        update_data = extra_option_dto.model_dump(exclude_unset=True)
        existing_extra_option.update(**update_data)

        updated_extra_option = self.repository.save(existing_extra_option)
        return ExtraOptionResponseDto.model_validate(updated_extra_option)

    def delete_extra_option(self, extra_option_id: int) -> ExtraOptionResponseDto:
        """Elimina lógicamente una opción extra."""
        extra_option_to_delete = self.repository.get_by_id(extra_option_id)
        if not extra_option_to_delete or not extra_option_to_delete.is_active():
            raise NotFoundException(f"Opción extra con ID {extra_option_id} no encontrada o ya eliminada.")
        
        extra_option_to_delete.mark_as_deleted()
        
        deleted_extra_option = self.repository.save(extra_option_to_delete)
        return ExtraOptionResponseDto.model_validate(deleted_extra_option)