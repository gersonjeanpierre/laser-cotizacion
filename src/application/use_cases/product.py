# src/application/use_cases/product.py
from typing import List, Optional
from src.domain.models.product import Product
from src.domain.models.product_type import ProductType
from src.domain.models.extra_option import ExtraOption
from src.application.ports.product import ProductRepository
from src.application.ports.product_type import ProductTypeRepository # Necesario para buscar ProductTypes
from src.application.ports.extra_option import ExtraOptionRepository # Necesario para buscar ExtraOptions
from src.application.dtos.product import CreateProductDto, UpdateProductDto, ProductResponseDto
from src.application.exceptions import NotFoundException, ConflictException
from datetime import datetime

class ProductUseCases:
    """
    Casos de uso para la gestión de Productos.
    """
    def __init__(
        self,
        product_repository: ProductRepository,
        product_type_repository: ProductTypeRepository,
        extra_option_repository: ExtraOptionRepository
    ):
        self.product_repository = product_repository
        self.product_type_repository = product_type_repository
        self.extra_option_repository = extra_option_repository

    def create_product(self, product_dto: CreateProductDto) -> ProductResponseDto:
        """Crea un nuevo producto y asocia sus tipos y opciones extra."""
        if self.product_repository.get_by_sku(product_dto.sku):
            raise ConflictException(f"Ya existe un producto con el SKU '{product_dto.sku}'.")
        if self.product_repository.get_by_name(product_dto.name):
            raise ConflictException(f"Ya existe un producto con el nombre '{product_dto.name}'.")

        # 1. Crear el producto base
        new_product = Product(
            sku=product_dto.sku,
            name=product_dto.name,
            description=product_dto.description,
            unity_measure=product_dto.unity_measure,
            price=product_dto.price,
            image_url=product_dto.image_url,
            created_at=datetime.now()
        )
        # El repositorio guarda el producto base y le asigna un ID si es nuevo
        created_product = self.product_repository.save(new_product)

        # 2. Asociar Tipos de Producto
        if product_dto.product_type_ids:
            product_types_to_add: List[ProductType] = []
            for pt_id in product_dto.product_type_ids:
                product_type = self.product_type_repository.get_by_id(pt_id)
                if not product_type or not product_type.is_active():
                    # Si un tipo de producto no existe o está inactivo, lanzamos un error
                    raise NotFoundException(f"Tipo de producto con ID {pt_id} no encontrado o inactivo.")
                product_types_to_add.append(product_type)
            # Usamos set_product_types para asegurar que solo los IDs proporcionados estén asociados
            created_product = self.product_repository.set_product_types(created_product, product_types_to_add)

        # 3. Asociar Opciones Extra
        if product_dto.extra_option_ids:
            extra_options_to_add: List[ExtraOption] = []
            for eo_id in product_dto.extra_option_ids:
                extra_option = self.extra_option_repository.get_by_id(eo_id)
                if not extra_option or not extra_option.is_active():
                    # Si una opción extra no existe o está inactiva, lanzamos un error
                    raise NotFoundException(f"Opción extra con ID {eo_id} no encontrada o inactiva.")
                extra_options_to_add.append(extra_option)
            # Usamos set_extra_options para asegurar que solo los IDs proporcionados estén asociados
            created_product = self.product_repository.set_extra_options(created_product, extra_options_to_add)

        return ProductResponseDto.model_validate(created_product)

    def get_product_by_id(self, product_id: int) -> ProductResponseDto:
        """Recupera un producto por su ID, incluyendo sus relaciones."""
        product = self.product_repository.get_by_id(product_id)
        if not product or not product.is_active():
            raise NotFoundException(f"Producto con ID {product_id} no encontrado o eliminado.")
        return ProductResponseDto.model_validate(product)

    def get_all_products(self, skip: int = 0, limit: int = 100) -> List[ProductResponseDto]:
        """Recupera todos los productos activos paginados, incluyendo sus relaciones."""
        products = self.product_repository.get_all(skip, limit)
        active_products = [p for p in products if p.is_active()]
        return [ProductResponseDto.model_validate(product) for product in active_products]

    def update_product(self, product_id: int, product_dto: UpdateProductDto) -> ProductResponseDto:
        """Actualiza un producto existente y sus relaciones."""
        existing_product = self.product_repository.get_by_id(product_id)
        if not existing_product or not existing_product.is_active():
            raise NotFoundException(f"Producto con ID {product_id} no encontrado o eliminado.")

        # Verificar conflictos de SKU/nombre si se están actualizando
        if product_dto.sku and product_dto.sku != existing_product.sku:
            if self.product_repository.get_by_sku(product_dto.sku):
                raise ConflictException(f"Ya existe otro producto con el SKU '{product_dto.sku}'.")
        if product_dto.name and product_dto.name != existing_product.name:
            if self.product_repository.get_by_name(product_dto.name):
                raise ConflictException(f"Ya existe otro producto con el nombre '{product_dto.name}'.")

        # 1. Actualizar atributos base del producto
        update_data = product_dto.model_dump(exclude_unset=True, exclude={'product_type_ids', 'extra_option_ids'})
        existing_product.update(**update_data) # Usa el método 'update' definido en el dominio
        
        # Guardar cambios base
        updated_product = self.product_repository.save(existing_product)

        # 2. Actualizar Tipos de Producto si se proporcionaron IDs
        if product_dto.product_type_ids is not None: # Usar 'is not None' para diferenciar de lista vacía
            product_types_to_set: List[ProductType] = []
            for pt_id in product_dto.product_type_ids:
                product_type = self.product_type_repository.get_by_id(pt_id)
                if not product_type or not product_type.is_active():
                    raise NotFoundException(f"Tipo de producto con ID {pt_id} no encontrado o inactivo.")
                product_types_to_set.append(product_type)
            updated_product = self.product_repository.set_product_types(updated_product, product_types_to_set)

        # 3. Actualizar Opciones Extra si se proporcionaron IDs
        if product_dto.extra_option_ids is not None: # Usar 'is not None' para diferenciar de lista vacía
            extra_options_to_set: List[ExtraOption] = []
            for eo_id in product_dto.extra_option_ids:
                extra_option = self.extra_option_repository.get_by_id(eo_id)
                if not extra_option or not extra_option.is_active():
                    raise NotFoundException(f"Opción extra con ID {eo_id} no encontrada o inactiva.")
                extra_options_to_set.append(extra_option)
            updated_product = self.product_repository.set_extra_options(updated_product, extra_options_to_set)

        return ProductResponseDto.model_validate(updated_product)

    def delete_product(self, product_id: int) -> ProductResponseDto:
        """Elimina lógicamente un producto."""
        product_to_delete = self.product_repository.get_by_id(product_id)
        if not product_to_delete or not product_to_delete.is_active():
            raise NotFoundException(f"Producto con ID {product_id} no encontrado o ya eliminado.")
        
        product_to_delete.mark_as_deleted()
        
        deleted_product = self.product_repository.save(product_to_delete)
        return ProductResponseDto.model_validate(deleted_product)