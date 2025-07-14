# src/application/dtos/order.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from src.application.dtos.order_detail import CreateOrderDetailDto, OrderDetailResponseDto
from src.application.dtos.customer import CustomerResponseDto
from src.application.dtos.store import StoreResponseDto
from src.application.dtos.order_status import OrderStatusResponseDto

# DTO para crear un pedido completo
class CreateOrderDto(BaseModel):
    customer_id: int = Field(..., description="ID del cliente que realiza el pedido.")
    store_id: int = Field(..., description="ID de la tienda donde se realizó el pedido.")
    order_status_id: int = Field(..., description="ID del estado inicial del pedido (ej. Pendiente).")
    total_amount: float = Field(..., gt=0, description="Monto total del pedido antes de descuentos e impuestos.")
    profit_margin: float = Field(..., description="Margen de ganancia del pedido.")
    discount_applied: float = Field(0.00, ge=0, description="Descuento total aplicado al pedido.")
    final_amount: float = Field(..., gt=0, description="Monto final a pagar, después de aplicar descuentos y el margen de ganancia.")
    payment_method: Optional[str] = Field(None, max_length=50)
    shipping_address: Optional[str] = Field(None, max_length=200)
    notes: Optional[str] = Field(None, max_length=200)
    
    # Lista de detalles del pedido, usando el DTO que ya definimos
    details: List[CreateOrderDetailDto] = Field(..., description="Lista de productos y sus opciones en el pedido.")

# DTO para la respuesta de un pedido
class OrderResponseDto(BaseModel):
    id: int
    customer_id: int
    store_id: int
    order_status_id: int
    total_amount: float
    profit_margin: float
    discount_applied: float
    final_amount: float
    payment_method: Optional[str]
    shipping_address: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    # Incluimos los detalles del pedido
    details: List[OrderDetailResponseDto] = Field(default_factory=list)
    
    # Incluimos las relaciones para una respuesta más completa
    customer: Optional[CustomerResponseDto] = None
    store: Optional[StoreResponseDto] = None
    status: Optional[OrderStatusResponseDto] = None
    
    class Config:
        from_attributes = True

class UpdateOrderStatusDto(BaseModel):
    order_status_id: int = Field(..., description="El nuevo ID del estado del pedido.")
    notes: Optional[str] = Field(None, max_length=200, description="Notas adicionales sobre el cambio de estado.")
    payment_method: Optional[str] = Field(None, description="Método de pago del pedido.")