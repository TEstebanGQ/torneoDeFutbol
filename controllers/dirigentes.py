import os
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import utils.corefiles as cf
from config import DIRIGENTES_FILE
from config import CARGOS_DIRIGENTES

def obtener_nombre_validado():
    
    while True:
        nombre = input("Ingrese el nombre completo del dirigente: ").strip().upper()
        if nombre and all(c.isalpha() or c.isspace() for c in nombre):
            return nombre
        else:
            print("Error: El nombre solo puede contener letras y espacios.")

def obtener_cargo_validado():
    while True:
        limpiar_pantalla()
        print("    Cargos Disponibles para Dirigentes    ")
        for i, cargo in enumerate(CARGOS_DIRIGENTES, 1):
            print(f"{i:2d}. {cargo}")
        
        
        try:
            opcion = int(input(f"Seleccione el cargo (1-{len(CARGOS_DIRIGENTES)}): "))
            if 1 <= opcion <= len(CARGOS_DIRIGENTES):
                return CARGOS_DIRIGENTES[opcion - 1]
            else:
                print(f"Error: Seleccione un número entre 1 y {len(CARGOS_DIRIGENTES)}.")
                pausar_pantalla()
        except ValueError:
            print("Error: Debe ingresar un número válido.")
            pausar_pantalla()

def mostrar_ligas_y_torneos():
    ligas = cf.obtenerLigas()
    torneos = cf.obtenerTorneos()
    
    print("=" * 80)
    print("LIGAS Y TORNEOS DISPONIBLES")
    print("=" * 80)
    
    ligas_activas = {lid: liga for lid, liga in ligas.items() if liga.get("activa", True)}
    if ligas_activas:
        print("LIGAS DISPONIBLES:")
        print("-" * 50)
        print(f"{'ID':<5} {'NOMBRE':<25} {'PAÍS':<15} {'EQUIPOS':<8}")
        print("-" * 50)
        for liga_id, liga in ligas_activas.items():
            num_equipos = len(liga.get('equipos_ids', []))
            print(f"{liga_id:<5} {liga['nombre'][:24]:<25} {liga['pais'][:14]:<15} {num_equipos:<8}")
        print("-" * 50)
    else:
        print("No hay ligas disponibles.")
    
    print()
    
    torneos_activos = {tid: torneo for tid, torneo in torneos.items() if torneo.get("activo", True)}
    if torneos_activos:
        print("TORNEOS DISPONIBLES:")
        print("-" * 60)
        print(f"{'ID':<5} {'NOMBRE':<25} {'PAÍS ORGANIZADOR':<20} {'EQUIPOS':<8}")
        print("-" * 60)
        for torneo_id, torneo in torneos_activos.items():
            num_equipos = len(torneo.get('equipos_ids', []))
            pais_org = torneo.get('pais_organizador', torneo.get('pais', 'N/A'))
            print(f"{torneo_id:<5} {torneo['nombre'][:24]:<25} {pais_org[:19]:<20} {num_equipos:<8}")
        print("-" * 60)
    else:
        print("No hay torneos disponibles.")
    
    print("=" * 80)

def seleccionar_liga_o_torneo():
    ligas = cf.obtenerLigas()
    torneos = cf.obtenerTorneos()
    
    ligasactivas = {lid: liga for lid, liga in ligas.items() if liga.get("activa", True)}
    torneosActivos = {tid: torneo for tid, torneo in torneos.items() if torneo.get("activo", True)}
    
    if not ligasactivas and not torneosActivos:
        print("No hay ligas ni torneos disponibles.")
        return None, None, None
    
    while True:
        print("¿A qué tipo de competición pertenece el dirigente?")
        print("1. Liga")
        print("2. Torneo")
        
        try:
            tipoOpcion = int(input("Seleccione el tipo (1-2): "))
            
            if tipoOpcion == 1:  
                if not ligasactivas:
                    print("No hay ligas disponibles.")
                    continue
                
                while True:
                    compId = input("Ingrese el ID de la liga: ").strip()
                    if compId in ligasactivas:
                        return "Liga", compId, ligasactivas[compId]['nombre']
                    else:
                        print("Error: ID de liga no válido.")
            elif tipoOpcion == 2: 
                if not torneosActivos:
                    print("No hay torneos disponibles.")
                    continue
                
                while True:
                    compId = input("Ingrese el ID del torneo: ").strip()
                    if compId in torneosActivos:
                        return "Torneo", compId, torneosActivos[compId]['nombre']
                    else:
                        print("Error: ID de torneo no válido.")
            
            else:
                print("Error: Seleccione 1 o 2.")
                
        except ValueError:
            print("Error: Debe ingresar un número válido.")

def subMenuDirigentes():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Gestión de Dirigentes ---")
        print("1. Registrar un nuevo dirigente")
        print("2. Listar dirigentes registrados")
        print("3. Volver al Menú Principal")
        print("---------------------------------------")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            registrar_dirigente()
        elif opcion == "2":
            listar_dirigentes()
        elif opcion == "3":
            break
        else:
            print("Opción no válida. Intente nuevamente.")
            pausar_pantalla()

