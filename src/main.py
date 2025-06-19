# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa la Base del ORM para que SQLAlchemy pueda crear las tablas
from src.infrastructure.database.database import Base, engine

# --- Importa el módulo de modelos ORM para que Base.metadata.create_all() los detecte ---
# Al importar el módulo 'models', su __init__.py se ejecuta, lo que a su vez importa
# todos los modelos ORM necesarios, registrándolos con Base.metadata.
from src.infrastructure.persistence.models.store import StoreORM 
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

# --- Aquí se incluirán los routers de tus módulos de API ---
# Incluye el router para Store
from src.infrastructure.api.routers import store as store_router
app.include_router(store_router.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to My Commerce App API"}