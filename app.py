""" 
Autor: Tomas Esteban Gonzalez Quintero
fecha: 27/07/2025
Descripcion: Aqui se impleta un sitema de torneos donde se guardan jugadores equipos, y demas para establecer las ligas y los torneos
"""
import controllers.equipos as equiposs
import controllers.jugadores as jugadoress
import controllers.transferencias as transferenciass
import controllers.ligas as ligass
import controllers.torneos as torneoss
import controllers.estadisticas as estadisticass
import controllers.partidos as partidoss
import controllers.dirigentes as dirigentess
from utils.screenControllers import limpiar_pantalla
from config import *

def mostrar_menu_numerico(menu_items):
    print("=" * 60)
    print("         SISTEMA DE GESTIÓN DE TORNEO DE FÚTBOL")
    print("=" * 60)
    print("Seleccione una opción escribiendo el número:")
    print("-" * 60)
    for i, item in enumerate(menu_items, start=1):
        print(f"{i}. {item}")
    print("-" * 60)




if __name__ == '__main__':
    

    menu_items = [
        "Gestionar Equipos",
        "Gestionar Jugadores",
        "Transferencias de Jugadores",
        "Gestionar Ligas",
        "Gestionar Torneos",
        "Ver Estadísticas",
        "Gestionar Dirigentes",
        "Gestionar Partidos",
        "Salir del Sistema"
    ]

    while True:
        limpiar_pantalla()
        mostrar_menu_numerico(menu_items)

        try:
            opcion = int(input("Ingrese una opción: "))
            limpiar_pantalla()
            

            if opcion < 1 or opcion > len(menu_items):
                print("Opción fuera de rango.")
                input("Presione Enter para continuar...")
                continue

            print(f"Ha seleccionado: {menu_items[opcion - 1]}")
            print("-" * 60)

            match opcion:
                case 1:
                    equiposs.subMenuEquipos()
                case 2:
                    jugadoress.subMenuJugadores()
                case 3:
                    transferenciass.subMenuTransferencias()
                case 4:
                    ligass.subMenuLigas()
                case 5:
                    torneoss.subMenuTorneos()
                case 6:
                    estadisticass.mostrar_estadisticas()
                    input("\nPresione Enter para continuar...")
                case 7:
                    dirigentess.subMenuDirigentes()
                case 8:
                    partidoss.subMenuPartidos()
                case 9:
                    limpiar_pantalla()
                    print("=" * 60)
                    print("Gracias por usar el Sistema de Gestión de Torneo.")
                    print("=" * 60)
                    break
        except ValueError:
            print("Debe ingresar un número válido.")
            input("Presione Enter para continuar...")
