import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener la URL de la base de datos de las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env")

# Crear el motor de la base de datos
# echo=True mostrará las consultas SQL en la consola (útil para depuración)
engine = create_engine(DATABASE_URL, echo=True)

# DeclarativeBase es la base para tus modelos ORM en SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

# Configurar la sesión de la base de datos
# autocommit=False: Control manual de las transacciones (commit/rollback)
# autoflush=False: No vaciar automáticamente la sesión al acceder a otros objetos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()