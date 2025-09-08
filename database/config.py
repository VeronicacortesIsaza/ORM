"""
Configuración de la base de datos
=================================

Configuraciones centralizadas para la conexión a la base de datos.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()  

DATABASE_URL = os.getenv("DATABASE_URL")

DB_ECHO: bool = os.getenv("DB_ECHO", "True").lower() == "true"
DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
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
    return SessionLocal()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
