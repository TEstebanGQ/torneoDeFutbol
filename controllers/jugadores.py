
import os 
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import json 

RUTA_JUGADORES_JSON = os.path.join("data", "jugadores.json")
RUTA_EQUIPOS_JSON = os.path.join("data", "equipos.json")

POSICIONES_VALIDAS = [
    "Portero",
    "Defensa Central Derecho",
    "Defensa Central Izquierdo",
    "Defensa Central",
    "Lateral Derecho",
    "Lateral Izquierdo",
    "Líbero",
    "Centrocampista Defensivo",
    "Centrocampista Central",
    "Centrocampista Ofensivo",
    "Centrocampista Derecho",
    "Centrocampista Izquierdo",
    "Extremo Derecho",
    "Extremo Izquierdo",
    "Delantero Centro"
]

def cargar_datos_jugadores():
    os.makedirs("data", exist_ok=True)
    try:
        with open(RUTA_JUGADORES_JSON, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos_jugadores(datos):
    with open(RUTA_JUGADORES_JSON, 'w') as f:
        json.dump(datos, f, indent=4)

def cargar_datos_equipos():
    try:
        with open(RUTA_EQUIPOS_JSON, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

lista_de_jugadores = cargar_datos_jugadores()

def obtener_id_validado():
    while True:
        try:
            id_str = input("Ingrese el ID del jugador: ").strip()
            id_ingresado = int(id_str)
            
            ids_existentes = [jugador.get("id") for jugador in lista_de_jugadores]
            if id_ingresado in ids_existentes:
                print("Error: El ID ingresado ya existe. Por favor, intente con otro.")
                continue
            
            return id_ingresado
        except ValueError:
            print("Error: Debe ingresar un número entero válido para el ID.")

def obtener_nombre_validado():
    while True:
        nombre = input("Ingrese el nombre del jugador: ").strip()
        if nombre and all(c.isalpha() or c.isspace() for c in nombre):
            return nombre
        else:
            print("Error: El nombre solo puede contener letras y espacios.")

def obtener_dorsal_validado():
    while True:
        dorsal_str = input("Ingrese el número de dorsal (1-99): ").strip()
        try:
            dorsal = int(dorsal_str)
            if 1 <= dorsal <= 99:
                return dorsal
            else:
                print("Error: El dorsal debe ser un número entre 1 y 99.")
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def obtener_posicion_validada():
    while True:
        posicion = input(f"Ingrese la posición: ").strip().title()
        if posicion in POSICIONES_VALIDAS:
            return posicion
        else:
            print("\nError: Posición no válida.")
            print("Las posiciones aceptadas son:", ", ".join(POSICIONES_VALIDAS))
            pausar_pantalla()
            limpiar_pantalla()
            print("--- Registro de Nuevos Jugadores (continuación) ---")

def subMenuJugadores():
    while True:
        limpiar_pantalla() 
        print("--- Submenú de Gestión de Jugadores ---")
        print("1. Registrar un nuevo jugador")
        print("2. Listar todos los jugadores")
        print("3. Volver al menú principal")
        print("-------------------------------------")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crearJugador()
        elif opcion == '2':
            listarJugadores()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar_pantalla()

def crearJugador():
    limpiar_pantalla()
    print("--- Registro de Nuevos Jugadores ---")
    
    equipos = cargar_datos_equipos()
    if not equipos:
        print("Error: No hay equipos registrados. No se puede añadir un jugador.")
        pausar_pantalla()
        return

    while True:
        nuevo_id = obtener_id_validado()
        nombre = obtener_nombre_validado()
        posicion = obtener_posicion_validada()
        dorsal = obtener_dorsal_validado()

        equipo_id_seleccionado = None
        while True:
            limpiar_pantalla()
            print("--- Equipos Disponibles ---")
            for equipo in equipos:
                print(f"ID: {equipo['id']} - Nombre: {equipo['nombre']}")
            print("---------------------------")
            
            try:
                id_ingresado = int(input("Ingrese el ID del equipo al que pertenece el jugador: "))
                ids_validos = [equipo['id'] for equipo in equipos]
                if id_ingresado in ids_validos:
                    equipo_id_seleccionado = id_ingresado
                    break
                else:
                    print("Error: El ID del equipo no existe. Intente de nuevo.")
                    pausar_pantalla()
            except ValueError:
                print("Error: Debe ingresar un número para el ID. Intente de nuevo.")
                pausar_pantalla()

        nuevo_jugador = {
            "id": nuevo_id,
            "nombre": nombre,
            "dorsal": dorsal,
            "posicion": posicion,
            "equipo_id": equipo_id_seleccionado
        }
        
        lista_de_jugadores.append(nuevo_jugador)
        guardar_datos_jugadores(lista_de_jugadores)
        
        print(f"\n¡Jugador '{nombre}' (ID: {nuevo_id}) registrado exitosamente!")
        
        while True:
            seguir = input("\n¿Desea registrar otro jugador? (Si/No): ").lower()
            if seguir in ['si', 'no']:
                break
            else:
                print("Respuesta no válida. Por favor, ingrese 'Si' o 'No'.")
        
        if seguir == 'no':
            break
        
        limpiar_pantalla()
        print("--- Registro de Nuevos Jugadores ---")

def listarJugadores():
    limpiar_pantalla()
    print("--- Lista de Jugadores Registrados ---")
    
    equipos = cargar_datos_equipos()
    mapa_nombres_equipos = {equipo['id']: equipo['nombre'] for equipo in equipos}

    if not lista_de_jugadores:
        print("No hay jugadores registrados.")
    else:
        for jugador in lista_de_jugadores:
            nombre_equipo = mapa_nombres_equipos.get(jugador['equipo_id'], "Equipo no encontrado")
            
            print(f"  ID: {jugador['id']}")
            print(f"  Nombre: {jugador['nombre']}")
            print(f"  Dorsal: {jugador['dorsal']} | Posición: {jugador['posicion']}")
            print(f"  Equipo: {nombre_equipo} (ID: {jugador['equipo_id']})")
            print("-" * 30)
    print("\nPresione Enter para continuar...")    
    pausar_pantalla()
