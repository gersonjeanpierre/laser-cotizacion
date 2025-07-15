# src/infrastructure/api/routers/customer.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.application.dtos.customer import CreateCustomerDto, UpdateCustomerDto, CustomerResponseDto
from src.application.use_cases.customer import CustomerUseCases
from src.infrastructure.persistence.repositories.customer import SQLAlchemyCustomerRepository
from src.infrastructure.persistence.repositories.type_client import SQLAlchemyTypeClientRepository # Necesario para los casos de uso
from src.application.exceptions import NotFoundException, ConflictException, ApplicationException

router = APIRouter(prefix="/customers", tags=["Customers"])

# Dependencia para obtener una instancia de CustomerUseCases
def get_customer_use_cases(db: Session = Depends(get_db)) -> CustomerUseCases:
    customer_repo = SQLAlchemyCustomerRepository(db)
    type_client_repo = SQLAlchemyTypeClientRepository(db)
    return CustomerUseCases(customer_repo, type_client_repo)

@router.post("/", response_model=CustomerResponseDto, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer_dto: CreateCustomerDto,
    use_cases: CustomerUseCases = Depends(get_customer_use_cases)
):
    try:
        return use_cases.create_customer(customer_dto)
    except (ConflictException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ValueError as e: # Captura errores de validación de DTOs
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear cliente: {e}")

@router.get("/{customer_id}", response_model=CustomerResponseDto)
def get_customer(
    customer_id: int,
    use_cases: CustomerUseCases = Depends(get_customer_use_cases)
):
    try:
        return use_cases.get_customer_by_id(customer_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener cliente: {e}")

@router.get("/", response_model=List[CustomerResponseDto])
def get_all_customers(
    skip: int = 0,
    limit: int = 100,
    use_cases: CustomerUseCases = Depends(get_customer_use_cases)
):
    try:
        return use_cases.get_all_customers(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener clientes: {e}")

@router.put("/{customer_id}", response_model=CustomerResponseDto)
def update_customer(
    customer_id: int,
    customer_dto: UpdateCustomerDto,
    use_cases: CustomerUseCases = Depends(get_customer_use_cases)
):
    try:
        return use_cases.update_customer(customer_id, customer_dto)
    except (NotFoundException, ConflictException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ValueError as e: # Captura errores de validación de DTOs
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar cliente: {e}")

@router.delete("/{customer_id}", response_model=CustomerResponseDto)
def delete_customer(
    customer_id: int,
    use_cases: CustomerUseCases = Depends(get_customer_use_cases)
):
    try:
        return use_cases.delete_customer(customer_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar cliente: {e}")