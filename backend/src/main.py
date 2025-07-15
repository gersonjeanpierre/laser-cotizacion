# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.api.routers import api_router

# # Crea las tablas en la base de datos si no existen
# # ¡ADVERTENCIA! En entornos de producción, se recomienda usar herramientas de migración como Alembic.
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cotizaciones API",
    description="API para la gestión de productos, clientes y cotizaciones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost:8080",
    "http://localhost:9000",        
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