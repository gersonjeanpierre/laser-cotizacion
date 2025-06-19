# src/application/dtos/order_detail.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CreateOrderDetailDto(BaseModel):
    order_id: int = Field(..., description="ID del pedido al que pertenece este detalle")
    product_id: int = Field(..., description="ID del producto en este detalle")
    quantity: int = Field(..., gt=0, description="Cantidad del producto")
    unit_price: float = Field(..., gt=0, description="Precio unitario del producto al momento de la venta")
    
    # Las opciones extra para el detalle se manejarán a través de un DTO específico o endpoint
    extra_option_ids: Optional[List[int]] = Field(None, description="Lista de IDs de opciones extras para este detalle (se necesitará el precio en el momento del pedido)")

class UpdateOrderDetailDto(BaseModel):
    order_id: Optional[int] = Field(None, description="ID del pedido")
    product_id: Optional[int] = Field(None, description="ID del producto")
    quantity: Optional[int] = Field(None, gt=0, description="Cantidad del producto")
    unit_price: Optional[float] = Field(None, gt=0, description="Precio unitario del producto")
    # total_extra_options y subtotal se recalculan
    extra_option_ids: Optional[List[int]] = Field(None, description="Lista de IDs de opciones extras a actualizar para este detalle")


class OrderDetailResponseDto(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_extra_options: float
    subtotal: float
    created_at: datetime
    deleted_at: Optional[datetime]
    
    # Si quieres incluir las opciones extra en la respuesta del detalle, necesitarías un DTO anidado
    # o una lista de IDs de las opciones extra asociadas y sus precios.
    # Por simplicidad, por ahora solo las IDs de las opciones extra si las hay
    extra_option_ids: List[int] = Field(default_factory=list) # IDs de las extra options aplicadas a este detalle

    class Config:
        from_attributes = True

# DTO específico para añadir/eliminar una opción extra a un detalle de pedido
class OrderDetailExtraOptionDto(BaseModel):
    extra_option_id: int
    price_at_order: float = Field(..., ge=0, description="Precio de la opción extra en el momento del pedido")