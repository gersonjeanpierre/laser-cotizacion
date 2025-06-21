# src/application/use_cases/order_status.py
from typing import List, Optional
from src.domain.models.order_status import OrderStatus
from src.application.ports.order_status import OrderStatusRepository
from src.application.dtos.order_status import CreateOrderStatusDto, UpdateOrderStatusDto, OrderStatusResponseDto
from src.application.exceptions import NotFoundException, ConflictException
from datetime import datetime

class OrderStatusUseCases:
    """
    Casos de uso para la gestión de Estados de Pedido.
    """
    def __init__(self, repository: OrderStatusRepository):
        self.repository = repository

    def create_order_status(self, status_dto: CreateOrderStatusDto) -> OrderStatusResponseDto:
        """Crea un nuevo estado de pedido."""
        if self.repository.get_by_code(status_dto.code):
            raise ConflictException(f"Ya existe un estado de pedido con el código '{status_dto.code}'.")
        if self.repository.get_by_name(status_dto.name):
            raise ConflictException(f"Ya existe un estado de pedido con el nombre '{status_dto.name}'.")

        new_status = OrderStatus(
            code=status_dto.code,
            name=status_dto.name,
            description=status_dto.description,
            created_at=datetime.now()
        )
        created_status = self.repository.save(new_status)
        return OrderStatusResponseDto.model_validate(created_status)

    def get_order_status_by_id(self, status_id: int) -> OrderStatusResponseDto:
        """Recupera un estado de pedido por su ID."""
        status = self.repository.get_by_id(status_id)
        if not status or not status.is_active():
            raise NotFoundException(f"Estado de pedido con ID {status_id} no encontrado o eliminado.")
        return OrderStatusResponseDto.model_validate(status)

    def get_all_order_statuses(self, skip: int = 0, limit: int = 100) -> List[OrderStatusResponseDto]:
        """Recupera todos los estados de pedido activos paginados."""
        statuses = self.repository.get_all(skip, limit)
        active_statuses = [s for s in statuses if s.is_active()]
        return [OrderStatusResponseDto.model_validate(status) for status in active_statuses]

    def update_order_status(self, status_id: int, status_dto: UpdateOrderStatusDto) -> OrderStatusResponseDto:
        """Actualiza un estado de pedido existente."""
        existing_status = self.repository.get_by_id(status_id)
        if not existing_status or not existing_status.is_active():
            raise NotFoundException(f"Estado de pedido con ID {status_id} no encontrado o eliminado.")

        if status_dto.code and status_dto.code != existing_status.code:
            if self.repository.get_by_code(status_dto.code):
                raise ConflictException(f"Ya existe otro estado de pedido con el código '{status_dto.code}'.")
        if status_dto.name and status_dto.name != existing_status.name:
            if self.repository.get_by_name(status_dto.name):
                raise ConflictException(f"Ya existe otro estado de pedido con el nombre '{status_dto.name}'.")

        update_data = status_dto.model_dump(exclude_unset=True)
        existing_status.update(**update_data)
        
        updated_status = self.repository.save(existing_status)
        return OrderStatusResponseDto.model_validate(updated_status)

    def delete_order_status(self, status_id: int) -> OrderStatusResponseDto:
        """Elimina lógicamente un estado de pedido."""
        status_to_delete = self.repository.get_by_id(status_id)
        if not status_to_delete or not status_to_delete.is_active():
            raise NotFoundException(f"Estado de pedido con ID {status_id} no encontrado o ya eliminado.")
        
        status_to_delete.mark_as_deleted()
        
        deleted_status = self.repository.save(status_to_delete)
        return OrderStatusResponseDto.model_validate(deleted_status)