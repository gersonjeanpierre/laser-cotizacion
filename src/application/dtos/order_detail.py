# src/application/dtos/order_detail.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# DTO para crear una opción extra de detalle de pedido
class CreateOrderDetailExtraOptionDto(BaseModel):
    extra_option_id: int = Field(..., description="ID de la opción extra.")
    quantity: float = Field(..., gt=0, description="Cantidad de la opción extra.")
    linear_meter: Optional[float] = Field(None, gt=0, description="Medida lineal si aplica.")
    width: Optional[float] = Field(None, gt=0, description="Ancho de la opción extra.")

# DTO para crear un detalle de pedido
class CreateOrderDetailDto(BaseModel):
    product_id: int = Field(..., description="ID del producto.")
    height: Optional[float] = Field(None, gt=0, description="Altura del producto.")
    width: Optional[float] = Field(None, gt=0, description="Ancho del producto.")
    quantity: int = Field(..., gt=0, description="Cantidad del producto.")
    linear_meter: Optional[float] = Field(None, gt=0, description="Medida lineal si aplica.")
    extra_options: List[CreateOrderDetailExtraOptionDto] = Field(default_factory=list, description="Opciones extra del detalle.")

# DTOs de respuesta
class OrderDetailExtraOptionResponseDto(BaseModel):
    extra_option_id: int
    quantity: float
    linear_meter: Optional[float]
    
    class Config:
        from_attributes = True

class OrderDetailResponseDto(BaseModel):
    id: int
    order_id: int
    product_id: int
    height: Optional[float]
    width: Optional[float]
    quantity: int
    linear_meter: Optional[float]
    subtotal: float
    total_extra_options: float
    created_at: datetime
    deleted_at: Optional[datetime]
    extra_options: List[OrderDetailExtraOptionResponseDto] = Field(default_factory=list)

    class Config:
        from_attributes = True