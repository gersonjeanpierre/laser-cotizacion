# src/application/dtos/order_status.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateOrderStatusDto(BaseModel):
    code: str = Field(..., max_length=10, description="Código único del estado de pedido")
    name: str = Field(..., max_length=50, description="Nombre descriptivo del estado de pedido")
    description: Optional[str] = Field(None, description="Descripción del estado de pedido")

class UpdateOrderStatusDto(BaseModel):
    code: Optional[str] = Field(None, max_length=10, description="Código único del estado de pedido")
    name: Optional[str] = Field(None, max_length=50, description="Nombre descriptivo del estado de pedido")
    description: Optional[str] = Field(None, description="Descripción del estado de pedido")

class OrderStatusResponseDto(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True