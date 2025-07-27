import os
import sys
import controllers.equipos as equiposs
import controllers.jugadores as jugadoress
import controllers.transferencias as transferenciass
import controllers.ligas as ligass
import controllers.torneos as torneoss
import controllers.estadisticas as estadisticass
from utils.screenControllers import limpiar_pantalla
import utils.corefiles as cf
from config import *

class AnsiColors:
    RESET = '\033[0m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

def _get_key_windows():
    import msvcrt
    key = msvcrt.getch()
    if key in b'\x00\xe0':
        key = msvcrt.getch()
        if key == b'H': return 'up'
        if key == b'P': return 'down'
    elif key == b'\r':
        return 'enter'
    return None

def _get_key_unix():
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(sys.stdin.fileno())
        char = sys.stdin.read(1)
        if char == '\x1b':
            sequence = sys.stdin.read(2)
            if sequence == '[A': return 'up'
            if sequence == '[B': return 'down'
        elif char in ('\n', '\r'):
            return 'enter'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

def interactive_menu_colored(options):
    current_option = 0
    get_key = _get_key_windows if os.name == 'nt' else _get_key_unix

    if os.name == 'nt':
        os.system('')

    while True:
        limpiar_pantalla()
        print("=" * 60)
        print(f"{AnsiColors.CYAN}🏆 SISTEMA DE GESTIÓN DE TORNEO DE FÚTBOL 🏆{AnsiColors.RESET}")
        print("=" * 60)
        print("Seleccione una opción (use las flechas ↑↓ y Enter):")
        print("-" * 60)

        for i, option in enumerate(options):
            if i == current_option:
                print(f"{AnsiColors.YELLOW}► {option}{AnsiColors.RESET}")
            else:
                print(f"  {option}")
        
        print("-" * 60)
        print(f"{AnsiColors.BLUE}💡 Tip: Use las flechas para navegar y Enter para seleccionar{AnsiColors.RESET}")

        key = get_key()

        if key == 'up':
            current_option = (current_option - 1) % len(options)
        elif key == 'down':
            current_option = (current_option + 1) % len(options)
        elif key == 'enter':
            return current_option

def inicializar_sistema():
    """Inicializa los archivos de datos necesarios"""
    print("Inicializando sistema...")
    
    # Inicializar archivos individuales
    cf.initializeJson(EQUIPOS_FILE, {})
    cf.initializeJson(JUGADORES_FILE, {})
    cf.initializeJson(LIGAS_FILE, {})
    cf.initializeJson(TORNEOS_FILE, {})
    cf.initializeJson(TRANSFERENCIAS_FILE, {})
    cf.initializeJson(DIRIGENTES_FILE, {})
    cf.initializeJson(PARTIDOS_FILE, {})
    
    print("✅ Sistema inicializado correctamente.")

def mostrar_resumen_sistema():
    """Muestra un resumen rápido del estado del sistema"""
    equipos = cf.obtenerEquipos()
    jugadores = cf.obtenerJugadores()
    ligas = cf.obtenerLigas()
    torneos = cf.obtenerTorneos()
    transferencias = cf.obtenerTransferencias()
    
    equipos_activos = len([e for e in equipos.values() if e.get("activo", True)])
    jugadores_activos = len([j for j in jugadores.values() if j.get("activo", True)])
    ligas_activas = len([l for l in ligas.values() if l.get("activa", True)])
    torneos_activos = len([t for t in torneos.values() if t.get("activo", True)])
    
    print(f"\n{AnsiColors.GREEN}📊 RESUMEN DEL SISTEMA:{AnsiColors.RESET}")
    print(f"   🏟️  Equipos registrados: {equipos_activos}")
    print(f"   👥 Jugadores registrados: {jugadores_activos}")
    print(f"   🏆 Ligas activas: {ligas_activas}")
    print(f"   🎯 Torneos activos: {torneos_activos}")
    print(f"   🔄 Transferencias realizadas: {len(transferencias)}")

if __name__ == '__main__':
    # Inicializar sistema al arrancar
    inicializar_sistema()
    
    menu_items = [
        '🏟️  Gestionar Equipos', 
        '👥 Gestionar Jugadores',
        '🔄 Transferencias de Jugadores',
        '🏆 Gestionar Ligas',
        '🎯 Gestionar Torneos',
        '📊 Ver Estadísticas',
        '👔 Gestionar Dirigentes',
        '⚽ Gestionar Partidos',
        '❌ Salir del Sistema'
    ]
    
    while True:
        selected_index = interactive_menu_colored(menu_items)
        limpiar_pantalla()
        
        # Mostrar resumen antes de cada acción
        mostrar_resumen_sistema()
        
        selected_text = menu_items[selected_index]
        print(f"\n{AnsiColors.GREEN}✅ Ha seleccionado: {selected_text}{AnsiColors.RESET}")
        print("-" * 60)

        match selected_index:
            case 0:  # Gestionar Equipos
                equiposs.subMenuEquipos()
            case 1:  # Gestionar Jugadores
                jugadoress.subMenuJugadores()
            case 2:  # Transferencias
                transferenciass.subMenuTransferencias()
            case 3:  # Gestionar Ligas
                ligass.subMenuLigas()
            case 4:  # Gestionar Torneos
                torneoss.subMenuTorneos()
            case 5:  # Ver Estadísticas
                estadisticass.mostrar_estadisticas()
                input("\nPresione Enter para continuar...")
            case 6:  # Gestionar Dirigentes
                print("🚧 Módulo de Dirigentes en desarrollo...")
                input("Presione Enter para continuar...")
            case 7:  # Gestionar Partidos
                print("Módulo de Partidos en desarrollo...")
                input("Presione Enter para continuar...")
            case 8:  # Salir
                limpiar_pantalla()
                print("=" * 60)
                print(f"{AnsiColors.GREEN}¡Gracias por usar el Sistema de Gestión de Torneo!{AnsiColors.RESET}")
                print("=" * 60)
                print("👋 ¡Hasta luego!")
                print("=" * 60)
                break
            case _:
                print(f"{AnsiColors.RED}Opción no válida.{AnsiColors.RESET}")
                input("Presione Enter para continuar...")