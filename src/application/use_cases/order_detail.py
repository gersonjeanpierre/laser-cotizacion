# src/application/use_cases/order_detail.py
from typing import List, Optional
from src.domain.models.order_detail import OrderDetail, OrderDetailExtraOption
from src.application.ports.order_detail import OrderDetailRepository
from src.application.dtos.order_detail import CreateOrderDetailDto, OrderDetailResponseDto
from src.application.exceptions import NotFoundException, ConflictException
from datetime import datetime

# Asumimos que tenemos un ProductRepository y un ExtraOptionRepository para validar
from src.application.ports.product import ProductRepository # Necesario para validar existencia del producto
from src.application.ports.extra_option import ExtraOptionRepository # Necesario para validar existencia de extras

class OrderDetailUseCases:
    """
    Casos de uso para la gestión de Detalles de Pedido.
    """
    def __init__(self, 
                 repository: OrderDetailRepository,
                 product_repo: ProductRepository,
                 extra_option_repo: ExtraOptionRepository):
        self.repository = repository
        self.product_repo = product_repo
        self.extra_option_repo = extra_option_repo

    def create_order_detail(self, order_id: int, detail_dto: CreateOrderDetailDto) -> OrderDetailResponseDto:
        """
        Crea un nuevo detalle de pedido para un pedido existente.
        Nota: Asume que el subtotal y total_extra_options vienen calculados desde el frontend.
        """
        # 1. Validar que el producto existe
        product = self.product_repo.get_by_id(detail_dto.product_id)
        if not product or not product.is_active():
            raise NotFoundException(f"Producto con ID {detail_dto.product_id} no encontrado o eliminado.")

        # 2. Validar que las opciones extra existen
        for extra_option_dto in detail_dto.extra_options:
            extra_option = self.extra_option_repo.get_by_id(extra_option_dto.extra_option_id)
            if not extra_option or not extra_option.is_active():
                raise NotFoundException(f"Opción extra con ID {extra_option_dto.extra_option_id} no encontrada o eliminada.")
        
        # 3. Mapear DTO a modelo de dominio de OrderDetail
        # El subtotal y total_extra_options se añadirán al crear el Order
        # Este caso de uso solo crea el detalle, no el pedido completo
        new_detail = OrderDetail(
            order_id=order_id,
            product_id=detail_dto.product_id,
            quantity=detail_dto.quantity,
            height=detail_dto.height,
            width=detail_dto.width,
            linear_meter=detail_dto.linear_meter,
            subtotal=0, # <-- Este valor se recalculará al crear el Order
            total_extra_options=0, # <-- Este valor se recalculará al crear el Order
            created_at=datetime.now()
        )
        
        # Mapear las opciones extra
        new_detail.extra_options = [
            OrderDetailExtraOption(
                extra_option_id=eo_dto.extra_option_id,
                quantity=eo_dto.quantity,
                linear_meter=eo_dto.linear_meter,
                width=eo_dto.width,
            ) for eo_dto in detail_dto.extra_options
        ]
        
        created_detail = self.repository.save(new_detail)
        return OrderDetailResponseDto.model_validate(created_detail)

    def get_order_details_by_order_id(self, order_id: int) -> List[OrderDetailResponseDto]:
        """Recupera todos los detalles de pedido para un ID de pedido dado."""
        details = self.repository.get_all_by_order_id(order_id)
        active_details = [d for d in details if d.is_active()]
        return [OrderDetailResponseDto.model_validate(detail) for detail in active_details]

    def delete_order_detail(self, detail_id: int) -> OrderDetailResponseDto:
        """Elimina lógicamente un detalle de pedido."""
        detail_to_delete = self.repository.get_by_id(detail_id)
        if not detail_to_delete or not detail_to_delete.is_active():
            raise NotFoundException(f"Detalle de pedido con ID {detail_id} no encontrado o ya eliminado.")
        
        detail_to_delete.mark_as_deleted()
        
        deleted_detail = self.repository.save(detail_to_delete)
        return OrderDetailResponseDto.model_validate(deleted_detail)