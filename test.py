from sqlalchemy import create_engine, inspect
from database.config import create_tables

# Crear tablas
create_tables()
print("[OK] Tablas creadas exitosamente")

# Verificar tablas existentes
engine = create_engine("postgresql://neondb_owner:npg_HdMWb1wIsDO7@ep-mute-shadow-adr33azf-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
inspector = inspect(engine)
tablas = inspector.get_table_names()
print("Tablas realmente en la BD:", tablas)
