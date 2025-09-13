from login import login
from database.config import SessionLocal
from entities.habitacion import Habitacion
from entities.reserva import Reserva

def menu():
    if not login():
        print("❌ Usuario o contraseña incorrectos.")
        return
    
    session = SessionLocal()

    while True:
        print("\n===== SISTEMA DE RESERVAS DE HOTEL =====")
        print("1. Reservar habitación")
        print("2. Cancelar reserva")
        print("3. Mostrar reservas")
        print("4. Salir")
        
        while True:
            opcion = input("Elige una opción (1-4): ")
            if opcion.isdigit():  
                opcion = int(opcion)  
                if 1 <= opcion <= 4:
                    print("Opción válida:", opcion) 
                    break  
                else:
                    print("El número debe estar entre 1 y 4.")
            else:
                print("Debes ingresar un número válido.")

        if opcion == 1:
            reservar_habitacion(session)
        elif opcion == 2:
            cancelar_reserva(session)
        elif opcion == 3:
            mostrar_reservas(session)
        elif opcion == 4:
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")

    session.close()

def reservar_habitacion(session):
    cliente = input("Nombre del cliente: ")
    telefono = input("Teléfono del cliente: ")
    correo = input("Correo del cliente: ")

    while True:
        try:
            noches = int(input("Número de noches: "))
            if noches > 0:
                break
            else:
                print("Debe ser mayor a cero.")
        except ValueError:
            print("Ingresa un número válido.")

    print("Tipos de habitación:")
    print("1. Estándar ($200000/noche)")
    print("2. Suite ($300000/noche)")
    print("3. Premium ($450000/noche)")

    tipo = input("Seleccione tipo: ")
    precios = {"1": ("Estandar", 200000),
               "2": ("Suite", 300000),
               "3": ("Premium", 450000)}

    if tipo not in precios:
        print("⚠️ Opción inválida.")
        return

    tipo_h, precio = precios[tipo]
    habitacion = session.query(Habitacion).filter_by(tipo=tipo_h, disponible=True).first()

    if habitacion:
        reserva = Reserva(cliente=cliente, documento=documento,
                          noches=noches, habitacion=habitacion)
        habitacion.disponible = False
        session.add(reserva)
        session.commit()
        print(f"✅ Reserva realizada para {cliente}. Habitación: {habitacion.tipo}")
    else:
        print("❌ No hay habitaciones disponibles de ese tipo.")

def cancelar_reserva(session):
    documento = input("Ingrese documento del cliente: ")
    reserva = session.query(Reserva).filter_by(documento=documento).first()

    if reserva:
        reserva.habitacion.disponible = True
        session.delete(reserva)
        session.commit()
        print("Reserva cancelada.")
    else:
        print("No se encontró la reserva.")

def mostrar_reservas(session):
    reservas = session.query(Reserva).all()

    if not reservas:
        print("No hay reservas registradas.")
        return

    print("\n===== RESERVAS REGISTRADAS =====")
    for r in reservas:
        print(f"Cliente: {r.cliente} | 🛏️ Habitación: {r.habitacion.tipo} | ⏳ Noches: {r.noches}")

if __name__ == "__main__":
    menu()
