import os
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import utils.corefiles as cf
from config import PARTIDOS_FILE
import controllers.ligas as ligas_controller
import controllers.torneos as torneos_controller
import controllers.equipos as equipos_controller

def validar_formato_fecha(fecha):
    """Valida que la fecha tenga formato DD-MM-AAAA"""
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
        print("4. Salir al menú principal")
        print("--------------------------------------")
        
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
    
    # Mostrar ligas disponibles
    print("Ligas disponibles:")
    for liga_id, liga in ligas.items():
        if liga.get("activa", True):
            print(f"ID: {liga_id} - {liga['nombre']} ({liga['pais']})")
    
    liga_id = input("\nIngrese el ID de la liga: ").strip()
    
    if liga_id not in ligas:
        print("Liga no encontrada.")
        pausar_pantalla()
        return
    
    liga = ligas[liga_id]
    equipos_liga = liga.get('equipos_ids', [])
    
    if len(equipos_liga) < 2:
        print("La liga debe tener al menos 2 equipos para registrar un partido.")
        pausar_pantalla()
        return
    
    print(f"\n--- Equipos de la Liga {liga['nombre']} ---")
    for equipo_id in equipos_liga:
        if equipo_id in equipos:
            equipo = equipos[equipo_id]
            print(f"ID: {equipo_id} - {equipo['nombre']}")
    
    # Seleccionar equipo local
    while True:
        equipo_local_id = input("\nIngrese el ID del equipo local: ").strip()
        if equipo_local_id in equipos_liga and equipo_local_id in equipos:
            break
        else:
            print("Error: ID de equipo no válido o no pertenece a esta liga.")
    
    # Seleccionar equipo visitante
    while True:
        equipo_visitante_id = input("Ingrese el ID del equipo visitante: ").strip()
        if equipo_visitante_id in equipos_liga and equipo_visitante_id in equipos:
            if equipo_visitante_id != equipo_local_id:
                break
            else:
                print("Error: El equipo visitante debe ser diferente al local.")
        else:
            print("Error: ID de equipo no válido o no pertenece a esta liga.")
    
    fecha_partido = obtener_fecha_valida("Ingrese la fecha del partido (DD-MM-AAAA): ")
    
    # Obtener resultados
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
    
    # Generar ID único numérico ascendente
    partidos = cf.readJson(PARTIDOS_FILE)
    nuevo_id = cf.generateId(list(partidos.keys()))
    
    nuevo_partido = {
        "tipo": "Liga",
        "liga_id": liga_id,
        "liga_nombre": liga['nombre'],
        "equipo_local_id": equipo_local_id,
        "equipo_local_nombre": equipos[equipo_local_id]['nombre'],
        "equipo_visitante_id": equipo_visitante_id,
        "equipo_visitante_nombre": equipos[equipo_visitante_id]['nombre'],
        "fecha": fecha_partido,
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
        "resultado": "Victoria Local" if goles_local > goles_visitante else "Victoria Visitante" if goles_visitante > goles_local else "Empate"
    }
    
    partidos[nuevo_id] = nuevo_partido
    cf.writeJson(partidos, PARTIDOS_FILE)
    
    print(f"\n¡Partido registrado exitosamente!")
    print(f"{equipos[equipo_local_id]['nombre']} {goles_local} - {goles_visitante} {equipos[equipo_visitante_id]['nombre']}")
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
    
    # Mostrar torneos disponibles
    print("Torneos disponibles:")
    for torneo_id, torneo in torneos.items():
        if torneo.get("activo", True):
            print(f"ID: {torneo_id} - {torneo['nombre']} (Organizador: {torneo.get('pais_organizador', torneo.get('pais', 'N/A'))})")
    
    torneo_id = input("\nIngrese el ID del torneo: ").strip()
    
    if torneo_id not in torneos:
        print("Torneo no encontrado.")
        pausar_pantalla()
        return
    
    torneo = torneos[torneo_id]
    equipos_torneo = torneo.get('equipos_ids', [])
    
    if len(equipos_torneo) < 2:
        print("El torneo debe tener al menos 2 equipos para registrar un partido.")
        pausar_pantalla()
        return
    
    print(f"\n--- Equipos del Torneo {torneo['nombre']} ---")
    for equipo_id in equipos_torneo:
        if equipo_id in equipos:
            equipo = equipos[equipo_id]
            print(f"ID: {equipo_id} - {equipo['nombre']} ({equipo['pais']})")
    
    # Seleccionar equipo local
    while True:
        equipo_local_id = input("\nIngrese el ID del equipo local: ").strip()
        if equipo_local_id in equipos_torneo and equipo_local_id in equipos:
            break
        else:
            print("Error: ID de equipo no válido o no pertenece a este torneo.")
    
    # Seleccionar equipo visitante
    while True:
        equipo_visitante_id = input("Ingrese el ID del equipo visitante: ").strip()
        if equipo_visitante_id in equipos_torneo and equipo_visitante_id in equipos:
            if equipo_visitante_id != equipo_local_id:
                break
            else:
                print("Error: El equipo visitante debe ser diferente al local.")
        else:
            print("Error: ID de equipo no válido o no pertenece a este torneo.")
    
    fecha_partido = obtener_fecha_valida("Ingrese la fecha del partido (DD-MM-AAAA): ")
    
    # Obtener resultados
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
    
    # Generar ID único numérico ascendente
    partidos = cf.readJson(PARTIDOS_FILE)
    nuevo_id = cf.generateId(list(partidos.keys()))
    
    nuevo_partido = {
        "tipo": "Torneo",
        "torneo_id": torneo_id,
        "torneo_nombre": torneo['nombre'],
        "equipo_local_id": equipo_local_id,
        "equipo_local_nombre": equipos[equipo_local_id]['nombre'],
        "equipo_visitante_id": equipo_visitante_id,
        "equipo_visitante_nombre": equipos[equipo_visitante_id]['nombre'],
        "fecha": fecha_partido,
        "goles_local": goles_local,
        "goles_visitante": goles_visitante,
        "resultado": "Victoria Local" if goles_local > goles_visitante else "Victoria Visitante" if goles_visitante > goles_local else "Empate"
    }
    
    partidos[nuevo_id] = nuevo_partido
    cf.writeJson(partidos, PARTIDOS_FILE)
    
    print(f"\n¡Partido registrado exitosamente!")
    print(f"{equipos[equipo_local_id]['nombre']} {goles_local} - {goles_visitante} {equipos[equipo_visitante_id]['nombre']}")
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