# src/infrastructure/persistence/repositories/store.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_ # No se usa en Store, pero es buena práctica tenerlo si se puede necesitar

from src.application.ports.store import StoreRepository
from src.domain.models.store import Store as DomainStore # Alias para evitar conflicto de nombres
from src.infrastructure.persistence.models.store import StoreORM
from datetime import datetime # Necesario para datetime.now() en el delete lógico

class SQLAlchemyStoreRepository(StoreRepository):
    """
    Implementación del puerto StoreRepository usando SQLAlchemy.
    Adapta las operaciones de dominio a operaciones de base de datos.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_model(self, orm_model: Optional[StoreORM]) -> Optional[DomainStore]: # <-- CORRECCIÓN AQUÍ
        """Convierte un modelo ORM a un modelo de dominio."""
        if orm_model is None: # Usar 'is None' es más idiomático que 'not orm_model' para None checks
            return None
        return DomainStore(
            id=orm_model.id,
            name=orm_model.name,
            code=orm_model.code,
            address=orm_model.address,
            phone_number=orm_model.phone_number,
            email=orm_model.email,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
            deleted_at=orm_model.deleted_at
        )

    def _to_orm_model(self, domain_model: DomainStore, orm_model: Optional[StoreORM] = None) -> StoreORM:
        """
        Convierte un modelo de dominio a un modelo ORM.
        Si se proporciona orm_model, actualiza la instancia existente.
        """
        if orm_model is None:
            orm_model = StoreORM()
        
        orm_model.name = domain_model.name
        orm_model.code = domain_model.code
        orm_model.address = domain_model.address
        orm_model.phone_number = domain_model.phone_number
        orm_model.email = domain_model.email
        # Timestamps como created_at y updated_at se gestionan a nivel de DB o por el ORM
        # No los asignamos directamente desde el dominio aquí, salvo deleted_at si se marcó.
        orm_model.deleted_at = domain_model.deleted_at # Persistir el deleted_at si se ha marcado.
        
        return orm_model

    def get_by_id(self, store_id: int) -> Optional[DomainStore]:
        orm_store = self.db.query(StoreORM).filter(StoreORM.id == store_id).first()
        return self._to_domain_model(orm_store)

    def get_by_code(self, code: str) -> Optional[DomainStore]:
        # Filtrar por código y asegurar que no esté lógicamente eliminado (si tu lógica lo requiere aquí)
        # Por ahora, solo por código. La eliminación lógica se verifica en el use case.
        orm_store = self.db.query(StoreORM).filter(StoreORM.code == code).first()
        return self._to_domain_model(orm_store)

    def get_by_name(self, name: str) -> Optional[DomainStore]:
        # Filtrar por nombre y asegurar que no esté lógicamente eliminado (si tu lógica lo requiere aquí)
        orm_store = self.db.query(StoreORM).filter(StoreORM.name == name).first()
        return self._to_domain_model(orm_store)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainStore]:
        # Aquí obtenemos todos, la lógica de filtrar activos se mueve al use case
        orm_stores = self.db.query(StoreORM).offset(skip).limit(limit).all()
        domain_stores = [self._to_domain_model(store) for store in orm_stores]
        return [store for store in domain_stores if store is not None]  # Filtrar None para cumplir con List[DomainStore]

    def save(self, store: DomainStore) -> DomainStore:
        if store.id is None:
            # Crear nueva tienda
            orm_store = self._to_orm_model(store)
            self.db.add(orm_store)
            self.db.commit()
            self.db.refresh(orm_store) # Actualiza el ORM con el ID generado por la DB
        else:
            # Actualizar tienda existente
            # Fetch the existing ORM object to update it
            orm_store = self.db.query(StoreORM).filter(StoreORM.id == store.id).first()
            if not orm_store:
                # Esto es un caso borde, ya que el use case debería haberlo manejado.
                # Podrías lanzar una excepción más específica aquí si es necesario.
                raise ValueError(f"Store with ID {store.id} not found for update in repository.")
            
            # Actualizar los campos del ORM desde el modelo de dominio
            # _to_orm_model ya tiene la lógica de actualización
            orm_store = self._to_orm_model(store, orm_store)

            self.db.commit()
            self.db.refresh(orm_store)

        domain_store = self._to_domain_model(orm_store)
        if domain_store is None:
            raise ValueError("Failed to save or retrieve the store from the database.")
        return domain_store  # Siempre retornamos el modelo de dominio actualizado

    def delete(self, store_id: int) -> Optional[DomainStore]:
        """
        Elimina lógicamente una tienda directamente desde el repositorio.
        Se puede llamar desde el UseCase.
        """
        orm_store = self.db.query(StoreORM).filter(StoreORM.id == store_id).first()
        if orm_store:
            orm_store.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_store)
            return self._to_domain_model(orm_store)
        return None # Retorna None si no se encontró la tienda con ese ID