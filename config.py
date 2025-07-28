import os

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "database.json")
EQUIPOS_FILE = os.path.join(DATA_DIR, "equipos.json")
JUGADORES_FILE = os.path.join(DATA_DIR, "jugadores.json")
LIGAS_FILE = os.path.join(DATA_DIR, "ligas.json")
TORNEOS_FILE = os.path.join(DATA_DIR, "torneos.json")
TRANSFERENCIAS_FILE = os.path.join(DATA_DIR, "transferencias.json")
DIRIGENTES_FILE = os.path.join(DATA_DIR, "dirigentes.json")
PARTIDOS_FILE = os.path.join(DATA_DIR, "partidos.json")


INITIAL_DB_STRUCTURE = {
    "equipos": {},
    "jugadores": {},
    "ligas": {},
    "torneos": {},
    "transferencias": {},
    "dirigentes": {},
    "partidos": {}
}

MAX_JUGADORES_POR_EQUIPO = 25
MIN_JUGADORES_POR_EQUIPO = 11
MAX_EQUIPOS_POR_LIGA = 20
MIN_EQUIPOS_POR_LIGA = 4
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
CARGOS_DIRIGENTES = [
    "Presidente",
    "Vicepresidente", 
    "Director deportivo",
    "Gerente general",
    "Secretario general",
    "Tesorero",
    "Director de operaciones",
    "Director de marketing",
    "Director de comunicación",
    "Director de relaciones institucionales",
    "Director de cantera o formación",
    "Jefe de scouting",
    "Delegado del equipo",
    "Asesor jurídico",
    "Encargado de seguridad",
    "Coordinador deportivo",
    "Representante ante la liga o federación",
    "Director financiero",
    "Responsable de infraestructura",
    "Responsable de logística"
]