# src/infrastructure/api/routers/store.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.application.dtos.store import CreateStoreDto, UpdateStoreDto, StoreResponseDto
from src.application.use_cases.store import StoreUseCases
from src.infrastructure.persistence.repositories.store import SQLAlchemyStoreRepository
from src.application.exceptions import NotFoundException, ConflictException, ApplicationException

router = APIRouter(prefix="/stores", tags=["Stores"])

# Dependencia para obtener una instancia de StoreUseCases
def get_store_use_cases(db: Session = Depends(get_db)) -> StoreUseCases:
    repository = SQLAlchemyStoreRepository(db)
    return StoreUseCases(repository)

@router.post("/", response_model=StoreResponseDto, status_code=status.HTTP_201_CREATED)
def create_store(
    store_dto: CreateStoreDto,
    use_cases: StoreUseCases = Depends(get_store_use_cases)
):
    try:
        return use_cases.create_store(store_dto)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear tienda: {e}")

@router.get("/{store_id}", response_model=StoreResponseDto)
def get_store(
    store_id: int,
    use_cases: StoreUseCases = Depends(get_store_use_cases)
):
    try:
        return use_cases.get_store_by_id(store_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener tienda: {e}")

@router.get("/", response_model=List[StoreResponseDto])
def get_all_stores(
    skip: int = 0,
    limit: int = 100,
    use_cases: StoreUseCases = Depends(get_store_use_cases)
):
    try:
        return use_cases.get_all_stores(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener tiendas: {e}")

@router.put("/{store_id}", response_model=StoreResponseDto)
def update_store(
    store_id: int,
    store_dto: UpdateStoreDto,
    use_cases: StoreUseCases = Depends(get_store_use_cases)
):
    try:
        return use_cases.update_store(store_id, store_dto)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar tienda: {e}")

@router.delete("/{store_id}", response_model=StoreResponseDto)
def delete_store(
    store_id: int,
    use_cases: StoreUseCases = Depends(get_store_use_cases)
):
    try:
        return use_cases.delete_store(store_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar tienda: {e}")