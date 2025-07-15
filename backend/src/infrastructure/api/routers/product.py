# src/infrastructure/api/routers/product.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.application.dtos.product import CreateProductDto, UpdateProductDto, ProductResponseDto
from src.application.use_cases.product import ProductUseCases
from src.infrastructure.persistence.repositories.product import SQLAlchemyProductRepository
from src.infrastructure.persistence.repositories.product_type import SQLAlchemyProductTypeRepository
from src.infrastructure.persistence.repositories.extra_option import SQLAlchemyExtraOptionRepository
from src.application.exceptions import NotFoundException, ConflictException, ApplicationException

router = APIRouter(prefix="/products", tags=["Products"])

# Dependencia para obtener una instancia de ProductUseCases
def get_product_use_cases(db: Session = Depends(get_db)) -> ProductUseCases:
    product_repo = SQLAlchemyProductRepository(db)
    product_type_repo = SQLAlchemyProductTypeRepository(db) # Necesario para los casos de uso
    extra_option_repo = SQLAlchemyExtraOptionRepository(db) # Necesario para los casos de uso
    return ProductUseCases(product_repo, product_type_repo, extra_option_repo)

@router.post("/", response_model=ProductResponseDto, status_code=status.HTTP_201_CREATED)
def create_product(
    product_dto: CreateProductDto,
    use_cases: ProductUseCases = Depends(get_product_use_cases)
):
    try:
        return use_cases.create_product(product_dto)
    except (ConflictException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear producto: {e}")

@router.get("/{product_id}", response_model=ProductResponseDto)
def get_product(
    product_id: int,
    use_cases: ProductUseCases = Depends(get_product_use_cases)
):
    try:
        return use_cases.get_product_by_id(product_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener producto: {e}")

@router.get("/", response_model=List[ProductResponseDto])
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    use_cases: ProductUseCases = Depends(get_product_use_cases)
):
    try:
        return use_cases.get_all_products(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener productos: {e}")

@router.put("/{product_id}", response_model=ProductResponseDto)
def update_product(
    product_id: int,
    product_dto: UpdateProductDto,
    use_cases: ProductUseCases = Depends(get_product_use_cases)
):
    try:
        return use_cases.update_product(product_id, product_dto)
    except (NotFoundException, ConflictException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar producto: {e}")

@router.delete("/{product_id}", response_model=ProductResponseDto)
def delete_product(
    product_id: int,
    use_cases: ProductUseCases = Depends(get_product_use_cases)
):
    try:
        return use_cases.delete_product(product_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar producto: {e}")