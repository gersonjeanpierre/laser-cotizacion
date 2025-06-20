# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.api.routers import api_router

from src.infrastructure.database.database import Base, engine

# Al importar el módulo 'models', su __init__.py se ejecuta, lo que a su vez importa
# todos los modelos ORM necesarios, registrándolos con Base.metadata.
from src.infrastructure.persistence.models.store import StoreORM 
from src.infrastructure.persistence.models.type_client import TypeClientORM 
from src.infrastructure.persistence.models.product_type import ProductTypeORM
from src.infrastructure.persistence.models.extra_option import ExtraOptionORM
from src.infrastructure.persistence.models.product import ProductORM
# from src.infrastructure.persistence.models import StoreORM, ProductTypeORM, ...

# Crea las tablas en la base de datos si no existen
# ¡ADVERTENCIA! En entornos de producción, se recomienda usar herramientas de migración como Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My Commerce App API",
    description="API para la gestión de productos, clientes y cotizaciones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

origins = [
    "http://localhost:4200",  # Tu frontend de Angular
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to My Cotizacion App API"}