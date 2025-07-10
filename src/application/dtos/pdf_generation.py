from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# DTO para las opciones extra que vienen de Angular
class AngularExtraOptionDto(BaseModel):
    extra_option_id: int
    quantity: float  # Cambiado a float porque puede ser 1.5
    linear_meter: Optional[float] = None
    name: str
    price: float

# DTO para los items que vienen de Angular
class AngularCartItemDto(BaseModel):
    id: Optional[int] = None  # ID del detalle de orden
    order_id: Optional[int] = None
    product_id: int
    height: float
    width: float
    quantity: int
    linear_meter: float
    subtotal: float
    total_extra_options: float
    created_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    extra_options: List[AngularExtraOptionDto]
    sku: str
    name: str
    price: float
    image: str

# DTO para el request de generación de PDF
class GeneratePdfRequest(BaseModel):
    items: List[AngularCartItemDto] = Field(..., description="Lista de ítems detallados del carrito para la generación del PDF.")