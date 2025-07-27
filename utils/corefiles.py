import json
import os
from typing import Dict, List, Optional, Any
from config import *

def readJson(file_path: str = None) -> Dict:
    """Lee un archivo JSON y retorna su contenido como diccionario"""
    if file_path is None:
        file_path = DB_FILE
    
    try:
        with open(file_path, "r", encoding="utf-8") as cf:
            return json.load(cf)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def writeJson(data: Dict, file_path: str = None) -> None:
    """Escribe datos en un archivo JSON"""
    if file_path is None:
        file_path = DB_FILE
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as cf:
        json.dump(data, cf, indent=4, ensure_ascii=False)

def updateJson(data: Dict, path: Optional[List[str]] = None, file_path: str = None) -> None:
    """Actualiza datos en un archivo JSON"""
    currentData = readJson(file_path)

    if not path:
        currentData.update(data)
    else:
        current = currentData
        for key in path[:-1]:
            current = current.setdefault(key, {})
        if path:
            current.setdefault(path[-1], {}).update(data)
    
    writeJson(currentData, file_path)

def deleteJson(path: List[str], file_path: str = None) -> bool:
    """Elimina un elemento del archivo JSON"""
    data = readJson(file_path)
    if not data:
        return False
    
    current = data
    for key in path[:-1]:
        if key not in current:
            return False
        current = current[key]
    
    if path and path[-1] in current:
        del current[path[-1]]
        writeJson(data, file_path)
        return True
    return False

def initializeJson(file_path: str = None, initialStructure: Dict = None) -> None:
    """Inicializa un archivo JSON con una estructura inicial"""
    if file_path is None:
        file_path = DB_FILE
    if initialStructure is None:
        initialStructure = INITIAL_DB_STRUCTURE
    
    if not os.path.isfile(file_path):
        writeJson(initialStructure, file_path)
    else:
        currentData = readJson(file_path)
        for key, value in initialStructure.items():
            if key not in currentData:
                currentData[key] = value
        writeJson(currentData, file_path)

def generateId(existing_ids: List[str] = None) -> str:
    """Genera un ID numérico ascendente"""
    if existing_ids is None:
        existing_ids = []
    
    # Extraer números de los IDs existentes y encontrar el máximo
    numeros_existentes = []
    for id_str in existing_ids:
        try:
            # Extraer solo números del ID
            numero = int(''.join(filter(str.isdigit, str(id_str))))
            numeros_existentes.append(numero)
        except ValueError:
            continue
    
    if numeros_existentes:
        return str(max(numeros_existentes) + 1)
    else:
        return "1"

# Funciones específicas para cada entidad
def obtenerEquipos() -> Dict:
    """Obtiene todos los equipos"""
    return readJson(EQUIPOS_FILE)

def obtenerJugadores() -> Dict:
    """Obtiene todos los jugadores"""
    return readJson(JUGADORES_FILE)

def obtenerLigas() -> Dict:
    """Obtiene todas las ligas"""
    return readJson(LIGAS_FILE)

def obtenerTorneos() -> Dict:
    """Obtiene todos los torneos"""
    return readJson(TORNEOS_FILE)

def obtenerTransferencias() -> Dict:
    """Obtiene todas las transferencias"""
    return readJson(TRANSFERENCIAS_FILE)

def guardarEquipos(equipos: Dict) -> None:
    """Guarda los equipos"""
    writeJson(equipos, EQUIPOS_FILE)

def guardarJugadores(jugadores: Dict) -> None:
    """Guarda los jugadores"""
    writeJson(jugadores, JUGADORES_FILE)

def guardarLigas(ligas: Dict) -> None:
    """Guarda las ligas"""
    writeJson(ligas, LIGAS_FILE)

def guardarTorneos(torneos: Dict) -> None:
    """Guarda los torneos"""
    writeJson(torneos, TORNEOS_FILE)

def guardarTransferencias(transferencias: Dict) -> None:
    """Guarda las transferencias"""
    writeJson(transferencias, TRANSFERENCIAS_FILE)