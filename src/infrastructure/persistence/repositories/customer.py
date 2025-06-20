# src/infrastructure/persistence/repositories/customer.py
from typing import List, Optional, cast, Literal
from sqlalchemy.orm import Session, selectinload # selectinload para cargar relaciones
from sqlalchemy import or_ # Para consultas OR
from datetime import datetime

from src.application.ports.customer import CustomerRepository
from src.domain.models.customer import Customer as DomainCustomer # Alias para evitar conflicto de nombres
from src.domain.models.type_client import TypeClient as DomainTypeClient # Para mapear el tipo de cliente en el dominio

from src.infrastructure.persistence.models.customer import CustomerORM
from src.infrastructure.persistence.models.type_client import TypeClientORM # Necesario para la relación

class SQLAlchemyCustomerRepository(CustomerRepository):
    """
    Implementación del puerto CustomerRepository usando SQLAlchemy.
    """
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_model(self, orm_model: Optional[CustomerORM]) -> Optional[DomainCustomer]:
        """Convierte un modelo ORM a un modelo de dominio, incluyendo su TypeClient."""
        if orm_model is None:
            return None
        
        domain_type_client = None
        if orm_model.type_client:
            domain_type_client = DomainTypeClient(
                id=orm_model.type_client.id,
                code=orm_model.type_client.code,
                name=orm_model.type_client.name,
                margin=float(orm_model.type_client.margin),
                created_at=orm_model.type_client.created_at,
                updated_at=orm_model.type_client.updated_at,
                deleted_at=orm_model.type_client.deleted_at
            )

        return DomainCustomer(
            id=orm_model.id,
            entity_type=cast(Literal['N', 'J'], orm_model.entity_type),
            ruc=orm_model.ruc,
            dni=orm_model.dni,
            name=orm_model.name,
            last_name=orm_model.last_name,
            business_name=orm_model.business_name,
            phone_number=orm_model.phone_number,
            email=orm_model.email,
            created_at=orm_model.created_at,
            updated_at=orm_model.updated_at,
            deleted_at=orm_model.deleted_at,
            type_client_id=orm_model.type_client_id, # Asigna el ID del tipo de cliente
            type_client=domain_type_client # Asigna el modelo de dominio TypeClient
        )

    def _to_orm_model(self, domain_model: DomainCustomer, orm_model: Optional[CustomerORM] = None) -> CustomerORM:
        """
        Convierte un modelo de dominio a un modelo ORM.
        Nota: La relación 'type_client' se maneja asignando type_client_id o la instancia ORM si ya está cargada.
        """
        if orm_model is None:
            orm_model = CustomerORM()
        
        orm_model.entity_type = domain_model.entity_type
        orm_model.ruc = domain_model.ruc
        orm_model.dni = domain_model.dni
        orm_model.name = domain_model.name
        orm_model.last_name = domain_model.last_name
        orm_model.business_name = domain_model.business_name
        orm_model.phone_number = domain_model.phone_number
        orm_model.email = domain_model.email
        orm_model.deleted_at = domain_model.deleted_at

        # Manejar la relación TypeClient
        if domain_model.type_client and domain_model.type_client.id is not None:
            orm_model.type_client_id = domain_model.type_client.id
            # Si necesitas que SQLAlchemy reconozca la relación como objeto, puedes hacer esto:
            # orm_model.type_client = self.db.query(TypeClientORM).get(domain_model.type_client.id)
            # Pero para el save inicial, solo type_client_id es suficiente si ya está validado.
        
        return orm_model

    def get_by_id(self, customer_id: int) -> Optional[DomainCustomer]:
        # Usar selectinload para cargar TypeClient en la misma consulta
        orm_customer = self.db.query(CustomerORM).options(
            selectinload(CustomerORM.type_client)
        ).filter(CustomerORM.id == customer_id).first()
        return self._to_domain_model(orm_customer)

    def get_by_ruc(self, ruc: str) -> Optional[DomainCustomer]:
        orm_customer = self.db.query(CustomerORM).options(
            selectinload(CustomerORM.type_client)
        ).filter(CustomerORM.ruc == ruc).first()
        return self._to_domain_model(orm_customer)

    def get_by_dni(self, dni: str) -> Optional[DomainCustomer]:
        orm_customer = self.db.query(CustomerORM).options(
            selectinload(CustomerORM.type_client)
        ).filter(CustomerORM.dni == dni).first()
        return self._to_domain_model(orm_customer)
    
    def get_by_email(self, email: str) -> Optional[DomainCustomer]:
        orm_customer = self.db.query(CustomerORM).options(
            selectinload(CustomerORM.type_client)
        ).filter(CustomerORM.email == email).first()
        return self._to_domain_model(orm_customer)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[DomainCustomer]:
        orm_customers = self.db.query(CustomerORM).options(
            selectinload(CustomerORM.type_client)
        ).offset(skip).limit(limit).all()
        domain_customers = [self._to_domain_model(c) for c in orm_customers]
        return [dc for dc in domain_customers if dc is not None]

    def save(self, customer: DomainCustomer) -> DomainCustomer:
        if customer.id is None:
            # Crear nuevo cliente
            orm_customer = self._to_orm_model(customer)
            self.db.add(orm_customer)
            self.db.commit()
            self.db.refresh(orm_customer) # Obtener el ID generado y relaciones cargadas
        else:
            # Actualizar cliente existente
            orm_customer = self.db.query(CustomerORM).filter(CustomerORM.id == customer.id).first()
            if not orm_customer:
                raise ValueError(f"Customer with ID {customer.id} not found for update in repository.")
            
            # Actualizar la relación type_client_id si cambió en el modelo de dominio
            if customer.type_client and customer.type_client.id is not None and orm_customer.type_client_id != customer.type_client.id:
                orm_customer.type_client_id = customer.type_client.id
            
            # Actualizar los campos escalares
            orm_customer = self._to_orm_model(customer, orm_customer)
            self.db.commit()
            self.db.refresh(orm_customer) # Refrescar para asegurar que los datos estén actualizados, incluyendo la relación cargada

        # Retorna el modelo de dominio actualizado con las relaciones cargadas
        domain_customer = self._to_domain_model(orm_customer)
        if domain_customer is None:
            raise ValueError("Failed to convert ORM model to domain model after save.")
        return domain_customer

    def delete(self, customer_id: int) -> Optional[DomainCustomer]:
        orm_customer = self.db.query(CustomerORM).filter(CustomerORM.id == customer_id).first()
        if orm_customer:
            orm_customer.deleted_at = datetime.now()
            self.db.commit()
            self.db.refresh(orm_customer)
            # Re-cargar con relaciones para el DTO de respuesta
            orm_customer_with_relations = self.db.query(CustomerORM).options(
                selectinload(CustomerORM.type_client)
            ).filter(CustomerORM.id == orm_customer.id).first()
            return self._to_domain_model(orm_customer_with_relations)
        return None