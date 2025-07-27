import utils.screenControllers as screen
from utils.screenControllers import pausar_pantalla as pausar
import utils.corefiles as cf
from config import EQUIPOS_FILE

def subMenuEquipos():
    while True:
        screen.limpiar_pantalla()
        print("--- Submenú de Gestión de Equipos ---")
        print("1. Registrar un nuevo equipo")
        print("2. Listar todos los equipos")
        print("3. Volver al menú principal")
        print("-------------------------------------")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crearEquipo()
        elif opcion == '2':
            listarEquipos()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar() 

def crearEquipo():
    screen.limpiar_pantalla()
    print("--- Registro de Nuevos Equipos ---")
    
    equipos = cf.obtenerEquipos()
    
    while True:
        # Generar ID único numérico ascendente
        nuevo_id = cf.generateId(list(equipos.keys()))

        nombre = input("Ingrese el nombre del equipo: ").strip().upper()
        if not nombre:
            print("Error: El nombre del equipo no puede estar vacío.")
            continue
        nombres_existentes = [eq["nombre"].upper() for eq in equipos.values()]
        if nombre in nombres_existentes:
            print(f"Error: El equipo '{nombre}' ya se encuentra registrado.")
            pausar()
            continue

        fecha_fundacion = input("Ingrese la fecha de fundación (DD-MM-AAAA): ").strip()
        if not validar_formato_fecha(fecha_fundacion):
            print("Error: Formato de fecha inválido. Use DD-MM-AAAA")
            continue

        pais = input("Ingrese el país de origen del equipo: ").strip().upper()
        ciudad = input("Ingrese la ciudad del equipo: ").strip().upper()

        nuevo_equipo = {
            "nombre": nombre,
            "pais": pais,
            "fecha_fundacion": fecha_fundacion,
            "ciudad": ciudad,
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
                print(f"  Fundación: {equipo['fecha_fundacion']}")
                # Mostrar liga si está asignada
                liga_id = equipo.get('liga_id')
                if liga_id:
                    print(f"  Liga ID: {liga_id}")
                print("-" * 30)
    
    print("Presione Enter para continuar...")
    pausar()

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