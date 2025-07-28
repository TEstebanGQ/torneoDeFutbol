from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import utils.corefiles as cf
from config import PARTIDOS_FILE


def validar_formato_fecha(fecha):
    try:
        partes = fecha.split('-')
        if len(partes) != 3:
            return False
        
        dia, mes, año = partes
        if len(dia) != 2 or len(mes) != 2 or len(año) != 4:
            return False
        
        dia_int = int(dia)
        mes_int = int(mes)
        año_int = int(año)
        
        if not (1 <= dia_int <= 31):
            return False
        if not (1 <= mes_int <= 12):
            return False
        if not (1900 <= año_int <= 2100):
            return False
        
        return True
    except ValueError:
        return False

def obtener_fecha_valida(prompt):
    while True:
        fecha_str = input(prompt).strip()
        if validar_formato_fecha(fecha_str):
            return fecha_str
        else:
            print("Error: Formato de fecha no válido. Por favor, use DD-MM-AAAA.")

def subMenuPartidos():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Gestión de Partidos ---")
        print("1. Registrar partidos de ligas")
        print("2. Registrar partidos de torneos")
        print("3. Listar partidos")
        print("4. Volver al menú principal")
        print('-' * 40)
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_partido_liga()
        elif opcion == '2':
            registrar_partido_torneo()
        elif opcion == '3':
            listar_partidos()
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar_pantalla()

def registrar_partido_liga():
    limpiar_pantalla()
    print("--- Registrar Partido de Liga ---")
    
    ligas = cf.obtenerLigas()
    equipos = cf.obtenerEquipos()
    
    if not ligas:
        print("No hay ligas registradas.")
        pausar_pantalla()
        return
    print("Ligas disponibles:")
    ligas_activas = {}
    for liga_id, liga in ligas.items():
        if liga.get("activa", True):
            ligas_activas[liga_id] = liga
            print(f"ID: {liga_id} - {liga['nombre']} ({liga['pais']})")
    
    if not ligas_activas:
        print("No hay ligas activas disponibles.")
        pausar_pantalla()
        return
    
    liga_id = input("\nIngrese el ID de la liga: ").strip()
    
    if liga_id not in ligas_activas:
        print("Liga no encontrada o no está activa.")
        pausar_pantalla()
        return
    
    liga = ligas_activas[liga_id]
    equipos_liga = liga.get('equipos_ids', [])
    
    if len(equipos_liga) < 2:
        print("La liga debe tener al menos 2 equipos para registrar un partido.")
        pausar_pantalla()
        return
    
    print(f"\n--- Equipos de la Liga {liga['nombre']} ---")
    equipos_validos = {}
    for equipo_id in equipos_liga:
        if equipo_id in equipos and equipos[equipo_id].get("activo", True):
            equipo = equipos[equipo_id]
            equipos_validos[equipo_id] = equipo
            print(f"ID: {equipo_id} - {equipo['nombre']}")
    
    if len(equipos_validos) < 2:
        print("No hay suficientes equipos activos en esta liga para registrar un partido.")
        pausar_pantalla()
        return
    
    while True:
        equipo_local_id = input("\nIngrese el ID del equipo local: ").strip()
        if equipo_local_id in equipos_validos:
            break
        else:
            print("Error: ID de equipo no válido o no pertenece a esta liga.")

    while True:
        equipo_visitante_id = input("Ingrese el ID del equipo visitante: ").strip()
        if equipo_visitante_id in equipos_validos:
            if equipo_visitante_id != equipo_local_id:
                break
            else:
                print("Error: El equipo visitante debe ser diferente al local.")
        else:
            print("Error: ID de equipo no válido o no pertenece a esta liga.")
    
    fecha_partido = obtener_fecha_valida("Ingrese la fecha del partido (DD-MM-AAAA): ")

    try:
        goles_local = int(input("Ingrese goles del equipo local: "))
        goles_visitante = int(input("Ingrese goles del equipo visitante: "))
        if goles_local < 0 or goles_visitante < 0:
            print("Error: Los goles no pueden ser negativos.")
            pausar_pantalla()
            return
    except ValueError:
        print("Error: Debe ingresar números válidos para los goles.")
        pausar_pantalla()
        return

    partidos = cf.readJson(PARTIDOS_FILE)
    nuevo_id = cf.generateId(list(partidos.keys()))
    
    nuevo_partido = {
        "tipo": "Liga",
        "liga_id": liga_id,
        "liga_nombre": liga['nombre'],
        "equipo_local_id": equipo_local_id,
        "equipo_local_nombre": equipos_validos[equipo_local_id]['nombre'],
        "equipo_visitante_id": equipo_visitante_id,
        "equipo_visitante_nombre": equipos_validos[equipo_visitante_id]['nombre'],
        "fecha": fecha_partido,
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
        "resultado": "Victoria Local" if goles_local > goles_visitante else "Victoria Visitante" if goles_visitante > goles_local else "Empate"
    }
    
    partidos[nuevo_id] = nuevo_partido
    cf.writeJson(partidos, PARTIDOS_FILE)
    
    print(f"\n¡Partido registrado exitosamente!")
    print(f"{equipos_validos[equipo_local_id]['nombre']} {goles_local} - {goles_visitante} {equipos_validos[equipo_visitante_id]['nombre']}")
    print(f"Resultado: {nuevo_partido['resultado']}")
    pausar_pantalla()

