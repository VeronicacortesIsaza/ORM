from login import login
from database.config import SessionLocal
from entities.habitacion import Habitacion
from entities.reserva import Reserva

def menu():
    session = SessionLocal()
    try:
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
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
    finally:
        session.close()
from datetime import date, timedelta

def reservar_habitacion(session, cliente_actual):
    if not cliente_actual:
        print("Debes iniciar sesión como cliente para reservar.")
        return

    while True:
        noches = input("Número de noches: ")
        if noches.isdigit():
            noches = int(noches)
            if noches > 0:
                break
            print("Debe ser mayor a cero.")
        else:
            print("Debes ingresar un número válido.")

    print("\nTipos de habitación:")
    print("1. Estándar ($200000/noche)")
    print("2. Suite ($300000/noche)")
    print("3. Premium ($450000/noche)")

    while True:
        tipo = input("Selecciona el tipo de habitación (1-3): ")
        if tipo.isdigit():
            tipo = int(tipo)
            if 1 <= tipo <= 3:
                break
            print("Debes seleccionar entre 1 y 3.")
        else:
            print("Debes ingresar un número válido.")
    habitacion = session.query(Habitacion).filter_by(tipo=tipo, disponible=True).first()
    if habitacion:
        precio_noche = habitacion.precio
        total = precio_noche * noches
    else:
        print("No hay habitaciones disponibles de ese tipo.")
        return

    fecha_entrada = date.today()
    fecha_salida = fecha_entrada + timedelta(days=noches)
    fecha_creacion = date.today()
    print(f"\nFecha entrada: {fecha_entrada}")
    print(f"Fecha salida: {fecha_salida}")
    print(f"Total: {noches} noches x ${precio_noche:,} = ${total:,}")

    confirmar = input("¿Desea confirmar la reserva? (s/n): ").lower()
    if confirmar != "s":
        print("Reserva cancelada.")
        return

    reserva = Reserva(
        id_cliente=cliente_actual.id_cliente,
        id_habitacion=habitacion.id_habitacion,
        fecha_entrada=fecha_entrada,
        fecha_salida=fecha_salida,
        estado_reserva="Activa",
        noches=noches,
        costo_total=total,
        id_usuario_crea=cliente_actual.id_cliente,
        fecha_creacion=fecha_creacion
    )

    habitacion.disponible = False
    session.add(reserva)
    session.commit()

    print(f"\nReserva creada para {cliente_actual.usuario.nombre} {cliente_actual.usuario.apellidos}")
    print(f"Habitación {habitacion.numero} - Total: ${total:,}")
    print(f"Del {fecha_entrada} al {fecha_salida}")

def cancelar_reserva(session):
    correo = input("Ingrese correo del cliente para cancelar la reserva: ")
    reserva = session.query(Reserva).filter_by(correo=correo).first()
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
    for r in reservas:
        print(f"{r.cliente} - {r.documento} - {r.habitacion.tipo} - {r.noches} noches")

if __name__ == "__main__":
    if login():
        menu()
    else:
        print("No se pudo iniciar sesión.")
