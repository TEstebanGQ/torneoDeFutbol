import os

# Configuración de rutas de archivos
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "database.json")

# Rutas específicas para cada entidad
EQUIPOS_FILE = os.path.join(DATA_DIR, "equipos.json")
JUGADORES_FILE = os.path.join(DATA_DIR, "jugadores.json")
LIGAS_FILE = os.path.join(DATA_DIR, "ligas.json")
TORNEOS_FILE = os.path.join(DATA_DIR, "torneos.json")
TRANSFERENCIAS_FILE = os.path.join(DATA_DIR, "transferencias.json")
DIRIGENTES_FILE = os.path.join(DATA_DIR, "dirigentes.json")
PARTIDOS_FILE = os.path.join(DATA_DIR, "partidos.json")

# Estructura inicial de la base de datos
INITIAL_DB_STRUCTURE = {
    "equipos": {},
    "jugadores": {},
    "ligas": {},
    "torneos": {},
    "transferencias": {},
    "dirigentes": {},
    "partidos": {}
}

# Configuraciones generales
MAX_JUGADORES_POR_EQUIPO = 25
MIN_JUGADORES_POR_EQUIPO = 11
MAX_EQUIPOS_POR_LIGA = 20
MIN_EQUIPOS_POR_LIGA = 4

# Posiciones válidas para jugadores
POSICIONES_VALIDAS = [
    "Portero",
    "Defensa Central Derecho",
    "Defensa Central Izquierdo", 
    "Defensa Central",
    "Lateral Derecho",
    "Lateral Izquierdo",
    "Líbero",
    "Centrocampista Defensivo",
    "Centrocampista Central",
    "Centrocampista Ofensivo",
    "Centrocampista Derecho",
    "Centrocampista Izquierdo",
    "Extremo Derecho",
    "Extremo Izquierdo",
    "Delantero Centro"
]

# Tipos de transferencia
TIPOS_TRANSFERENCIA = [
    "Transferencia definitiva",
    "Cesión o préstamo", 
    "Transferencia libre",
    "Cláusula de rescisión",
    "Intercambio de jugadores",
    "Transferencias de juveniles",
    "Co-propiedad",
    "Transferencia por subasta o tribunal"
]