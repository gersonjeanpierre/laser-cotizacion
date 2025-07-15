# src/infrastructure/api/routers/type_client.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.application.dtos.type_client import CreateTypeClientDto, UpdateTypeClientDto, TypeClientResponseDto
from src.application.use_cases.type_client import TypeClientUseCases
from src.infrastructure.persistence.repositories.type_client import SQLAlchemyTypeClientRepository
from src.application.exceptions import NotFoundException, ConflictException, ApplicationException

router = APIRouter(prefix="/type_clients", tags=["Type Clients"])

# Dependencia para obtener una instancia de TypeClientUseCases
def get_type_client_use_cases(db: Session = Depends(get_db)) -> TypeClientUseCases:
    repository = SQLAlchemyTypeClientRepository(db)
    return TypeClientUseCases(repository)

@router.post("/", response_model=TypeClientResponseDto, status_code=status.HTTP_201_CREATED)
def create_type_client(
    type_client_dto: CreateTypeClientDto,
    use_cases: TypeClientUseCases = Depends(get_type_client_use_cases)
):
    try:
        return use_cases.create_type_client(type_client_dto)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear tipo de cliente: {e}")

@router.get("/{type_client_id}", response_model=TypeClientResponseDto)
def get_type_client(
    type_client_id: int,
    use_cases: TypeClientUseCases = Depends(get_type_client_use_cases)
):
    try:
        return use_cases.get_type_client_by_id(type_client_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener tipo de cliente: {e}")

@router.get("/", response_model=List[TypeClientResponseDto])
def get_all_type_clients(
    skip: int = 0,
    limit: int = 100,
    use_cases: TypeClientUseCases = Depends(get_type_client_use_cases)
):
    try:
        return use_cases.get_all_type_clients(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener tipos de cliente: {e}")

@router.put("/{type_client_id}", response_model=TypeClientResponseDto)
def update_type_client(
    type_client_id: int,
    type_client_dto: UpdateTypeClientDto,
    use_cases: TypeClientUseCases = Depends(get_type_client_use_cases)
):
    try:
        return use_cases.update_type_client(type_client_id, type_client_dto)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar tipo de cliente: {e}")

@router.delete("/{type_client_id}", response_model=TypeClientResponseDto)
def delete_type_client(
    type_client_id: int,
    use_cases: TypeClientUseCases = Depends(get_type_client_use_cases)
):
    try:
        return use_cases.delete_type_client(type_client_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar tipo de cliente: {e}")