def registrar_partido_torneo():
    limpiar_pantalla()
    print("--- Registrar Partido de Torneo ---")
    
    torneos = cf.obtenerTorneos()
    equipos = cf.obtenerEquipos()
    
    if not torneos:
        print("No hay torneos registrados.")
        pausar_pantalla()
        return

    print("Torneos disponibles:")
    torneos_activos = {}
    for torneo_id, torneo in torneos.items():
        if torneo.get("activo", True):
            torneos_activos[torneo_id] = torneo
            print(f"ID: {torneo_id} - {torneo['nombre']} (Organizador: {torneo.get('pais_organizador', torneo.get('pais', 'N/A'))})")
    
    if not torneos_activos:
        print("No hay torneos activos disponibles.")
        pausar_pantalla()
        return
    
    torneo_id = input("Ingrese el ID del torneo: ").strip()
    
    if torneo_id not in torneos_activos:
        print("Torneo no encontrado o no está activo.")
        pausar_pantalla()
        return
    
    torneo = torneos_activos[torneo_id]
    equipos_torneo = torneo.get('equipos_ids', [])
    
    if len(equipos_torneo) < 2:
        print("El torneo debe tener al menos 2 equipos para registrar un partido.")
        pausar_pantalla()
        return
    
    print(f"--- Equipos del Torneo {torneo['nombre']} ---")
    equipos_validos = {}
    for equipo_id in equipos_torneo:
        if equipo_id in equipos and equipos[equipo_id].get("activo", True):
            equipo = equipos[equipo_id]
            equipos_validos[equipo_id] = equipo
            print(f"ID: {equipo_id} - {equipo['nombre']} ({equipo['pais']})")
    
    if len(equipos_validos) < 2:
        print("No hay suficientes equipos activos en este torneo para registrar un partido.")
        pausar_pantalla()
        return

    while True:
        equipo_local_id = input("Ingrese el ID del equipo local: ").strip()
        if equipo_local_id in equipos_validos:
            break
        else:
            print("Error: ID de equipo no válido o no pertenece a este torneo.")

    while True:
        equipo_visitante_id = input("Ingrese el ID del equipo visitante: ").strip()
        if equipo_visitante_id in equipos_validos:
            if equipo_visitante_id != equipo_local_id:
                break
            else:
                print("Error: El equipo visitante debe ser diferente al local.")
        else:
            print("Error: ID de equipo no válido o no pertenece a este torneo.")
    
    fecha_partido = obtener_fecha_valida("Ingrese la fecha del partido (DD-MM-AAAA): ")
    
    try:
        goles_local = int(input("Ingrese goles del equipo local: "))
        goles_visitante = int(input("Ingrese goles del equipo visitante: "))
        if goles_local < 0 or goles_visitante < 0:
            print("Error: Los goles no pueden ser negativos.")
            pausar_pantalla()
            return
    except ValueError:
        print("Error: Debe ingresar números válidos para los goles.")
        pausar_pantalla()
        return
    
    partidos = cf.readJson(PARTIDOS_FILE)
    nuevo_id = cf.generateId(list(partidos.keys()))
    
    nuevo_partido = {
        "tipo": "Torneo",
        "torneo_id": torneo_id,
        "torneo_nombre": torneo['nombre'],
        "equipo_local_id": equipo_local_id,
        "equipo_local_nombre": equipos_validos[equipo_local_id]['nombre'],
        "equipo_visitante_id": equipo_visitante_id,
        "equipo_visitante_nombre": equipos_validos[equipo_visitante_id]['nombre'],
        "fecha": fecha_partido,
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
        "resultado": "Victoria Local" if goles_local > goles_visitante else "Victoria Visitante" if goles_visitante > goles_local else "Empate"
    }
    
    partidos[nuevo_id] = nuevo_partido
    cf.writeJson(partidos, PARTIDOS_FILE)
    
    print(f"¡Partido registrado exitosamente!")
    print(f"{equipos_validos[equipo_local_id]['nombre']} {goles_local} - {goles_visitante} {equipos_validos[equipo_visitante_id]['nombre']}")
    print(f"Resultado: {nuevo_partido['resultado']}")
    pausar_pantalla()

def listar_partidos():
    limpiar_pantalla()
    print("--- Lista de Partidos Registrados ---")
    
    partidos = cf.readJson(PARTIDOS_FILE)
    
    if not partidos:
        print("No hay partidos registrados.")
    else:
        print(f"Total de partidos: {len(partidos)}")
        print("-" * 80)
        
        for partido_id, partido in partidos.items():
            print(f"ID: {partido_id} | Tipo: {partido['tipo']}")
            
            if partido['tipo'] == 'Liga':
                print(f"Liga: {partido.get('liga_nombre', 'N/A')}")
            else:
                print(f"Torneo: {partido.get('torneo_nombre', 'N/A')}")
            
            print(f"Fecha: {partido['fecha']}")
            print(f"{partido['equipo_local_nombre']} {partido['goles_local']} - {partido['goles_visitante']} {partido['equipo_visitante_nombre']}")
            print(f"Resultado: {partido['resultado']}")
            print("-" * 80)
    
    print("Presione Enter para continuar...")
    pausar_pantalla()