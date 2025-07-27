
import utils.screenControllers as screen
from utils.screenControllers import pausar_pantalla as pausar
import os
import json

NOMBRE_CARPETA_DATA = "data"
NOMBRE_ARCHIVO_JSON = "equipos.json"
RUTA_ARCHIVO_JSON = os.path.join(NOMBRE_CARPETA_DATA, NOMBRE_ARCHIVO_JSON)

def cargar_datos():
    os.makedirs(NOMBRE_CARPETA_DATA, exist_ok=True)
    try:
        with open(RUTA_ARCHIVO_JSON, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_datos(datos):
    with open(RUTA_ARCHIVO_JSON, 'w') as f:
        json.dump(datos, f, indent=4)

lista_de_equipos = cargar_datos()

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
    
    while True:
        if not lista_de_equipos:
            nuevo_id = 1
        else:
            max_id = max(equipo["id"] for equipo in lista_de_equipos)
            nuevo_id = max_id + 1

        nombre = input("Ingrese el nombre del equipo: ").strip()
        if not nombre:
            print("Error: El nombre del equipo no puede estar vacío.")
            continue

        if nombre.lower() in [equipo["nombre"].lower() for equipo in lista_de_equipos]:
            print(f"Error: El equipo '{nombre}' ya se encuentra registrado.")
            pausar()
            continue

        fecha_fundacion = input("Ingrese la fecha de fundación (YYYY-MM-DD): ").strip()
        pais = input("Ingrese el país de origen del equipo: ").strip()
        

        nuevo_equipo = {
            "id": nuevo_id,
            "nombre": nombre,
            "fecha_fundacion": fecha_fundacion,
            "pais": pais,
            "liga_id": None
        }

        lista_de_equipos.append(nuevo_equipo)
        guardar_datos(lista_de_equipos)
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

    if not lista_de_equipos:
        print("Aún no hay equipos registrados.")
    else:
        for equipo in lista_de_equipos:
            print(f"  ID: {equipo['id']}")
            print(f"  Nombre: {equipo['nombre']}")
            print(f"  País: {equipo['pais']}")
            print(f"  Fundación: {equipo['fecha_fundacion']}")
            print(f"  Liga ID: {equipo['liga_id']}")
            print("-" * 20)
    
    print("Presione Enter para continuar...")
    pausar()

