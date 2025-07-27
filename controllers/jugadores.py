import os 
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import utils.corefiles as cf
from config import JUGADORES_FILE, EQUIPOS_FILE, POSICIONES_VALIDAS
from datetime import datetime

def obtener_nombre_validado():
    while True:
        nombre = input("Ingrese el nombre del jugador: ").strip().upper()
        if nombre and all(c.isalpha() or c.isspace() for c in nombre):
            return nombre
        else:
            print("Error: El nombre solo puede contener letras y espacios.")

def obtener_dorsal_validado(equipo_id):
    """Valida que el dorsal sea único dentro del equipo"""
    jugadores = cf.obtenerJugadores()
    dorsales_ocupados = []
    
    # Obtener dorsales ya ocupados en el equipo
    for jugador in jugadores.values():
        if jugador.get("equipo_id") == equipo_id and jugador.get("activo", True):
            dorsales_ocupados.append(jugador.get("dorsal"))
    
    while True:
        dorsal_str = input("Ingrese el número de dorsal (1-99): ").strip()
        try:
            dorsal = int(dorsal_str)
            if 1 <= dorsal <= 99:
                if dorsal not in dorsales_ocupados:
                    return dorsal
                else:
                    print(f"Error: El dorsal {dorsal} ya está ocupado en este equipo.")
            else:
                print("Error: El dorsal debe ser un número entre 1 y 99.")
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def obtener_posicion_validada():
    while True:
        print("\nPosiciones disponibles:")
        for i, posicion in enumerate(POSICIONES_VALIDAS, 1):
            print(f"{i}. {posicion}")
        
        try:
            opcion = int(input(f"\nSeleccione la posición (1-{len(POSICIONES_VALIDAS)}): "))
            if 1 <= opcion <= len(POSICIONES_VALIDAS):
                return POSICIONES_VALIDAS[opcion - 1]
            else:
                print(f"Error: Seleccione un número entre 1 y {len(POSICIONES_VALIDAS)}.")
        except ValueError:
            print("Error: Debe ingresar un número válido.")

def obtener_fecha_nacimiento():
    while True:
        fecha_str = input("Ingrese la fecha de nacimiento (DD/MM/YYYY): ").strip()
        try:
            fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
            
            # Calcular edad
            hoy = datetime.now()
            edad = hoy.year - fecha_obj.year - ((hoy.month, hoy.day) < (fecha_obj.month, fecha_obj.day))
            
            if edad < 16:
                print("Error: El jugador debe tener al menos 16 años.")
                continue
            elif edad > 50:
                print("Error: Edad no válida para un jugador profesional.")
                continue
                
            return fecha_str, edad
        except ValueError:
            print("Error: Formato de fecha no válido. Use DD/MM/YYYY.")

def obtener_nacionalidad():
    while True:
        nacionalidad = input("Ingrese la nacionalidad: ").strip().upper()
        if nacionalidad and all(c.isalpha() or c.isspace() for c in nacionalidad):
            return nacionalidad
        else:
            print("Error: La nacionalidad solo puede contener letras y espacios.")

def subMenuJugadores():
    while True:
        limpiar_pantalla() 
        print("--- Submenú de Gestión de Jugadores ---")
        print("1. Registrar un nuevo jugador")
        print("2. Listar todos los jugadores")
        print("3. Buscar jugador por equipo")
        print("4. Buscar jugador por ID")
        print("5. Volver al menú principal")
        print("-------------------------------------")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crearJugador()
        elif opcion == '2':
            listarJugadores()
        elif opcion == '3':
            buscarJugadoresPorEquipo()
        elif opcion == '4':
            buscarJugadorPorId()
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar_pantalla()

def crearJugador():
    limpiar_pantalla()
    print("--- Registro de Nuevos Jugadores ---")
    
    equipos = cf.obtenerEquipos()
    if not equipos:
        print("Error: No hay equipos registrados. No se puede añadir un jugador.")
        pausar_pantalla()
        return

    jugadores = cf.obtenerJugadores()

    while True:
        # Generar ID único
        nuevo_id = cf.generateId("JG", list(jugadores.keys()))
        
        nombre = obtener_nombre_validado()
        fecha_nacimiento, edad = obtener_fecha_nacimiento()
        nacionalidad = obtener_nacionalidad()
        posicion = obtener_posicion_validada()

        # Selección de equipo
        equipo_id_seleccionado = None
        while True:
            limpiar_pantalla()
            print("--- Equipos Disponibles ---")
            for equipo_id, equipo in equipos.items():
                if equipo.get("activo", True):
                    print(f"ID: {equipo_id} - Nombre: {equipo['nombre']} - País: {equipo['pais']}")
            print("---------------------------")
            
            equipo_id_input = input("Ingrese el ID del equipo al que pertenece el jugador: ").strip()
            
            if equipo_id_input in equipos and equipos[equipo_id_input].get("activo", True):
                equipo_id_seleccionado = equipo_id_input
                break
            else:
                print("Error: El ID del equipo no existe o está inactivo. Intente de nuevo.")
                pausar_pantalla()

        dorsal = obtener_dorsal_validado(equipo_id_seleccionado)

        nuevo_jugador = {
            "nombre": nombre,
            "dorsal": dorsal,
            "posicion": posicion,
            "equipo_id": equipo_id_seleccionado,
            "fecha_nacimiento": fecha_nacimiento,
            "edad": edad,
            "nacionalidad": nacionalidad,
            "fecha_registro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "activo": True,
            "historial_equipos": [equipo_id_seleccionado]
        }
        
        jugadores[nuevo_id] = nuevo_jugador
        cf.guardarJugadores(jugadores)
        
        equipo_nombre = equipos[equipo_id_seleccionado]['nombre']
        print(f"\n¡Jugador '{nombre}' (ID: {nuevo_id}) registrado exitosamente en {equipo_nombre}!")
        
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
    
    jugadores = cf.obtenerJugadores()
    equipos = cf.obtenerEquipos()

    if not jugadores:
        print("No hay jugadores registrados.")
    else:
        for jugador_id, jugador in jugadores.items():
            if jugador.get("activo", True):
                equipo_nombre = "Equipo no encontrado"
                if jugador['equipo_id'] in equipos:
                    equipo_nombre = equipos[jugador['equipo_id']]['nombre']
                
                print(f"  ID: {jugador_id}")
                print(f"  Nombre: {jugador['nombre']}")
                print(f"  Edad: {jugador.get('edad', 'N/A')} años")
                print(f"  Nacionalidad: {jugador.get('nacionalidad', 'N/A')}")
                print(f"  Dorsal: {jugador['dorsal']} | Posición: {jugador['posicion']}")
                print(f"  Equipo: {equipo_nombre} (ID: {jugador['equipo_id']})")
                print(f"  Registrado: {jugador.get('fecha_registro', 'N/A')}")
                print("-" * 40)
    
    print("\nPresione Enter para continuar...")    
    pausar_pantalla()

