from datetime import datetime
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import utils.corefiles as cf
from config import LIGAS_FILE, EQUIPOS_FILE
import controllers.equipos as equipos_controller

def obtener_nombre_liga_validado(ligas_existentes):
    while True:
        nombre = input("Ingrese el nombre de la liga: ").strip().upper()
        if not nombre:
            print("Error: El nombre de la liga no puede estar vacío.")
            continue
        nombres_existentes = [liga["nombre"].upper() for liga in ligas_existentes.values()]
        if nombre in nombres_existentes:
            print(f"Error: La liga '{nombre}' ya se encuentra registrada.")
            continue
        return nombre

def obtener_pais_validado():
    while True:
        pais = input("Ingrese el país de la liga: ").strip().upper()
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

def agregar_equipos_a_liga(nueva_liga_id, pais_de_la_liga):
    equipos_seleccionados_ids = []
    
    while True:
        limpiar_pantalla()
        equipos_del_pais = equipos_controller.obtenerEquiposPorPais(pais_de_la_liga)
        equipos_disponibles = {}
        for id_equipo, datos_equipo in equipos_del_pais.items():
            if 'liga_id' not in datos_equipo:
                equipos_disponibles[id_equipo] = datos_equipo

        print(f"    Agregar Equipos de '{pais_de_la_liga}' a la Liga    ")
        
        if not equipos_disponibles:
            print(f"No hay equipos disponibles de {pais_de_la_liga} para agregar a la liga.")
            print("Todos los equipos de este país ya están asignados a otras ligas.")
            pausar_pantalla()
            break

        print("Equipos Disponibles:")
        for id_equipo, datos_equipo in equipos_disponibles.items():
            print(f"ID: {id_equipo} - Nombre: {datos_equipo['nombre']} - Ciudad: {datos_equipo['ciudad']}")
        print("-" * 50)

        respuesta = input("Ingrese el ID del equipo a agregar (o 'fin' para terminar): ").strip()
        
        if respuesta.lower() == 'fin':
            break
        
        if respuesta in equipos_disponibles:
            equipos_seleccionados_ids.append(respuesta)
            equipo_agregado = equipos_disponibles[respuesta]
            print(f"¡Equipo '{equipo_agregado['nombre']}' agregado a la liga!")
            pausar_pantalla()
        else:
            print("Error: ID de equipo no válido o ya no disponible.")
            pausar_pantalla()

    return equipos_seleccionados_ids

def subMenuLigas():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Gestión de Ligas ---")
        print("1. Crear una nueva Liga")
        print("2. Listar todas las Ligas")
        print("3. Volver al Menú Principal")
        print("-----------------------------------")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            crearLiga()
        elif opcion == "2":
            listarLigas()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar_pantalla()

def crearLiga():
    limpiar_pantalla()
    print("    Crear Nueva Liga    ")
    
    ligas_existentes = cf.obtenerLigas()
    nuevo_id = cf.generateId(list(ligas_existentes.keys()))
    nombre = obtener_nombre_liga_validado(ligas_existentes)
    pais = obtener_pais_validado()
    fecha_inicial_str = obtener_fecha_valida("Ingrese la fecha de inicio (DD-MM-AAAA): ")
    fecha_final_str = obtener_fecha_valida(
        "Ingrese la fecha de finalización (DD-MM-AAAA): ", 
        fecha_inicial_str, 
        debe_ser_mayor=True )

    ids_equipos_en_liga = agregar_equipos_a_liga(nuevo_id, pais)

    if not ids_equipos_en_liga:
        print("No se puede crear una liga sin equipos.")
        pausar_pantalla()
        return

    nueva_liga = {
        "nombre": nombre,
        "pais": pais,
        "fecha_inicial": fecha_inicial_str,
        "fecha_final": fecha_final_str,
        "equipos_ids": ids_equipos_en_liga,
        "activa": True
    }
    
    ligas_existentes[nuevo_id] = nueva_liga
    cf.guardarLigas(ligas_existentes)
    
    equipos = cf.obtenerEquipos()
    for equipo_id in ids_equipos_en_liga:
        if equipo_id in equipos:
            equipos[equipo_id]['liga_id'] = nuevo_id
    cf.guardarEquipos(equipos)
    
    print(f"¡Liga '{nombre}' (ID: {nuevo_id}) creada exitosamente con {len(ids_equipos_en_liga)} equipos!")
    print(f"Los equipos han sido actualizados con el ID de liga: {nuevo_id}")
    pausar_pantalla()

def listarLigas():
    limpiar_pantalla()
    print("    Listado de Ligas Registradas    ")
    
    ligas = cf.obtenerLigas()
    equipos = cf.obtenerEquipos()

    if not ligas:
        print("No hay ligas registradas.")
    else:
        for liga_id, liga in ligas.items():
            if liga.get("activa", True):
                print(f"\nID: {liga_id}")
                print(f"Nombre: {liga['nombre']}")
                print(f"País: {liga['pais']}")
                print(f"Duración: {liga['fecha_inicial']} a {liga['fecha_final']}")
                print(f"Equipos participantes: {len(liga.get('equipos_ids', []))}")
                equipos_liga = liga.get('equipos_ids', [])
                if equipos_liga:
                    print("Equipos:")
                    for equipo_id in equipos_liga:
                        if equipo_id in equipos:
                            equipo = equipos[equipo_id]
                            print(f"  - {equipo['nombre']} (ID: {equipo_id})")
                        else:
                            print(f"  - Equipo ID {equipo_id} (No encontrado)")
                
                print("-" * 50)
    
    print("Presione Enter para continuar...")
    pausar_pantalla()

def obtenerLigaPorId(liga_id: str):
    ligas = cf.obtenerLigas()
    return ligas.get(liga_id)

def obtenerLigasPorPais(pais: str):
    ligas = cf.obtenerLigas()
    return {id_lg: lg for id_lg, lg in ligas.items() 
            if lg.get("pais", "").upper() == pais.upper() and lg.get("activa", True)}

def obtenerTodasLigas():
    ligas = cf.obtenerLigas()
    return {id_lg: lg for id_lg, lg in ligas.items() if lg.get("activa", True)}

def obtenerEquiposDeLiga(liga_id: str):
    liga = obtenerLigaPorId(liga_id)
    if not liga:
        return {}
    
    equipos = cf.obtenerEquipos()
    equipos_ids = liga.get('equipos_ids', [])
    
    return {eq_id: equipos[eq_id] for eq_id in equipos_ids if eq_id in equipos}

def verificarEquipoEnLiga(equipo_id: str, liga_id: str):
    liga = obtenerLigaPorId(liga_id)
    if not liga:
        return False
    return equipo_id in liga.get('equipos_ids', [])