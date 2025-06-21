# src/infrastructure/api/routers/order_status.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.application.dtos.order_status import CreateOrderStatusDto, UpdateOrderStatusDto, OrderStatusResponseDto
from src.application.use_cases.order_status import OrderStatusUseCases
from src.infrastructure.persistence.repositories.order_status import SQLAlchemyOrderStatusRepository
from src.application.exceptions import NotFoundException, ConflictException, ApplicationException

router = APIRouter(prefix="/order_statuses", tags=["Order Statuses"])

# Dependencia para obtener una instancia de OrderStatusUseCases
def get_order_status_use_cases(db: Session = Depends(get_db)) -> OrderStatusUseCases:
    repo = SQLAlchemyOrderStatusRepository(db)
    return OrderStatusUseCases(repo)

@router.post("/", response_model=OrderStatusResponseDto, status_code=status.HTTP_201_CREATED)
def create_order_status(
    status_dto: CreateOrderStatusDto,
    use_cases: OrderStatusUseCases = Depends(get_order_status_use_cases)
):
    try:
        return use_cases.create_order_status(status_dto)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear estado de pedido: {e}")

@router.get("/{status_id}", response_model=OrderStatusResponseDto)
def get_order_status(
    status_id: int,
    use_cases: OrderStatusUseCases = Depends(get_order_status_use_cases)
):
    try:
        return use_cases.get_order_status_by_id(status_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener estado de pedido: {e}")

@router.get("/", response_model=List[OrderStatusResponseDto])
def get_all_order_statuses(
    skip: int = 0,
    limit: int = 100,
    use_cases: OrderStatusUseCases = Depends(get_order_status_use_cases)
):
    try:
        return use_cases.get_all_order_statuses(skip, limit)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener estados de pedido: {e}")

@router.put("/{status_id}", response_model=OrderStatusResponseDto)
def update_order_status(
    status_id: int,
    status_dto: UpdateOrderStatusDto,
    use_cases: OrderStatusUseCases = Depends(get_order_status_use_cases)
):
    try:
        return use_cases.update_order_status(status_id, status_dto)
    except (NotFoundException, ConflictException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar estado de pedido: {e}")

@router.delete("/{status_id}", response_model=OrderStatusResponseDto)
def delete_order_status(
    status_id: int,
    use_cases: OrderStatusUseCases = Depends(get_order_status_use_cases)
):
    try:
        return use_cases.delete_order_status(status_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar estado de pedido: {e}")