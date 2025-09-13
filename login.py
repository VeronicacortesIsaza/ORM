from database.config import SessionLocal
from entities.usuario import Usuario

def login():
    session = SessionLocal()
    while True:
        user = input("Usuario: ")
        password = input("Contraseña: ")
        usuario = session.query(Usuario).filter_by(username=user, password=password).first()
        if usuario:
            print(f"Bienvenido {user}")
            return True
        else:
            print("Usuario o contraseña incorrectos. Intente de nuevo.")