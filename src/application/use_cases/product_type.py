# src/application/use_cases/product_type.py
from typing import List, Optional
from src.domain.models.product_type import ProductType
from src.application.ports.product_type import ProductTypeRepository
from src.application.dtos.product_type import CreateProductTypeDto, UpdateProductTypeDto, ProductTypeResponseDto
from src.application.exceptions import NotFoundException, ConflictException
from datetime import datetime

class ProductTypeUseCases:
    """
    Casos de uso para la gestión de Tipos de Producto.
    """
    def __init__(self, repository: ProductTypeRepository):
        self.repository = repository

    def create_product_type(self, product_type_dto: CreateProductTypeDto) -> ProductTypeResponseDto:
        """Crea un nuevo tipo de producto."""
        if self.repository.get_by_name(product_type_dto.name):
            raise ConflictException(f"Ya existe un tipo de producto con el nombre '{product_type_dto.name}'.")

        new_product_type = ProductType(
            name=product_type_dto.name,
            description=product_type_dto.description,
            created_at=datetime.now()
        )
        
        created_product_type = self.repository.save(new_product_type)
        
        return ProductTypeResponseDto.model_validate(created_product_type)

    def get_product_type_by_id(self, product_type_id: int) -> ProductTypeResponseDto:
        """Recupera un tipo de producto por su ID."""
        product_type = self.repository.get_by_id(product_type_id)
        if not product_type or not product_type.is_active():
            raise NotFoundException(f"Tipo de producto con ID {product_type_id} no encontrado o eliminado.")
        return ProductTypeResponseDto.model_validate(product_type)

    def get_all_product_types(self, skip: int = 0, limit: int = 100) -> List[ProductTypeResponseDto]:
        """Recupera todos los tipos de producto activos paginados."""
        product_types = self.repository.get_all(skip, limit)
        active_product_types = [pt for pt in product_types if pt.is_active()]
        return [ProductTypeResponseDto.model_validate(product_type) for product_type in active_product_types]

    def update_product_type(self, product_type_id: int, product_type_dto: UpdateProductTypeDto) -> ProductTypeResponseDto:
        """Actualiza un tipo de producto existente."""
        existing_product_type = self.repository.get_by_id(product_type_id)
        if not existing_product_type or not existing_product_type.is_active():
            raise NotFoundException(f"Tipo de producto con ID {product_type_id} no encontrado o eliminado.")

        if product_type_dto.name and product_type_dto.name != existing_product_type.name:
            if self.repository.get_by_name(product_type_dto.name):
                raise ConflictException(f"Ya existe otro tipo de producto con el nombre '{product_type_dto.name}'.")

        update_data = product_type_dto.model_dump(exclude_unset=True)
        existing_product_type.update(**update_data)

        updated_product_type = self.repository.save(existing_product_type)
        return ProductTypeResponseDto.model_validate(updated_product_type)

    def delete_product_type(self, product_type_id: int) -> ProductTypeResponseDto:
        """Elimina lógicamente un tipo de producto."""
        product_type_to_delete = self.repository.get_by_id(product_type_id)
        if not product_type_to_delete or not product_type_to_delete.is_active():
            raise NotFoundException(f"Tipo de producto con ID {product_type_id} no encontrado o ya eliminado.")
        
        product_type_to_delete.mark_as_deleted()
        
        deleted_product_type = self.repository.save(product_type_to_delete)
        return ProductTypeResponseDto.model_validate(deleted_product_type)