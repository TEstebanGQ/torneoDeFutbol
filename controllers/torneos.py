import os
import json
import datetime
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
        
        # Verificar si ya existe un torneo con ese nombre
        nombres_existentes = [torneo["nombre"].upper() for torneo in torneos_existentes.values()]
        if nombre in nombres_existentes:
            print(f"Error: El torneo '{nombre}' ya se encuentra registrado.")
            continue
            
        return nombre

def obtener_pais_validado():
    while True:
        pais = input("Ingrese el país del torneo: ").strip().upper()
        if not pais:
            print("Error: El país no puede estar vacío.")
            continue

        if all(c.isalpha() or c.isspace() for c in pais):
            return pais
        else:
            print("Error: El país solo puede contener letras y espacios.")

def obtener_fecha_valida(prompt, fecha_referencia=None):
    while True:
        fecha_str = input(prompt).strip()
        try:
            fecha_obj = datetime.datetime.strptime(fecha_str, "%d/%m/%Y")
            if fecha_referencia and fecha_obj <= fecha_referencia:
                print(f"Error: La fecha final debe ser posterior a la fecha inicial ({fecha_referencia.strftime('%d/%m/%Y')}).")
                continue
            return fecha_str, fecha_obj
        except ValueError:
            print("Error: Formato de fecha no válido. Por favor, use DD/MM/YYYY.")

def agregar_equipos_a_torneo(nuevo_torneo_id):
    """Función para agregar equipos al torneo (cualquier país)"""
    equipos_seleccionados_ids = []
    
    while True:
        limpiar_pantalla()
        
        # Obtener todos los equipos disponibles
        todos_equipos = equipos_controller.obtenerTodosEquipos()
        
        # Filtrar equipos que no estén ya en este torneo
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
        print("-------------------------------")
        
        if equipos_seleccionados_ids:
            print(f"\nEquipos ya agregados: {len(equipos_seleccionados_ids)}")
            print("Equipos seleccionados:")
            for eq_id in equipos_seleccionados_ids:
                if eq_id in todos_equipos:
                    print(f"  - {todos_equipos[eq_id]['nombre']} ({todos_equipos[eq_id]['pais']})")
            print("-------------------------------")

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
        print("3. Ver detalles de un Torneo")
        print("4. Agregar equipos a un Torneo existente")
        print("5. Volver al Menú Principal")
        print("-------------------------------------")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            crearTorneo()
        elif opcion == "2":
            listarTorneos()
        elif opcion == "3":
            verDetallesTorneo()
        elif opcion == "4":
            agregarEquiposExistente()
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar_pantalla()

def crearTorneo():
    limpiar_pantalla()
    print("--- Crear Nuevo Torneo ---")
    
    torneos_existentes = cf.obtenerTorneos()
    
    # Generar ID único
    nuevo_id = cf.generateId("TR", list(torneos_existentes.keys()))

    nombre = obtener_nombre_torneo_validado(torneos_existentes)
    pais = obtener_pais_validado()
    fecha_inicial_str, fecha_inicial_obj = obtener_fecha_valida("Ingrese la fecha de inicio (DD/MM/YYYY): ")
    fecha_final_str, _ = obtener_fecha_valida("Ingrese la fecha de finalización (DD/MM/YYYY): ", fecha_referencia=fecha_inicial_obj)

    print("\n--- Agregando Equipos al Torneo ---")
    print("Nota: En los torneos pueden participar equipos de cualquier país")
    pausar_pantalla()
    
    ids_equipos_en_torneo = agregar_equipos_a_torneo(nuevo_id)

    if not ids_equipos_en_torneo:
        print("No se puede crear un torneo sin equipos.")
        pausar_pantalla()
        return

    nuevo_torneo = {
        "nombre": nombre,
        "pais": pais,
        "fecha_inicial": fecha_inicial_str,
        "fecha_final": fecha_final_str,
        "equipos_ids": ids_equipos_en_torneo,
        "fecha_registro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "activo": True
    }
    
    torneos_existentes[nuevo_id] = nuevo_torneo
    cf.guardarTorneos(torneos_existentes)
    
    print(f"\n¡Torneo '{nombre}' creado exitosamente con {len(ids_equipos_en_torneo)} equipos!")
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
                print(f"\nID: {torneo_id}")
                print(f"Nombre: {torneo['nombre']}")
                print(f"País: {torneo['pais']}")
                print(f"Duración: {torneo['fecha_inicial']} a {torneo['fecha_final']}")
                print(f"Equipos participantes: {len(torneo.get('equipos_ids', []))}")
                print(f"Registrado: {torneo.get('fecha_registro', 'N/A')}")
                
                # Mostrar países de los equipos participantes
                paises_participantes = set()
                for equipo_id in torneo.get('equipos_ids', []):
                    if equipo_id in equipos:
                        paises_participantes.add(equipos[equipo_id]['pais'])
                
                if paises_participantes:
                    print(f"Países participantes: {', '.join(sorted(paises_participantes))}")
                
                print("-" * 60)
    
    print("Presione Enter para continuar...")
    pausar_pantalla()

