# src/application/use_cases/order.py
from typing import List, Optional
from src.domain.models.order import Order
from src.domain.models.order_detail import OrderDetail, OrderDetailExtraOption
from src.application.ports.order import OrderRepository
from src.application.ports.customer import CustomerRepository
from src.application.ports.store import StoreRepository
from src.application.ports.order_status import OrderStatusRepository
from src.application.ports.product import ProductRepository
from src.application.ports.extra_option import ExtraOptionRepository
from src.application.dtos.order import CreateOrderDto, OrderResponseDto, UpdateOrderStatusDto
from src.application.dtos.order_detail import CreateOrderDetailDto
from src.application.exceptions import NotFoundException, ConflictException, ApplicationException
from datetime import datetime

class OrderUseCases:
    """
    Casos de uso para la gestión de Pedidos.
    """
    def __init__(self, 
                 repository: OrderRepository,
                 customer_repo: CustomerRepository,
                 store_repo: StoreRepository,
                 order_status_repo: OrderStatusRepository,
                 product_repo: ProductRepository,
                 extra_option_repo: ExtraOptionRepository):
        self.repository = repository
        self.customer_repo = customer_repo
        self.store_repo = store_repo
        self.order_status_repo = order_status_repo
        self.product_repo = product_repo
        self.extra_option_repo = extra_option_repo

    def create_order(self, order_dto: CreateOrderDto) -> OrderResponseDto:
        """
        Crea un nuevo pedido completo con sus detalles.
        Asume que los montos (total_amount, final_amount, etc.) ya vienen calculados del frontend.
        """
        # 1. Validar la existencia de las entidades relacionadas
        customer = self.customer_repo.get_by_id(order_dto.customer_id)
        if not customer or not customer.is_active():
            raise NotFoundException(f"Cliente con ID {order_dto.customer_id} no encontrado o eliminado.")

        store = self.store_repo.get_by_id(order_dto.store_id)
        if not store or not store.is_active():
            raise NotFoundException(f"Tienda con ID {order_dto.store_id} no encontrada o eliminada.")

        status = self.order_status_repo.get_by_id(order_dto.order_status_id)
        if not status or not status.is_active():
            raise NotFoundException(f"Estado de pedido con ID {order_dto.order_status_id} no encontrado o eliminado.")

        # 2. Mapear DTO a modelo de dominio de Order
        new_order = Order(
            customer_id=order_dto.customer_id,
            store_id=order_dto.store_id,
            order_status_id=order_dto.order_status_id,
            total_amount=order_dto.total_amount,
            profit_margin=order_dto.profit_margin,
            discount_applied=order_dto.discount_applied,
            final_amount=order_dto.final_amount,
            payment_method=order_dto.payment_method,
            shipping_address=order_dto.shipping_address,
            notes=order_dto.notes,
            created_at=datetime.now(),
            customer=customer, # Enriquecemos el modelo
            store=store,
            status=status,
            details=[]
        )

        # 3. Mapear los detalles del pedido y validar productos/extras
        for detail_dto in order_dto.details:
            # Validar que el producto existe
            product = self.product_repo.get_by_id(detail_dto.product_id)
            if not product or not product.is_active():
                raise NotFoundException(f"Producto con ID {detail_dto.product_id} no encontrado o eliminado en el detalle.")
                
            # Mapear las opciones extra y validar su existencia
            extra_options_domain = []
            for eo_dto in detail_dto.extra_options:
                extra_option = self.extra_option_repo.get_by_id(eo_dto.extra_option_id)
                if not extra_option or not extra_option.is_active():
                    raise NotFoundException(f"Opción extra con ID {eo_dto.extra_option_id} no encontrada o eliminada.")
                extra_options_domain.append(OrderDetailExtraOption(
                    extra_option_id=eo_dto.extra_option_id,
                    quantity=eo_dto.quantity,
                    linear_meter=eo_dto.linear_meter,
                    width=eo_dto.width,
                    giga_select=eo_dto.giga_select
                ))

            # Crear el detalle de dominio y añadirlo al pedido
            order_detail_domain = OrderDetail(
                order_id=new_order.id if new_order.id is not None else 0, # Temporarily 0 for creation
                product_id=detail_dto.product_id,
                height=detail_dto.height,
                width=detail_dto.width,
                quantity=detail_dto.quantity,
                linear_meter=detail_dto.linear_meter,
                subtotal=detail_dto.subtotal,
                total_extra_options=detail_dto.total_extra_options,
                extra_options=extra_options_domain,
                product=product # Enriquecemos el detalle
            )
            new_order.details.append(order_detail_domain)
            
        # 4. Guardar el pedido completo (y sus detalles anidados) en el repositorio
        created_order = self.repository.save(new_order)
        
        return OrderResponseDto.model_validate(created_order)

    def get_order_by_id(self, order_id: int) -> OrderResponseDto:
        """Recupera un pedido completo por su ID."""
        order = self.repository.get_by_id(order_id)
        if not order or not order.is_active():
            raise NotFoundException(f"Pedido con ID {order_id} no encontrado o eliminado.")
        
        return OrderResponseDto.model_validate(order)
    
    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[OrderResponseDto]:
        """Recupera todos los pedidos activos paginados."""
        orders = self.repository.get_all(skip, limit)
        active_orders = [o for o in orders if o.is_active()]
        return [OrderResponseDto.model_validate(order) for order in active_orders]

    def delete_order(self, order_id: int) -> OrderResponseDto:
        """Elimina lógicamente un pedido."""
        order_to_delete = self.repository.delete(order_id)
        if not order_to_delete:
            raise NotFoundException(f"Pedido con ID {order_id} no encontrado o ya eliminado.")
        
        return OrderResponseDto.model_validate(order_to_delete)
    
    def update_order_status(self, order_id: int, status_dto: UpdateOrderStatusDto) -> OrderResponseDto:
        """
        Actualiza el estado, notas y método de pago de un pedido existente.
        """
        # 1. Recuperar el pedido por su ID
        order_to_update = self.repository.get_by_id(order_id)
        if not order_to_update or not order_to_update.is_active():
            raise NotFoundException(f"Pedido con ID {order_id} no encontrado o eliminado.")

        # 2. Validar que el nuevo estado de pedido existe y está activo
        new_status = self.order_status_repo.get_by_id(status_dto.order_status_id)
        if not new_status or not new_status.is_active():
            raise NotFoundException(f"Estado de pedido con ID {status_dto.order_status_id} no encontrado o eliminado.")
        
        # 3. Actualizar el modelo de dominio con los nuevos datos
        order_to_update.order_status_id = status_dto.order_status_id
        if status_dto.notes is not None:
            order_to_update.notes = status_dto.notes
        if status_dto.payment_method is not None:
            order_to_update.payment_method = status_dto.payment_method
        
        # 4. Guardar los cambios a través del repositorio
        updated_order = self.repository.save(order_to_update)
        
        return OrderResponseDto.model_validate(updated_order)