from datetime import datetime
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import utils.corefiles as cf
from config import TORNEOS_FILE, EQUIPOS_FILE
import controllers.equipos as equipos_controller

def obtener_nombre_torneo_validado(torneos_existentes):
    while True:
        nombre = input("Ingrese el nombre del torneo: ").strip().upper()
        if not nombre:
            print("Error: El nombre del torneo no puede estar vacío.")
            continue
        
        nombres_existentes = [torneo["nombre"].upper() for torneo in torneos_existentes.values()]
        if nombre in nombres_existentes:
            print(f"Error: El torneo '{nombre}' ya se encuentra registrado.")
            continue
            
        return nombre

def obtener_pais_validado():
    while True:
        pais = input("Ingrese el país organizador del torneo: ").strip().upper()
        if not pais:
            print("Error: El país no puede estar vacío.")
            continue

        if all(c.isalpha() or c.isspace() for c in pais):
            return pais
        else:
            print("Error: El país solo puede contener letras y espacios.")

def convertir_fecha_a_datetime(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%d-%m-%Y")
    except ValueError:
        return None

def obtener_fecha_valida(prompt, fecha_referencia=None, debe_ser_mayor=False):
    while True:
        fecha_str = input(prompt).strip()
        if not validar_formato_fecha(fecha_str):
            print("Error: Formato de fecha no válido. Por favor, use DD-MM-AAAA.")
            continue
        
        if fecha_referencia and debe_ser_mayor:
            fecha_actual = convertir_fecha_a_datetime(fecha_str)
            fecha_ref = convertir_fecha_a_datetime(fecha_referencia)
            
            if fecha_actual and fecha_ref:
                if fecha_actual <= fecha_ref:
                    print(f"Error: La fecha final debe ser mayor a la fecha inicial ({fecha_referencia}).")
                    continue
        
        return fecha_str

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

def agregar_equipos_a_torneo(nuevo_torneo_id):
    equipos_seleccionados_ids = []
    
    while True:
        limpiar_pantalla()
        
        todos_equipos = equipos_controller.obtenerTodosEquipos()

        equipos_disponibles = {}
        for id_equipo, datos_equipo in todos_equipos.items():
            if id_equipo not in equipos_seleccionados_ids:
                equipos_disponibles[id_equipo] = datos_equipo

        print(f"--- Agregar Equipos al Torneo ---")
        
        if not equipos_disponibles:
            print("No hay más equipos disponibles para agregar al torneo.")
            pausar_pantalla()
            break

        print("Equipos Disponibles:")
        for id_equipo, datos_equipo in equipos_disponibles.items():
            print(f"ID: {id_equipo} - Nombre: {datos_equipo['nombre']} - País: {datos_equipo['pais']} - Ciudad: {datos_equipo['ciudad']}")
        print("-" * 50)
        
        if equipos_seleccionados_ids:
            print(f"Equipos ya agregados: {len(equipos_seleccionados_ids)}")
            print("Equipos seleccionados:")
            for eq_id in equipos_seleccionados_ids:
                if eq_id in todos_equipos:
                    print(f"  - {todos_equipos[eq_id]['nombre']} ({todos_equipos[eq_id]['pais']})")
            print("-" * 50)

        respuesta = input("Ingrese el ID del equipo a agregar (o 'fin' para terminar): ").strip()
        
        if respuesta.lower() == 'fin':
            break
        
        if respuesta in equipos_disponibles:
            equipos_seleccionados_ids.append(respuesta)
            equipo_agregado = equipos_disponibles[respuesta]
            print(f"¡Equipo '{equipo_agregado['nombre']}' agregado al torneo!")
            pausar_pantalla()
        else:
            print("Error: ID de equipo no válido o ya agregado.")
            pausar_pantalla()

    return equipos_seleccionados_ids

def subMenuTorneos():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Gestión de Torneos ---")
        print("1. Crear un nuevo Torneo")
        print("2. Listar todos los Torneos")
        print("3. Volver al Menú Principal")
        print("-" * 40)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            crearTorneo()
        elif opcion == "2":
            listarTorneos()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar_pantalla()

def crearTorneo():
    limpiar_pantalla()
    print("--- Crear Nuevo Torneo ---")
    
    torneos_existentes = cf.obtenerTorneos()
    nuevo_id = cf.generateId(list(torneos_existentes.keys()))
    nombre = obtener_nombre_torneo_validado(torneos_existentes)
    pais = obtener_pais_validado()
    fecha_inicial_str = obtener_fecha_valida("Ingrese la fecha de inicio (DD-MM-AAAA): ")
    fecha_final_str = obtener_fecha_valida(
        "Ingrese la fecha de finalización (DD-MM-AAAA): ", 
        fecha_inicial_str, 
        debe_ser_mayor=True )

    print("     Agregando Equipos al Torneo     ")
    print("Nota: En los torneos pueden participar equipos de cualquier país")
    pausar_pantalla()
    
    ids_equipos_en_torneo = agregar_equipos_a_torneo(nuevo_id)

    if not ids_equipos_en_torneo:
        print("No se puede crear un torneo sin equipos.")
        pausar_pantalla()
        return

    nuevo_torneo = {
        "nombre": nombre,
        "pais_organizador": pais,
        "fecha_inicial": fecha_inicial_str,
        "fecha_final": fecha_final_str,
        "equipos_ids": ids_equipos_en_torneo,
        "activo": True
    }
    
    torneos_existentes[nuevo_id] = nuevo_torneo
    cf.guardarTorneos(torneos_existentes)
    
    print(f"Torneo '{nombre}' creado exitosamente con {len(ids_equipos_en_torneo)} equipos")
    pausar_pantalla()

def listarTorneos():
    limpiar_pantalla()
    print("--- Listado de Torneos Registrados ---")
    
    torneos = cf.obtenerTorneos()
    equipos = cf.obtenerEquipos()

    if not torneos:
        print("No hay torneos registrados.")
    else:
        for torneo_id, torneo in torneos.items():
            if torneo.get("activo", True):
                print(f"ID: {torneo_id}")
                print(f"Nombre: {torneo['nombre']}")
                print(f"País Organizador: {torneo.get('pais_organizador', torneo.get('pais', 'N/A'))}")
                print(f"Duración: {torneo['fecha_inicial']} a {torneo['fecha_final']}")
                print(f"Equipos participantes: {len(torneo.get('equipos_ids', []))}")
                print("-" * 60)
    
    print("Presione Enter para continuar...")
    pausar_pantalla()

def obtenerTorneoPorId(torneo_id: str):
    torneos = cf.obtenerTorneos()
    return torneos.get(torneo_id)

def obtenerTorneosPorPais(pais: str):
    torneos = cf.obtenerTorneos()
    return {id_tr: tr for id_tr, tr in torneos.items() 
            if tr.get("pais_organizador", tr.get("pais", "")).upper() == pais.upper() and tr.get("activo", True)}

def obtenerTodosTorneos():
    torneos = cf.obtenerTorneos()
    return {id_tr: tr for id_tr, tr in torneos.items() if tr.get("activo", True)}