def buscarJugadoresPorEquipo():
    limpiar_pantalla()
    print("--- Buscar Jugadores por Equipo ---")
    
    equipos = cf.obtenerEquipos()
    
    if not equipos:
        print("No hay equipos registrados.")
        pausar_pantalla()
        return
    
    print("Equipos disponibles:")
    for equipo_id, equipo in equipos.items():
        if equipo.get("activo", True):
            print(f"ID: {equipo_id} - {equipo['nombre']} ({equipo['pais']})")
    
    equipo_id = input("\nIngrese el ID del equipo: ").strip()
    
    if equipo_id not in equipos:
        print("Equipo no encontrado.")
        pausar_pantalla()
        return
    
    jugadores = cf.obtenerJugadores()
    jugadores_equipo = {jid: j for jid, j in jugadores.items() 
                       if j.get("equipo_id") == equipo_id and j.get("activo", True)}
    
    equipo_nombre = equipos[equipo_id]['nombre']
    
    print(f"\n--- Jugadores de {equipo_nombre} ---")
    
    if not jugadores_equipo:
        print("Este equipo no tiene jugadores registrados.")
    else:
        print(f"Total de jugadores: {len(jugadores_equipo)}\n")
        
        # Agrupar por posición
        jugadores_por_posicion = {}
        for jugador in jugadores_equipo.values():
            posicion = jugador['posicion']
            if posicion not in jugadores_por_posicion:
                jugadores_por_posicion[posicion] = []
            jugadores_por_posicion[posicion].append(jugador)
        
        for posicion, lista_jugadores in jugadores_por_posicion.items():
            print(f"{posicion}:")
            for jugador in lista_jugadores:
                print(f"  - #{jugador['dorsal']} {jugador['nombre']} ({jugador.get('edad', 'N/A')} años)")
            print()
    
    pausar_pantalla()

def buscarJugadorPorId():
    limpiar_pantalla()
    print("--- Buscar Jugador por ID ---")
    
    jugadores = cf.obtenerJugadores()
    
    if not jugadores:
        print("No hay jugadores registrados.")
        pausar_pantalla()
        return
    
    jugador_id = input("Ingrese el ID del jugador: ").strip()
    
    if jugador_id not in jugadores:
        print("Jugador no encontrado.")
        pausar_pantalla()
        return
    
    jugador = jugadores[jugador_id]
    
    if not jugador.get("activo", True):
        print("El jugador encontrado está inactivo.")
        pausar_pantalla()
        return
    
    equipos = cf.obtenerEquipos()
    equipo_nombre = "Equipo no encontrado"
    if jugador['equipo_id'] in equipos:
        equipo_nombre = equipos[jugador['equipo_id']]['nombre']
    
    print(f"\n--- Información del Jugador ---")
    print(f"ID: {jugador_id}")
    print(f"Nombre: {jugador['nombre']}")
    print(f"Fecha de nacimiento: {jugador.get('fecha_nacimiento', 'N/A')}")
    print(f"Edad: {jugador.get('edad', 'N/A')} años")
    print(f"Nacionalidad: {jugador.get('nacionalidad', 'N/A')}")
    print(f"Posición: {jugador['posicion']}")
    print(f"Dorsal: {jugador['dorsal']}")
    print(f"Equipo actual: {equipo_nombre}")
    print(f"Registrado: {jugador.get('fecha_registro', 'N/A')}")
    
    # Mostrar historial de equipos si existe
    if 'historial_equipos' in jugador and len(jugador['historial_equipos']) > 1:
        print(f"\nHistorial de equipos:")
        for eq_id in jugador['historial_equipos']:
            if eq_id in equipos:
                print(f"  - {equipos[eq_id]['nombre']}")
    
    pausar_pantalla()

def obtenerJugadorPorId(jugador_id: str):
    """Función auxiliar para obtener un jugador por ID"""
    jugadores = cf.obtenerJugadores()
    return jugadores.get(jugador_id)

def obtenerJugadoresPorEquipo(equipo_id: str):
    """Función auxiliar para obtener jugadores de un equipo"""
    jugadores = cf.obtenerJugadores()
    return {jid: j for jid, j in jugadores.items() 
            if j.get("equipo_id") == equipo_id and j.get("activo", True)}

def obtenerTodosJugadores():
    """Función auxiliar para obtener todos los jugadores activos"""
    jugadores = cf.obtenerJugadores()
    return {jid: j for jid, j in jugadores.items() if j.get("activo", True)}