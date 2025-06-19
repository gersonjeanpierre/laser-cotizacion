# src/application/dtos/order.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateOrderDto(BaseModel):
    customer_id: int = Field(..., description="ID del cliente que realiza el pedido")
    store_id: int = Field(..., description="ID de la tienda donde se realizó el pedido")
    order_status_id: int = Field(..., description="ID del estado inicial del pedido")
    
    # order_date se generará en la capa de aplicación o persistencia, no se recibe aquí
    # total_amount, profit_margin, final_amount se calcularán en la lógica de negocio
    
    discount_applied: float = Field(0.00, ge=0, description="Descuento aplicado al pedido")
    payment_method: Optional[str] = Field(None, max_length=50, description="Método de pago")
    shipping_address: Optional[str] = Field(None, max_length=200, description="Dirección de envío")
    notes: Optional[str] = Field(None, max_length=200, description="Notas adicionales para el pedido")

class UpdateOrderDto(BaseModel):
    customer_id: Optional[int] = Field(None, description="ID del cliente")
    store_id: Optional[int] = Field(None, description="ID de la tienda")
    order_status_id: Optional[int] = Field(None, description="ID del estado actual del pedido")
    # No se actualiza order_date
    # Los montos se recalcularán si se actualizan los detalles, no se actualizan directamente
    discount_applied: Optional[float] = Field(None, ge=0, description="Descuento aplicado al pedido")
    payment_method: Optional[str] = Field(None, max_length=50, description="Método de pago")
    shipping_address: Optional[str] = Field(None, max_length=200, description="Dirección de envío")
    notes: Optional[str] = Field(None, max_length=200, description="Notas adicionales para el pedido")

class OrderResponseDto(BaseModel):
    id: int
    customer_id: int
    store_id: int
    order_status_id: int
    order_date: datetime
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

    class Config:
        from_attributes = True