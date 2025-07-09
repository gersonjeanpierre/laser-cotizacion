# src/infrastructure/api/routers/order.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse # Necesario para devolver el PDF
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field # Necesario para definir DTOs si no están en otro archivo
from io import BytesIO # Necesario para manejar el buffer del PDF


# Importa las dependencias necesarias
from src.infrastructure.database.database import get_db
from src.application.dtos.order import CreateOrderDto, OrderResponseDto, UpdateOrderStatusDto
from src.application.use_cases.order import OrderUseCases
from src.infrastructure.persistence.repositories.order import SQLAlchemyOrderRepository
from src.infrastructure.persistence.repositories.customer import SQLAlchemyCustomerRepository
from src.infrastructure.persistence.repositories.store import SQLAlchemyStoreRepository
from src.infrastructure.persistence.repositories.order_status import SQLAlchemyOrderStatusRepository
from src.infrastructure.persistence.repositories.product import SQLAlchemyProductRepository
from src.infrastructure.persistence.repositories.extra_option import SQLAlchemyExtraOptionRepository
from src.application.exceptions import NotFoundException, ConflictException

# Importa el servicio de generación de PDF
from src.services.pdf_generator import generate_order_pdf

# Importa los DTOs necesarios para el request del PDF desde el servicio de PDF
# Estos DTOs son específicos para la información detallada que el frontend envía para la impresión
# Si estos DTOs se usaran en otros lugares, podrías moverlos a un archivo `src/application/dtos/pdf_generation.py`
from src.services.pdf_generator import (
    DisplayCartItemSchema,
    DisplayProductExtraOptionSchema,
    MyCartDetailExtraOptionSchema # Aunque no se usa directamente en el endpoint, es parte del esquema
)

router = APIRouter(prefix="/orders", tags=["Orders"])

# Dependencia para obtener una instancia de OrderUseCases
def get_order_use_cases(db: Session = Depends(get_db)) -> OrderUseCases:
    order_repo = SQLAlchemyOrderRepository(db)
    customer_repo = SQLAlchemyCustomerRepository(db)
    store_repo = SQLAlchemyStoreRepository(db)
    order_status_repo = SQLAlchemyOrderStatusRepository(db)
    product_repo = SQLAlchemyProductRepository(db)
    extra_option_repo = SQLAlchemyExtraOptionRepository(db)
    
    return OrderUseCases(
        repository=order_repo,
        customer_repo=customer_repo,
        store_repo=store_repo,
        order_status_repo=order_status_repo,
        product_repo=product_repo,
        extra_option_repo=extra_option_repo
    )

# DTO para el cuerpo de la solicitud del PDF (lo que Angular enviará)
class GeneratePdfRequest(BaseModel):
    items: List[DisplayCartItemSchema] = Field(..., description="Lista de ítems detallados del carrito para la generación del PDF.")


@router.post("/", response_model=OrderResponseDto, status_code=status.HTTP_201_CREATED)
def create_order(
    order_dto: CreateOrderDto,
    use_cases: OrderUseCases = Depends(get_order_use_cases)
):
    """
    Crea un nuevo pedido con sus detalles y opciones extra.
    """
    try:
        return use_cases.create_order(order_dto)
    except (NotFoundException, ConflictException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        # Registra la excepción para depuración
        print(f"Error al crear el pedido: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor al crear el pedido.")

@router.get("/{order_id}", response_model=OrderResponseDto)
def get_order(
    order_id: int,
    use_cases: OrderUseCases = Depends(get_order_use_cases)
):
    """
    Obtiene los detalles de un pedido por su ID.
    """
    try:
        return use_cases.get_order_by_id(order_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener el pedido: {e}")

@router.get("/", response_model=List[OrderResponseDto])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    use_cases: OrderUseCases = Depends(get_order_use_cases)
):
    """
    Obtiene una lista de todos los pedidos activos.
    """
    try:
        return use_cases.get_all_orders(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener los pedidos: {e}")

@router.delete("/{order_id}", response_model=OrderResponseDto)
def delete_order(
    order_id: int,
    use_cases: OrderUseCases = Depends(get_order_use_cases)
):
    """
    Elimina lógicamente un pedido por su ID.
    """
    try:
        return use_cases.delete_order(order_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar el pedido: {e}")
    
@router.patch("/{order_id}/status", response_model=OrderResponseDto)
def update_order_status(
    order_id: int,
    status_dto: UpdateOrderStatusDto,
    use_cases: OrderUseCases = Depends(get_order_use_cases)
):
    """
    Actualiza el estado de un pedido por su ID.
    """
    try:
        return use_cases.update_order_status(order_id, status_dto)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar el estado del pedido: {e}")

@router.post("/{order_id}/generate-pdf", response_class=StreamingResponse)
async def generate_pdf_for_order(
    order_id: int,
    request_data: GeneratePdfRequest, # Aquí recibimos los ítems detallados desde Angular
    use_cases: OrderUseCases = Depends(get_order_use_cases)
):
    """
    Genera un PDF de la orden especificada.
    El cuerpo de la solicitud debe contener los detalles del carrito desde el frontend,
    que son utilizados para la representación visual en el PDF (nombres, SKUs, etc.).
    """
    try:
        # 1. Obtener la orden completa desde la capa de casos de uso
        # Asumimos que get_order_by_id en OrderUseCases ya carga las relaciones (cliente, tienda, estado, detalles de la orden con productos)
        order = use_cases.get_order_by_id(order_id)
        
        if not order:
            raise NotFoundException(f"Order with ID {order_id} not found.")

        # 2. Generar el PDF utilizando la información oficial de la orden del backend
        # y los detalles de display del frontend (para nombres, SKUs, etc.)
        pdf_buffer = generate_order_pdf(
            order=order,
            display_items=request_data.items
        )

        # 3. Devolver el PDF como una respuesta de streaming
        return StreamingResponse(pdf_buffer, media_type="application/pdf", headers={
            "Content-Disposition": f"attachment; filename=orden_{order_id}.pdf"
        })

    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        print(f"Error al generar el PDF para la orden {order_id}: {e}") # Para depuración
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor al generar el PDF: {e}")

