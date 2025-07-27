
import os
import json
import datetime
from utils.screenControllers import limpiar_pantalla, pausar_pantalla

RUTA_JUGADORES_JSON = os.path.join("data", "jugadores.json")
RUTA_EQUIPOS_JSON = os.path.join("data", "equipos.json")
RUTA_TRANSFERENCIAS_JSON = os.path.join("data", "transferencias.json")

TIPOS_TRANSFERENCIA = [
    "Transferencia definitiva",
    "Cesión o préstamo",
    "Transferencia libre",
    "Cláusula de rescisión",
    "Intercambio de jugadores",
    "Transferencias de juveniles",
    "Co-propiedad",
    "Transferencia por subasta o tribunal"
]

def cargar_datos(ruta_archivo):
    os.makedirs("data", exist_ok=True)
    try:
        with open(ruta_archivo, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(datos, ruta_archivo):
    with open(ruta_archivo, 'w') as f:
        json.dump(datos, f, indent=4)

def obtener_fecha_valida():
    while True:
        fecha_str = input("Ingrese la fecha de la transferencia (YYYY-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha_str
        except ValueError:
            print("Error: Formato de fecha no válido. Por favor, use YYYY-MM-DD (ej: 2024-07-28).")

def subMenuTransferencias():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Transferencias ---")
        print("1. Realizar una nueva transferencia")
        print("2. Ver historial de transferencias")
        print("3. Volver al Menú Principal")
        print("---------------------------------")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            transferir_jugador()
        elif opcion == '2':
            ver_transferencias()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar_pantalla()

def transferir_jugador():
    jugadores = cargar_datos(RUTA_JUGADORES_JSON)
    equipos = cargar_datos(RUTA_EQUIPOS_JSON)
    transferencias = cargar_datos(RUTA_TRANSFERENCIAS_JSON)

    if not jugadores or not equipos:
        print("Error: Se necesitan datos de jugadores y equipos para realizar una transferencia.")
        pausar_pantalla()
        return

    mapa_equipos = {e['id']: e['nombre'] for e in equipos}

    while True:
        limpiar_pantalla()
        print("--- Jugadores Disponibles para Transferir ---")
        for jugador in jugadores:
            nombre_equipo_actual = mapa_equipos.get(jugador.get('equipo_id'), "Sin Equipo")
            print(f"ID: {jugador['id']} | Nombre: {jugador['nombre']} | Equipo: {nombre_equipo_actual}")
        print("---------------------------------------------")
        
        try:
            jugador_id = int(input("Ingrese el ID del jugador a transferir: "))
            jugador_a_transferir = next((j for j in jugadores if j['id'] == jugador_id), None)
            if jugador_a_transferir:
                break
            else:
                print("\nError: No se encontró un jugador con ese ID. Intente de nuevo.")
                pausar_pantalla()
        except ValueError:
            print("\nError: Por favor, ingrese un número de ID válido. Intente de nuevo.")
            pausar_pantalla()

    equipo_origen_id = jugador_a_transferir['equipo_id']
    nombre_origen = mapa_equipos.get(equipo_origen_id, "Desconocido")
    
    limpiar_pantalla()
    print(f"Jugador seleccionado: {jugador_a_transferir['nombre']}")
    print(f"Equipo de Origen: {nombre_origen} (ID: {equipo_origen_id})")

    equipos_disponibles = [e for e in equipos if e['id'] != equipo_origen_id]
    
    while True:
        print("\n--- Equipos de Destino Disponibles ---")
        for equipo in equipos_disponibles:
            print(f"ID: {equipo['id']} - Nombre: {equipo['nombre']}")
        print("------------------------------------")
        try:
            equipo_destino_id = int(input("Ingrese el ID del nuevo equipo: "))
            if equipo_destino_id in [e['id'] for e in equipos_disponibles]:
                break
            else:
                print("Error: ID de equipo no válido o es el mismo equipo de origen.")
                pausar_pantalla()
                limpiar_pantalla()
        except ValueError:
            print("Error: Por favor, ingrese un número de ID válido.")
            pausar_pantalla()
            limpiar_pantalla()

    tipo_transferencia = ""
    while True:
        limpiar_pantalla()
        print("--- Tipos de Transferencia Disponibles ---")
        for i, tipo in enumerate(TIPOS_TRANSFERENCIA):
            print(f"{i + 1}. {tipo}")
        print("----------------------------------------")
        try:
            opcion_tipo = int(input("Seleccione el número del tipo de transferencia: "))
            if 1 <= opcion_tipo <= len(TIPOS_TRANSFERENCIA):
                tipo_transferencia = TIPOS_TRANSFERENCIA[opcion_tipo - 1]
                break
            else:
                print("Error: Número de opción no válido. Intente de nuevo.")
                pausar_pantalla()
        except ValueError:
            print("Error: Debe ingresar un número. Intente de nuevo.")
            pausar_pantalla()

    fecha_transferencia = obtener_fecha_valida()
    
    nueva_transferencia = {
        "jugador_id": jugador_id,
        "equipo_origen_id": equipo_origen_id,
        "equipo_destino_id": equipo_destino_id,
        "tipo": tipo_transferencia,
        "fecha": fecha_transferencia
    }
    transferencias.append(nueva_transferencia)
    guardar_datos(transferencias, RUTA_TRANSFERENCIAS_JSON)

    for jugador in jugadores:
        if jugador['id'] == jugador_id:
            jugador['equipo_id'] = equipo_destino_id
            break
    guardar_datos(jugadores, RUTA_JUGADORES_JSON)
    
    print("\n¡Transferencia completada y registrada exitosamente!")
    pausar_pantalla()


def ver_transferencias():
    limpiar_pantalla()
    print("--- Historial de Transferencias Realizadas ---")

    transferencias = cargar_datos(RUTA_TRANSFERENCIAS_JSON)
    jugadores = cargar_datos(RUTA_JUGADORES_JSON)
    equipos = cargar_datos(RUTA_EQUIPOS_JSON)
    
    if not transferencias:
        print("No hay transferencias registradas aún.")
    else:
        mapa_jugadores = {j['id']: j['nombre'] for j in jugadores}
        mapa_equipos = {e['id']: e['nombre'] for e in equipos}

        for trans in transferencias:
            nombre_jugador = mapa_jugadores.get(trans['jugador_id'], "Jugador Desconocido")
            nombre_origen = mapa_equipos.get(trans['equipo_origen_id'], "Equipo Origen Desconocido")
            nombre_destino = mapa_equipos.get(trans['equipo_destino_id'], "Equipo Destino Desconocido")

            print(f"  Fecha: {trans['fecha']}")
            print(f"  Jugador: {nombre_jugador} (ID: {trans['jugador_id']})")
            print(f"  Origen: {nombre_origen} -> Destino: {nombre_destino}")
            print(f"  Tipo: {trans['tipo']}")
            print("-" * 40)
    print("Presione Enter para continuar...")
    pausar_pantalla()