def verDetallesTorneo():
    limpiar_pantalla()
    print("--- Ver Detalles de Torneo ---")
    
    torneos = cf.obtenerTorneos()
    
    if not torneos:
        print("No hay torneos registrados.")
        pausar_pantalla()
        return
    
    # Mostrar torneos disponibles
    print("Torneos disponibles:")
    for torneo_id, torneo in torneos.items():
        if torneo.get("activo", True):
            print(f"ID: {torneo_id} - {torneo['nombre']} ({torneo['pais']})")
    
    torneo_id = input("\nIngrese el ID del torneo: ").strip()
    
    if torneo_id not in torneos:
        print("Torneo no encontrado.")
        pausar_pantalla()
        return
    
    torneo = torneos[torneo_id]
    equipos = cf.obtenerEquipos()
    
    print(f"\n--- Detalles de {torneo['nombre']} ---")
    print(f"ID: {torneo_id}")
    print(f"País: {torneo['pais']}")
    print(f"Fecha inicio: {torneo['fecha_inicial']}")
    print(f"Fecha fin: {torneo['fecha_final']}")
    print(f"Registrado: {torneo.get('fecha_registro', 'N/A')}")
    print(f"\nTotal de equipos: {len(torneo.get('equipos_ids', []))}")
    print("\nEquipos participantes:")
    
    # Agrupar equipos por país
    equipos_por_pais = {}
    for equipo_id in torneo.get('equipos_ids', []):
        if equipo_id in equipos:
            equipo = equipos[equipo_id]
            pais = equipo['pais']
            if pais not in equipos_por_pais:
                equipos_por_pais[pais] = []
            equipos_por_pais[pais].append(equipo)
        else:
            print(f"  - Equipo {equipo_id} (No encontrado)")
    
    for pais, lista_equipos in sorted(equipos_por_pais.items()):
        print(f"\n  {pais}:")
        for equipo in lista_equipos:
            print(f"    - {equipo['nombre']} ({equipo['ciudad']})")
    
    pausar_pantalla()

def agregarEquiposExistente():
    limpiar_pantalla()
    print("--- Agregar Equipos a Torneo Existente ---")
    
    torneos = cf.obtenerTorneos()
    
    if not torneos:
        print("No hay torneos registrados.")
        pausar_pantalla()
        return
    
    # Mostrar torneos disponibles
    print("Torneos disponibles:")
    for torneo_id, torneo in torneos.items():
        if torneo.get("activo", True):
            print(f"ID: {torneo_id} - {torneo['nombre']} ({len(torneo.get('equipos_ids', []))} equipos)")
    
    torneo_id = input("\nIngrese el ID del torneo: ").strip()
    
    if torneo_id not in torneos:
        print("Torneo no encontrado.")
        pausar_pantalla()
        return
    
    torneo = torneos[torneo_id]
    equipos_actuales = torneo.get('equipos_ids', [])
    
    # Obtener equipos disponibles (que no estén ya en el torneo)
    todos_equipos = equipos_controller.obtenerTodosEquipos()
    equipos_disponibles = {id_eq: eq for id_eq, eq in todos_equipos.items() 
                          if id_eq not in equipos_actuales}
    
    if not equipos_disponibles:
        print("No hay equipos disponibles para agregar a este torneo.")
        pausar_pantalla()
        return
    
    nuevos_equipos = []
    
    while True:
        limpiar_pantalla()
        print(f"--- Agregar Equipos a '{torneo['nombre']}' ---")
        print(f"Equipos actuales en el torneo: {len(equipos_actuales)}")
        
        if nuevos_equipos:
            print(f"Equipos a agregar: {len(nuevos_equipos)}")
        
        print("\nEquipos Disponibles:")
        equipos_mostrar = {id_eq: eq for id_eq, eq in equipos_disponibles.items() 
                          if id_eq not in nuevos_equipos}
        
        if not equipos_mostrar:
            print("No hay más equipos disponibles.")
            break
            
        for id_equipo, datos_equipo in equipos_mostrar.items():
            print(f"ID: {id_equipo} - {datos_equipo['nombre']} - {datos_equipo['pais']} ({datos_equipo['ciudad']})")
        
        respuesta = input("\nIngrese el ID del equipo a agregar (o 'fin' para terminar): ").strip()
        
        if respuesta.lower() == 'fin':
            break
        
        if respuesta in equipos_mostrar:
            nuevos_equipos.append(respuesta)
            equipo_agregado = equipos_mostrar[respuesta]
            print(f"¡Equipo '{equipo_agregado['nombre']}' será agregado al torneo!")
            pausar_pantalla()
        else:
            print("Error: ID de equipo no válido.")
            pausar_pantalla()
    
    if nuevos_equipos:
        torneo['equipos_ids'].extend(nuevos_equipos)
        torneos[torneo_id] = torneo
        cf.guardarTorneos(torneos)
        print(f"\n¡Se agregaron {len(nuevos_equipos)} equipos al torneo '{torneo['nombre']}'!")
    else:
        print("No se agregaron equipos al torneo.")
    
    pausar_pantalla()

def obtenerTorneoPorId(torneo_id: str):
    """Función auxiliar para obtener un torneo por ID"""
    torneos = cf.obtenerTorneos()
    return torneos.get(torneo_id)

def obtenerTorneosPorPais(pais: str):
    """Función auxiliar para obtener torneos por país"""
    torneos = cf.obtenerTorneos()
    return {id_tr: tr for id_tr, tr in torneos.items() 
            if tr.get("pais", "").upper() == pais.upper() and tr.get("activo", True)}

def obtenerTodosTorneos():
    """Función auxiliar para obtener todos los torneos activos"""
    torneos = cf.obtenerTorneos()
    return {id_tr: tr for id_tr, tr in torneos.items() if tr.get("activo", True)}