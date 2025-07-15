# src/infrastructure/api/routers/product_type.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.application.dtos.product_type import CreateProductTypeDto, UpdateProductTypeDto, ProductTypeResponseDto
from src.application.use_cases.product_type import ProductTypeUseCases
from src.infrastructure.persistence.repositories.product_type import SQLAlchemyProductTypeRepository
from src.application.exceptions import NotFoundException, ConflictException, ApplicationException

router = APIRouter(prefix="/product_types", tags=["Product Types"])

# Dependencia para obtener una instancia de ProductTypeUseCases
def get_product_type_use_cases(db: Session = Depends(get_db)) -> ProductTypeUseCases:
    repository = SQLAlchemyProductTypeRepository(db)
    return ProductTypeUseCases(repository)

@router.post("/", response_model=ProductTypeResponseDto, status_code=status.HTTP_201_CREATED)
def create_product_type(
    product_type_dto: CreateProductTypeDto,
    use_cases: ProductTypeUseCases = Depends(get_product_type_use_cases)
):
    try:
        return use_cases.create_product_type(product_type_dto)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear tipo de producto: {e}")

@router.get("/{product_type_id}", response_model=ProductTypeResponseDto)
def get_product_type(
    product_type_id: int,
    use_cases: ProductTypeUseCases = Depends(get_product_type_use_cases)
):
    try:
        return use_cases.get_product_type_by_id(product_type_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener tipo de producto: {e}")

@router.get("/", response_model=List[ProductTypeResponseDto])
def get_all_product_types(
    skip: int = 0,
    limit: int = 100,
    use_cases: ProductTypeUseCases = Depends(get_product_type_use_cases)
):
    try:
        return use_cases.get_all_product_types(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener tipos de producto: {e}")

@router.put("/{product_type_id}", response_model=ProductTypeResponseDto)
def update_product_type(
    product_type_id: int,
    product_type_dto: UpdateProductTypeDto,
    use_cases: ProductTypeUseCases = Depends(get_product_type_use_cases)
):
    try:
        return use_cases.update_product_type(product_type_id, product_type_dto)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar tipo de producto: {e}")

@router.delete("/{product_type_id}", response_model=ProductTypeResponseDto)
def delete_product_type(
    product_type_id: int,
    use_cases: ProductTypeUseCases = Depends(get_product_type_use_cases)
):
    try:
        return use_cases.delete_product_type(product_type_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar tipo de producto: {e}")