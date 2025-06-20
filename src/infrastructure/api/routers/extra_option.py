# src/infrastructure/api/routers/extra_option.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.application.dtos.extra_option import CreateExtraOptionDto, UpdateExtraOptionDto, ExtraOptionResponseDto
from src.application.use_cases.extra_option import ExtraOptionUseCases
from src.infrastructure.persistence.repositories.extra_option import SQLAlchemyExtraOptionRepository
from src.application.exceptions import NotFoundException, ConflictException, ApplicationException

router = APIRouter(prefix="/extra_options", tags=["Extra Options"])

# Dependencia para obtener una instancia de ExtraOptionUseCases
def get_extra_option_use_cases(db: Session = Depends(get_db)) -> ExtraOptionUseCases:
    repository = SQLAlchemyExtraOptionRepository(db)
    return ExtraOptionUseCases(repository)

@router.post("/", response_model=ExtraOptionResponseDto, status_code=status.HTTP_201_CREATED)
def create_extra_option(
    extra_option_dto: CreateExtraOptionDto,
    use_cases: ExtraOptionUseCases = Depends(get_extra_option_use_cases)
):
    try:
        return use_cases.create_extra_option(extra_option_dto)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al crear opción extra: {e}")

@router.get("/{extra_option_id}", response_model=ExtraOptionResponseDto)
def get_extra_option(
    extra_option_id: int,
    use_cases: ExtraOptionUseCases = Depends(get_extra_option_use_cases)
):
    try:
        return use_cases.get_extra_option_by_id(extra_option_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener opción extra: {e}")

@router.get("/", response_model=List[ExtraOptionResponseDto])
def get_all_extra_options(
    skip: int = 0,
    limit: int = 100,
    use_cases: ExtraOptionUseCases = Depends(get_extra_option_use_cases)
):
    try:
        return use_cases.get_all_extra_options(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al obtener opciones extra: {e}")

@router.put("/{extra_option_id}", response_model=ExtraOptionResponseDto)
def update_extra_option(
    extra_option_id: int,
    extra_option_dto: UpdateExtraOptionDto,
    use_cases: ExtraOptionUseCases = Depends(get_extra_option_use_cases)
):
    try:
        return use_cases.update_extra_option(extra_option_id, extra_option_dto)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except ConflictException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar opción extra: {e}")

@router.delete("/{extra_option_id}", response_model=ExtraOptionResponseDto)
def delete_extra_option(
    extra_option_id: int,
    use_cases: ExtraOptionUseCases = Depends(get_extra_option_use_cases)
):
    try:
        return use_cases.delete_extra_option(extra_option_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar opción extra: {e}")