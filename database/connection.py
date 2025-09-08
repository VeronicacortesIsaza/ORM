"""from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ No se encontró DATABASE_URL en el archivo .env")
print("✅ DATABASE_URL cargada:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT @@VERSION"))
        print("✅ Conectado a SQL Server")
        for row in result:
            print(row[0])
except Exception as e:
    print("❌ Error al conectar:", e)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()"""

"""
Configuración y conexión a la base de datos
===========================================

Este módulo maneja la conexión a la base de datos usando SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from typing import Generator
import logging

from database.config import DATABASE_URL, DB_ECHO, DB_POOL_SIZE, DB_MAX_OVERFLOW

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_engine():
    """Retorna el motor de base de datos"""
    return engine

def get_session() -> Session:
    """
    Crea y retorna una nueva sesión de base de datos
    
    Returns:
        Session: Sesión de SQLAlchemy
    """
    return SessionLocal()

@contextmanager
def get_session_context() -> Generator[Session, None, None]:
    """
    Context manager para manejar sesiones de base de datos
    
    Yields:
        Session: Sesión de SQLAlchemy
        
    Example:
        with get_session_context() as session:
            user = session.query(Usuario).first()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f"Error en la sesión: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def create_tables():
    """
    Crea todas las tablas definidas en los modelos
    
    Esta función debe ser llamada después de importar todos los modelos
    para que SQLAlchemy pueda detectarlos.
    """
    try:
        logger.info("Creando tablas en la base de datos...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas creadas exitosamente")
    except Exception as e:
        logger.error(f"Error al crear tablas: {e}")
        raise

def drop_tables():
    """
    Elimina todas las tablas de la base de datos
    
    ⚠️ CUIDADO: Esta función elimina TODOS los datos
    """
    try:
        logger.warning("Eliminando todas las tablas...")
        Base.metadata.drop_all(bind=engine)
        logger.info("Tablas eliminadas exitosamente")
    except Exception as e:
        logger.error(f"Error al eliminar tablas: {e}")
        raise

def check_connection():
    """
    Verifica la conexión a la base de datos
    
    Returns:
        bool: True si la conexión es exitosa, False en caso contrario
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        logger.info("Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        logger.error(f"Error de conexión a la base de datos: {e}")
        return False