def registrar_dirigente():
    limpiar_pantalla()
    print("    Registrar Nuevo Dirigente    ")
    
    dirigentes = cf.readJson(DIRIGENTES_FILE)
    nuevo_id = cf.generateId(list(dirigentes.keys()))
    nombre = obtener_nombre_validado()
    cargo = obtener_cargo_validado()
    limpiar_pantalla()
    print("    Asignar Dirigente a Liga/Torneo    ")
    mostrar_ligas_y_torneos()
    tipoCompeticion, competicionId, competicionNombre = seleccionar_liga_o_torneo()
    
    if not tipoCompeticion:
        print("No se puede registrar el dirigente sin asignarlo a una competición.")
        pausar_pantalla()
        return

    nuevoDirigente = {
        "nombre": nombre,
        "cargo": cargo,
        "tipo_competicion": tipoCompeticion,
        "competicion_id": competicionId,
        "competicion_nombre": competicionNombre,
        "activo": True
    }
    
    dirigentes[nuevo_id] = nuevoDirigente
    cf.writeJson(dirigentes, DIRIGENTES_FILE)
    print("="*60)
    print("¡DIRIGENTE REGISTRADO EXITOSAMENTE!")
    print("="*60)
    print(f"ID: {nuevo_id}")
    print(f"Nombre: {nombre}")
    print(f"Cargo: {cargo}")
    print(f"Asignado a: {tipoCompeticion} - {competicionNombre}")
    print("="*60)
    pausar_pantalla()

def listar_dirigentes():
    limpiar_pantalla()
    print("    Lista de Dirigentes Registrados   ")
    
    dirigentes = cf.readJson(DIRIGENTES_FILE)
    
    if not dirigentes:
        print("No hay dirigentes registrados.")
    else:
        dirigentesActivos = {did: d for did, d in dirigentes.items() if d.get("activo", True)}
        
        if not dirigentesActivos:
            print("No hay dirigentes activos.")
        else:
            print(f"Total de dirigentes: {len(dirigentesActivos)}")
            print("=" * 90)
            dirigentesligas = {}
            dirigentesTorneos = {}
            
            for dirigenteid, dirigente in dirigentesActivos.items():
                if dirigente.get('tipo_competicion') == 'Liga':
                    comp_id = dirigente.get('competicion_id')
                    if comp_id not in dirigentesligas:
                        dirigentesligas[comp_id] = []
                    dirigentesligas[comp_id].append((dirigenteid, dirigente))
                elif dirigente.get('tipo_competicion') == 'Torneo':
                    comp_id = dirigente.get('competicion_id')
                    if comp_id not in dirigentesTorneos:
                        dirigentesTorneos[comp_id] = []
                    dirigentesTorneos[comp_id].append((dirigenteid, dirigente))
            if dirigentesligas:
                print("DIRIGENTES DE LIGAS")
                print("-" * 90)
                for liga_id, listaDirigentess in dirigentesligas.items():
                    ligaNombres = listaDirigentess[0][1].get('competicion_nombre', 'Liga Desconocida')
                    print(f"Liga: {ligaNombres} (ID: {liga_id})")
                    print("-" * 70)
                    print(f"{'ID':<5} {'NOMBRE':<25} {'CARGO':<35}")
                    print("-" * 70)
                    
                    for dirigenteid, dirigente in listaDirigentess:
                        print(f"{dirigenteid:<5} {dirigente['nombre'][:24]:<25} {dirigente['cargo'][:34]:<35}")
                    print("-" * 70)
            if dirigentesTorneos:
                print("DIRIGENTES DE TORNEOS")
                print("-" * 90)
                for torneo_id, listaDirigentess in dirigentesTorneos.items():
                    torneo_nombre = listaDirigentess[0][1].get('competicion_nombre', 'Torneo Desconocido')
                    print(f"Torneo: {torneo_nombre} (ID: {torneo_id})")
                    print("-" * 70)
                    print(f"{'ID':<5} {'NOMBRE':<25} {'CARGO':<35}")
                    print("-" * 70)
                    
                    for dirigenteid, dirigente in listaDirigentess:
                        print(f"{dirigenteid:<5} {dirigente['nombre'][:24]:<25} {dirigente['cargo'][:34]:<35}")
                    print("-" * 70)
    
    print("  Presione Enter para continuar...")
    pausar_pantalla()

def obtener_dirigente_por_id(dirigente_id: str):
    dirigentes = cf.readJson(DIRIGENTES_FILE)
    return dirigentes.get(dirigente_id)

def obtener_dirigentes_por_competicion(tipo_competicion: str, competicion_id: str):
    dirigentes = cf.readJson(DIRIGENTES_FILE)
    return {did: d for did, d in dirigentes.items() 
            if d.get("tipo_competicion") == tipo_competicion 
            and d.get("competicion_id") == competicion_id 
            and d.get("activo", True)}

def obtener_todos_dirigentes():
    dirigentes = cf.readJson(DIRIGENTES_FILE)
    return {did: d for did, d in dirigentes.items() if d.get("activo", True)}

def contar_dirigentes_por_cargo():
    dirigentes = cf.readJson(DIRIGENTES_FILE)
    dirigentes_activos = {did: d for did, d in dirigentes.items() if d.get("activo", True)}
    
    conteoCargos = {}
    for dirigente in dirigentes_activos.values():
        cargo = dirigente.get('cargo', 'Sin cargo')
        conteoCargos[cargo] = conteoCargos.get(cargo, 0) + 1
    
    return conteoCargos