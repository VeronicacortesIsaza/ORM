from entities.usuario import Usuario
from database.connection import get_session

def insertar_usuario():
    session = get_session()
    try:
        nuevo_usuario = Usuario(
            id_usuario=123,
            nombre="Juan",
            apellidos="Pérez",
            telefono="555-1234",
            nombre_usuario="juanp",
            clave="clave123",
            id_usuario_crea=1
        )
        session.add(nuevo_usuario)
        session.commit()
        session.refresh(nuevo_usuario)
        print(f"Usuario insertado: {nuevo_usuario}")
    except Exception as e:
        session.rollback()
        print(f"❌ Error al insertar usuario: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    insertar_usuario()
