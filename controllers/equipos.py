import utils.screenControllers as screen
from utils.screenControllers import pausar_pantalla as pausar
import utils.corefiles as cf
from config import EQUIPOS_FILE
from datetime import datetime

def subMenuEquipos():
    while True:
        screen.limpiar_pantalla()
        print("--- Submenú de Gestión de Equipos ---")
        print("1. Registrar un nuevo equipo")
        print("2. Listar todos los equipos")
        print("3. Buscar equipo por ID")
        print("4. Volver al menú principal")
        print("-------------------------------------")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crearEquipo()
        elif opcion == '2':
            listarEquipos()
        elif opcion == '3':
            buscarEquipoPorId()
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar() 

def crearEquipo():
    screen.limpiar_pantalla()
    print("--- Registro de Nuevos Equipos ---")
    
    equipos = cf.obtenerEquipos()
    
    while True:
        # Generar ID único
        nuevo_id = cf.generateId("EQ", list(equipos.keys()))

        nombre = input("Ingrese el nombre del equipo: ").strip().upper()
        if not nombre:
            print("Error: El nombre del equipo no puede estar vacío.")
            continue

        # Verificar si ya existe un equipo con ese nombre
        nombres_existentes = [eq["nombre"].upper() for eq in equipos.values()]
        if nombre in nombres_existentes:
            print(f"Error: El equipo '{nombre}' ya se encuentra registrado.")
            pausar()
            continue

        fecha_fundacion = input("Ingrese la fecha de fundación (DD/MM/YYYY): ").strip()
        pais = input("Ingrese el país de origen del equipo: ").strip().upper()
        ciudad = input("Ingrese la ciudad del equipo: ").strip().upper()
        estadio = input("Ingrese el nombre del estadio: ").strip().upper()

        nuevo_equipo = {
            "nombre": nombre,
            "pais": pais,
            "fecha_fundacion": fecha_fundacion,
            "ciudad": ciudad,
            "estadio": estadio,
            "fecha_registro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "activo": True
        }

        equipos[nuevo_id] = nuevo_equipo
        cf.guardarEquipos(equipos)
        print(f"¡Equipo '{nombre}' (ID: {nuevo_id}) registrado y guardado con éxito!")

        while True:
            seguir = input("\n¿Desea registrar otro equipo? (Si/No): ").lower()
            if seguir in ['si', 'no']:
                break
            else:
                print("Respuesta no válida. Por favor, ingrese 'Si' o 'No'.")
        
        if seguir == 'no':
            break
        
        screen.limpiar_pantalla()
        print("--- Registro de Nuevos Equipos ---")

def listarEquipos():
    screen.limpiar_pantalla()
    print("--- Lista de Equipos Registrados ---")

    equipos = cf.obtenerEquipos()
    
    if not equipos:
        print("Aún no hay equipos registrados.")
    else:
        for equipo_id, equipo in equipos.items():
            if equipo.get("activo", True):  # Solo mostrar equipos activos
                print(f"  ID: {equipo_id}")
                print(f"  Nombre: {equipo['nombre']}")
                print(f"  País: {equipo['pais']}")
                print(f"  Ciudad: {equipo['ciudad']}")
                print(f"  Estadio: {equipo['estadio']}")
                print(f"  Fundación: {equipo['fecha_fundacion']}")
                print(f"  Registrado: {equipo['fecha_registro']}")
                print("-" * 30)
    
    print("Presione Enter para continuar...")
    pausar()

def buscarEquipoPorId():
    screen.limpiar_pantalla()
    print("--- Buscar Equipo por ID ---")
    
    equipos = cf.obtenerEquipos()
    
    if not equipos:
        print("No hay equipos registrados.")
        pausar()
        return
    
    equipo_id = input("Ingrese el ID del equipo a buscar: ").strip()
    
    if equipo_id in equipos:
        equipo = equipos[equipo_id]
        if equipo.get("activo", True):
            print(f"\n--- Información del Equipo ---")
            print(f"ID: {equipo_id}")
            print(f"Nombre: {equipo['nombre']}")
            print(f"País: {equipo['pais']}")
            print(f"Ciudad: {equipo['ciudad']}")
            print(f"Estadio: {equipo['estadio']}")
            print(f"Fundación: {equipo['fecha_fundacion']}")
            print(f"Registrado: {equipo['fecha_registro']}")
        else:
            print("El equipo encontrado está inactivo.")
    else:
        print("No se encontró un equipo con ese ID.")
    
    pausar()

def obtenerEquipoPorId(equipo_id: str):
    """Función auxiliar para obtener un equipo por ID"""
    equipos = cf.obtenerEquipos()
    return equipos.get(equipo_id)

def obtenerEquiposPorPais(pais: str):
    """Función auxiliar para obtener equipos por país"""
    equipos = cf.obtenerEquipos()
    return {id_eq: eq for id_eq, eq in equipos.items() 
            if eq.get("pais", "").upper() == pais.upper() and eq.get("activo", True)}

def obtenerTodosEquipos():
    """Función auxiliar para obtener todos los equipos activos"""
    equipos = cf.obtenerEquipos()
    return {id_eq: eq for id_eq, eq in equipos.items() if eq.get("activo", True)}