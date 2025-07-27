import os
import json
import datetime
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
        
        # Verificar si ya existe una liga con ese nombre
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

def agregar_equipos_a_liga(nueva_liga_id, pais_de_la_liga):
    """Función corregida para agregar equipos de un país específico a la liga"""
    equipos_seleccionados_ids = []
    
    while True:
        limpiar_pantalla()
        
        # Obtener equipos disponibles del país especificado
        equipos_del_pais = equipos_controller.obtenerEquiposPorPais(pais_de_la_liga)
        
        # Filtrar equipos que no tengan liga asignada
        equipos_disponibles = {}
        for id_equipo, datos_equipo in equipos_del_pais.items():
            # Verificar si el equipo ya está en alguna liga
            ligas_existentes = cf.obtenerLigas()
            equipo_ya_asignado = False
            
            for liga in ligas_existentes.values():
                if id_equipo in liga.get("equipos_ids", []):
                    equipo_ya_asignado = True
                    break
            
            if not equipo_ya_asignado:
                equipos_disponibles[id_equipo] = datos_equipo

        print(f"--- Agregar Equipos de '{pais_de_la_liga}' a la Liga ---")
        
        if not equipos_disponibles:
            print(f"No hay equipos disponibles de {pais_de_la_liga} para agregar a la liga.")
            print("Todos los equipos de este país ya están asignados a otras ligas.")
            pausar_pantalla()
            break

        print("Equipos Disponibles:")
        for id_equipo, datos_equipo in equipos_disponibles.items():
            print(f"ID: {id_equipo} - Nombre: {datos_equipo['nombre']} - Ciudad: {datos_equipo['ciudad']}")
        print("-------------------------------")

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
        print("3. Ver detalles de una Liga")
        print("4. Volver al Menú Principal")
        print("-----------------------------------")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            crearLiga()
        elif opcion == "2":
            listarLigas()
        elif opcion == "3":
            verDetallesLiga()
        elif opcion == "4":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar_pantalla()

def crearLiga():
    limpiar_pantalla()
    print("--- Crear Nueva Liga ---")
    
    ligas_existentes = cf.obtenerLigas()
    
    # Generar ID único
    nuevo_id = cf.generateId("LG", list(ligas_existentes.keys()))

    nombre = obtener_nombre_liga_validado(ligas_existentes)
    pais = obtener_pais_validado()
    fecha_inicial_str, fecha_inicial_obj = obtener_fecha_valida("Ingrese la fecha de inicio (DD/MM/YYYY): ")
    fecha_final_str, _ = obtener_fecha_valida("Ingrese la fecha de finalización (DD/MM/YYYY): ", fecha_referencia=fecha_inicial_obj)

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
        "fecha_registro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "activa": True
    }
    
    ligas_existentes[nuevo_id] = nueva_liga
    cf.guardarLigas(ligas_existentes)
    
    print(f"\n¡Liga '{nombre}' creada exitosamente con {len(ids_equipos_en_liga)} equipos!")
    pausar_pantalla()

def listarLigas():
    limpiar_pantalla()
    print("--- Listado de Ligas Registradas ---")
    
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
                print(f"Registrada: {liga.get('fecha_registro', 'N/A')}")
                print("-" * 50)
    
    print("Presione Enter para continuar...")
    pausar_pantalla()

def verDetallesLiga():
    limpiar_pantalla()
    print("--- Ver Detalles de Liga ---")
    
    ligas = cf.obtenerLigas()
    
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
    equipos = cf.obtenerEquipos()
    
    print(f"\n--- Detalles de {liga['nombre']} ---")
    print(f"ID: {liga_id}")
    print(f"País: {liga['pais']}")
    print(f"Fecha inicio: {liga['fecha_inicial']}")
    print(f"Fecha fin: {liga['fecha_final']}")
    print(f"Registrada: {liga.get('fecha_registro', 'N/A')}")
    print("\nEquipos participantes:")
    
    for equipo_id in liga.get('equipos_ids', []):
        if equipo_id in equipos:
            equipo = equipos[equipo_id]
            print(f"  - {equipo['nombre']} ({equipo['ciudad']})")
        else:
            print(f"  - Equipo {equipo_id} (No encontrado)")
    
    pausar_pantalla()