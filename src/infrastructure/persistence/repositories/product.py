# src/infrastructure/persistence/repositories/product.py
from typing import List, Optional
from sqlalchemy.orm import Session, selectinload # selectinload para cargar relaciones
from datetime import datetime

from src.application.exceptions import NotFoundException
from src.application.ports.product import ProductRepository
from src.domain.models.product import Product as DomainProduct # Alias
from src.domain.models.product_type import ProductType as DomainProductType
from src.domain.models.extra_option import ExtraOption as DomainExtraOption

from src.infrastructure.persistence.models.product import ProductORM
from src.infrastructure.persistence.models.product_type import ProductTypeORM
from src.infrastructure.persistence.models.extra_option import ExtraOptionORM


class SQLAlchemyProductRepository(ProductRepository):
    """
    Implementación del puerto ProductRepository usando SQLAlchemy,
    manejando las relaciones Many-to-Many.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_model(self, orm_model: Optional[ProductORM]) -> Optional[DomainProduct]:
        """Convierte un modelo ORM a un modelo de dominio, incluyendo sus relaciones."""
        if orm_model is None:
            return None
        
        # Mapea los tipos de producto asociados
        domain_product_types = [
            DomainProductType(
                id=pt_orm.id,
                name=pt_orm.name,
                description=pt_orm.description,
                created_at=pt_orm.created_at,
                updated_at=pt_orm.updated_at,
                deleted_at=pt_orm.deleted_at
            ) for pt_orm in orm_model.product_types
        ]

        # Mapea las opciones extra asociadas
        domain_extra_options = [
            DomainExtraOption(
                id=eo_orm.id,
                name=eo_orm.name,
                price=float(eo_orm.price), # Aseguramos float
                description=eo_orm.description,
                created_at=eo_orm.created_at,
                updated_at=eo_orm.updated_at,
                deleted_at=eo_orm.deleted_at
            ) for eo_orm in orm_model.extra_options
        ]

        return DomainProduct(
            id=orm_model.id,
            sku=orm_model.sku,
            name=orm_model.name,
            description=orm_model.description,
            unity_measure=orm_model.unity_measure,
            price=float(orm_model.price), # Aseguramos float
            image_url=orm_model.image_url,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
            deleted_at=orm_model.deleted_at,
            product_types=domain_product_types, # Asigna los modelos de dominio relacionados
            extra_options=domain_extra_options
        )

    def _to_orm_model(self, domain_model: DomainProduct, orm_model: Optional[ProductORM] = None) -> ProductORM:
        """
        Convierte un modelo de dominio a un modelo ORM.
        Nota: Las relaciones (product_types, extra_options) no se manejan aquí.
        Se manejan en métodos de asociación específicos (`set_product_types`, `set_extra_options`).
        """
        if orm_model is None:
            orm_model = ProductORM()
        
        orm_model.sku = domain_model.sku
        orm_model.name = domain_model.name
        orm_model.description = domain_model.description
        orm_model.unity_measure = domain_model.unity_measure
        orm_model.price = domain_model.price
        orm_model.image_url = domain_model.image_url
        orm_model.deleted_at = domain_model.deleted_at
        
        return orm_model

    def get_by_id(self, product_id: int) -> Optional[DomainProduct]:
        # Usar selectinload para cargar las relaciones en la misma consulta y evitar N+1
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.product_types),
            selectinload(ProductORM.extra_options)
        ).filter(ProductORM.id == product_id).first()
        return self._to_domain_model(orm_product)

    def get_by_sku(self, sku: str) -> Optional[DomainProduct]:
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.product_types),
            selectinload(ProductORM.extra_options)
        ).filter(ProductORM.sku == sku).first()
        return self._to_domain_model(orm_product)

    def get_by_name(self, name: str) -> Optional[DomainProduct]:
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.product_types),
            selectinload(ProductORM.extra_options)
        ).filter(ProductORM.name == name).first()
        return self._to_domain_model(orm_product)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainProduct]:
        orm_products = self.db.query(ProductORM).options(
            selectinload(ProductORM.product_types),
            selectinload(ProductORM.extra_options)
        ).offset(skip).limit(limit).all()
        domain_products = [self._to_domain_model(p) for p in orm_products]
        return [dp for dp in domain_products if dp is not None]  # Filtrar None si hay productos eliminados

    def save(self, product: DomainProduct) -> DomainProduct:
        if product.id is None:
            # Crear nuevo producto
            orm_product = self._to_orm_model(product)
            self.db.add(orm_product)
            self.db.commit()
            self.db.refresh(orm_product) # Obtener el ID generado por la DB
        else:
            # Actualizar producto existente
            orm_product = self.db.query(ProductORM).filter(ProductORM.id == product.id).first()
            if not orm_product:
                raise ValueError(f"Product with ID {product.id} not found for update in repository.")
            
            orm_product = self._to_orm_model(product, orm_product)
            self.db.commit()
            self.db.refresh(orm_product) # Refrescar para asegurar que cualquier dato actualizado esté cargado

        # Después de guardar el producto base, cargamos sus relaciones (si el producto tiene ID)
        # Esto es importante para que el _to_domain_model pueda mapear las relaciones existentes.
        # Si las relaciones se acaban de asociar, refresh() debería cargarlas.
        updated_product_with_relations = self.db.query(ProductORM).options(
            selectinload(ProductORM.product_types),
            selectinload(ProductORM.extra_options)
        ).filter(ProductORM.id == orm_product.id).first()

        domain_product = self._to_domain_model(updated_product_with_relations)
        if domain_product is None:
            raise ValueError(f"Failed to convert ORM model to domain model for product ID {orm_product.id}.")
        return domain_product


    def delete(self, product_id: int) -> Optional[DomainProduct]:
        orm_product = self.db.query(ProductORM).filter(ProductORM.id == product_id).first()
        if orm_product:
            orm_product.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_product)
            # Re-cargar con relaciones para el DTO de respuesta
            orm_product_with_relations = self.db.query(ProductORM).options(
                selectinload(ProductORM.product_types),
                selectinload(ProductORM.extra_options)
            ).filter(ProductORM.id == orm_product.id).first()
            return self._to_domain_model(orm_product_with_relations)
        return None

    # --- Métodos para manejar las relaciones Many-to-Many ---

    def set_product_types(self, product: DomainProduct, product_types: List[DomainProductType]) -> DomainProduct:
        """Establece (sobrescribe) los tipos de producto asociados a un producto."""
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.product_types) # Carga la relación actual
        ).filter(ProductORM.id == product.id).first()

        if not orm_product:
            raise NotFoundException(f"Producto con ID {product.id} no encontrado para establecer tipos.")

        # Obtiene las instancias ORM de los tipos de producto a asociar
        product_type_orms = self.db.query(ProductTypeORM).filter(
            ProductTypeORM.id.in_([pt.id for pt in product_types])
        ).all()

        # Establece la relación: sobrescribe la lista existente
        orm_product.product_types = product_type_orms
        self.db.commit()
        self.db.refresh(orm_product) # Refresca para cargar las nuevas relaciones
        domain_product = self._to_domain_model(orm_product)
        if domain_product is None:
            raise ValueError(f"Failed to convert ORM model to domain model for product ID {orm_product.id}.")   
        return domain_product


    def add_product_types(self, product: DomainProduct, product_types: List[DomainProductType]) -> DomainProduct:
        """Añade tipos de producto a un producto existente."""
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.product_types)
        ).filter(ProductORM.id == product.id).first()

        if not orm_product:
            raise NotFoundException(f"Producto con ID {product.id} no encontrado para añadir tipos.")

        # Obtiene los IDs de los tipos de producto ya asociados
        current_type_ids = {pt.id for pt in orm_product.product_types}
        
        # Filtra los nuevos tipos para añadir solo los que no están ya asociados
        new_product_type_ids = [pt.id for pt in product_types if pt.id not in current_type_ids]

        if new_product_type_ids:
            new_product_type_orms = self.db.query(ProductTypeORM).filter(
                ProductTypeORM.id.in_(new_product_type_ids)
            ).all()
            orm_product.product_types.extend(new_product_type_orms)
            self.db.commit()
            self.db.refresh(orm_product)
        
        domain_product = self._to_domain_model(orm_product)
        if domain_product is None:
            raise ValueError(f"Failed to convert ORM model to domain model for product ID {orm_product.id}.")
        return domain_product

    def remove_product_types(self, product: DomainProduct, product_type_ids: List[int]) -> DomainProduct:
        """Remueve tipos de producto de un producto existente."""
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.product_types)
        ).filter(ProductORM.id == product.id).first()

        if not orm_product:
            raise NotFoundException(f"Producto con ID {product.id} no encontrado para remover tipos.")

        # Filtra los tipos de producto a remover que realmente están asociados
        product_types_to_remove = [
            pt_orm for pt_orm in orm_product.product_types
            if pt_orm.id in product_type_ids
        ]

        for pt_orm in product_types_to_remove:
            orm_product.product_types.remove(pt_orm)
        
        if product_types_to_remove: # Solo commitea si hay cambios
            self.db.commit()
            self.db.refresh(orm_product)
        
        domain_product = self._to_domain_model(orm_product)
        if domain_product is None:
            raise ValueError(f"Failed to convert ORM model to domain model for product ID {orm_product.id}.")
        return domain_product


    def set_extra_options(self, product: DomainProduct, extra_options: List[DomainExtraOption]) -> DomainProduct:
        """Establece (sobrescribe) las opciones extra asociadas a un producto."""
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.extra_options)
        ).filter(ProductORM.id == product.id).first()

        if not orm_product:
            raise NotFoundException(f"Producto con ID {product.id} no encontrado para establecer opciones extra.")

        extra_option_orms = self.db.query(ExtraOptionORM).filter(
            ExtraOptionORM.id.in_([eo.id for eo in extra_options])
        ).all()

        orm_product.extra_options = extra_option_orms
        self.db.commit()
        self.db.refresh(orm_product)

        domain_product = self._to_domain_model(orm_product)
        if domain_product is None:
            raise ValueError(f"Failed to convert ORM model to domain model for product ID {orm_product.id}.")
        return domain_product

    def add_extra_options(self, product: DomainProduct, extra_options: List[DomainExtraOption]) -> DomainProduct:
        """Añade opciones extra a un producto existente."""
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.extra_options)
        ).filter(ProductORM.id == product.id).first()

        if not orm_product:
            raise NotFoundException(f"Producto con ID {product.id} no encontrado para añadir opciones extra.")

        current_option_ids = {eo.id for eo in orm_product.extra_options}
        
        new_extra_option_ids = [eo.id for eo in extra_options if eo.id not in current_option_ids]

        if new_extra_option_ids:
            new_extra_option_orms = self.db.query(ExtraOptionORM).filter(
                ExtraOptionORM.id.in_(new_extra_option_ids)
            ).all()
            orm_product.extra_options.extend(new_extra_option_orms)
            self.db.commit()
            self.db.refresh(orm_product)
        
        domain_product = self._to_domain_model(orm_product)
        if domain_product is None:
            raise ValueError(f"Failed to convert ORM model to domain model for product ID {orm_product.id}.")
        return domain_product

    def remove_extra_options(self, product: DomainProduct, extra_option_ids: List[int]) -> DomainProduct:
        """Remueve opciones extra de un producto existente."""
        orm_product = self.db.query(ProductORM).options(
            selectinload(ProductORM.extra_options)
        ).filter(ProductORM.id == product.id).first()

        if not orm_product:
            raise NotFoundException(f"Producto con ID {product.id} no encontrado para remover opciones extra.")

        extra_options_to_remove = [
            eo_orm for eo_orm in orm_product.extra_options
            if eo_orm.id in extra_option_ids
        ]

        for eo_orm in extra_options_to_remove:
            orm_product.extra_options.remove(eo_orm)
        
        if extra_options_to_remove:
            self.db.commit()
            self.db.refresh(orm_product)
        
        domain_product = self._to_domain_model(orm_product)
        if domain_product is None:
            raise ValueError(f"Failed to convert ORM model to domain model for product ID {orm_product.id}.")
        return domain_product