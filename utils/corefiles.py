import json
import os
from typing import Dict, List, Optional
from config import *

def readJson(file_path: str = None) -> Dict:
    if file_path is None:
        file_path = DB_FILE
    
    try:
        with open(file_path, "r", encoding="utf-8") as cf:
            return json.load(cf)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def writeJson(data: Dict, file_path: str = None) -> None:
    if file_path is None:
        file_path = DB_FILE

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as cf:
        json.dump(data, cf, indent=4, ensure_ascii=False)

def updateJson(data: Dict, path: Optional[List[str]] = None, file_path: str = None) -> None:
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
    if existing_ids is None:
        existing_ids = []
    
    numeros_existentes = []
    for id_str in existing_ids:
        try:
            numero = int(''.join(filter(str.isdigit, str(id_str))))
            numeros_existentes.append(numero)
        except ValueError:
            continue
    
    if numeros_existentes:
        return str(max(numeros_existentes) + 1)
    else:
        return "1"

def obtenerEquipos() -> Dict:
    return readJson(EQUIPOS_FILE)

def obtenerJugadores() -> Dict:
    return readJson(JUGADORES_FILE)

def obtenerLigas() -> Dict:
    return readJson(LIGAS_FILE)

def obtenerTorneos() -> Dict:
    return readJson(TORNEOS_FILE)

def obtenerTransferencias() -> Dict:
    return readJson(TRANSFERENCIAS_FILE)

def guardarEquipos(equipos: Dict) -> None:
    writeJson(equipos, EQUIPOS_FILE)

def guardarJugadores(jugadores: Dict) -> None:
    writeJson(jugadores, JUGADORES_FILE)

def guardarLigas(ligas: Dict) -> None:
    writeJson(ligas, LIGAS_FILE)

def guardarTorneos(torneos: Dict) -> None:
    writeJson(torneos, TORNEOS_FILE)

def guardarTransferencias(transferencias: Dict) -> None:
    writeJson(transferencias, TRANSFERENCIAS_FILE)