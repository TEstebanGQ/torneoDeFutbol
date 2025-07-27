import os
import json
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import utils.corefiles as cf
from config import TRANSFERENCIAS_FILE, TIPOS_TRANSFERENCIA
import controllers.jugadores as jugadores_controller
import controllers.equipos as equipos_controller

def obtener_fecha_valida():
    while True:
        fecha_str = input("Ingrese la fecha de la transferencia (DD-MM-AAAA): ").strip()
        if validar_formato_fecha(fecha_str):
            return fecha_str
        else:
            print("Error: Formato de fecha no válido. Por favor, use DD-MM-AAAA.")

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

def mostrar_jugadores_disponibles():
    """Muestra panel con jugadores disponibles para transferir"""
    jugadores = cf.obtenerJugadores()
    equipos = cf.obtenerEquipos()
    
    jugadores_activos = {jid: j for jid, j in jugadores.items() if j.get("activo", True)}
    
    if not jugadores_activos:
        print("No hay jugadores disponibles para transferir.")
        return
    
    print("=" * 60)
    print("📋 JUGADORES DISPONIBLES PARA TRANSFERIR")
    print("=" * 60)
    
    for jugador_id, jugador in jugadores_activos.items():
        equipo_actual = equipos.get(jugador.get('equipo_id'), {})
        nombre_equipo_actual = equipo_actual.get('nombre', "Sin Equipo")
        
        print(f"ID: {jugador_id} | {jugador['nombre']} #{jugador['dorsal']}")
        print(f"   Equipo: {nombre_equipo_actual} | Posición: {jugador['posicion']}")
        print("-" * 60)

def subMenuTransferencias():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Transferencias ---")
        print("1. Realizar una nueva transferencia")
        print("2. Ver historial de transferencias")
        print("3. Volver al Menú Principal")
        print("---------------------------------")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            transferir_jugador()
        elif opcion == '2':
            ver_transferencias()
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            pausar_pantalla()

def transferir_jugador():
    jugadores = cf.obtenerJugadores()
    equipos = cf.obtenerEquipos()
    transferencias = cf.obtenerTransferencias()

    if not jugadores or not equipos:
        print("Error: Se necesitan datos de jugadores y equipos para realizar una transferencia.")
        pausar_pantalla()
        return

    # Filtrar solo jugadores activos
    jugadores_activos = {jid: j for jid, j in jugadores.items() if j.get("activo", True)}

    while True:
        limpiar_pantalla()
        mostrar_jugadores_disponibles()
        
        if not jugadores_activos:
            print("No hay jugadores disponibles para transferir.")
            pausar_pantalla()
            return
        
        try:
            jugador_id = input("\nIngrese el ID del jugador a transferir: ").strip()
            
            if jugador_id not in jugadores_activos:
                print("\nError: No se encontró un jugador activo con ese ID. Intente de nuevo.")
                pausar_pantalla()
                continue
            else:
                break
        except:
            print("Error: ID inválido. Intente de nuevo.")
            pausar_pantalla()
            continue

    jugador_a_transferir = jugadores_activos[jugador_id]
    equipo_origen_id = jugador_a_transferir['equipo_id']
    equipo_origen = equipos.get(equipo_origen_id, {})
    nombre_origen = equipo_origen.get('nombre', "Desconocido")
    
    limpiar_pantalla()
    print(f"Jugador seleccionado: {jugador_a_transferir['nombre']}")
    print(f"Equipo de Origen: {nombre_origen} (ID: {equipo_origen_id})")
    print(f"Posición: {jugador_a_transferir['posicion']} | Dorsal: {jugador_a_transferir['dorsal']}")

    # Mostrar equipos de destino disponibles
    equipos_disponibles = {eid: eq for eid, eq in equipos.items() 
                          if eid != equipo_origen_id and eq.get("activo", True)}
    
    while True:
        print("\n--- Equipos de Destino Disponibles ---")
        for equipo_id, equipo in equipos_disponibles.items():
            print(f"ID: {equipo_id} - Nombre: {equipo['nombre']} - País: {equipo['pais']} ({equipo['ciudad']})")
        print("------------------------------------")
        
        equipo_destino_id = input("Ingrese el ID del nuevo equipo: ").strip()
        
        if equipo_destino_id in equipos_disponibles:
            break
        else:
            print("Error: ID de equipo no válido o es el mismo equipo de origen.")
            pausar_pantalla()

    equipo_destino = equipos_disponibles[equipo_destino_id]
    nombre_destino = equipo_destino['nombre']

    # Selección del tipo de transferencia
    tipo_transferencia = ""
    while True:
        limpiar_pantalla()
        print("--- Tipos de Transferencia Disponibles ---")
        tipos_simplificados = ["Transferencia definitiva", "Cesión o préstamo", "Transferencia libre"]
        for i, tipo in enumerate(tipos_simplificados, 1):
            print(f"{i}. {tipo}")
        print("----------------------------------------")
        try:
            opcion_tipo = int(input("Seleccione el número del tipo de transferencia: "))
            if 1 <= opcion_tipo <= len(tipos_simplificados):
                tipo_transferencia = tipos_simplificados[opcion_tipo - 1]
                break
            else:
                print("Error: Número de opción no válido. Intente de nuevo.")
                pausar_pantalla()
        except ValueError:
            print("Error: Debe ingresar un número. Intente de nuevo.")
            pausar_pantalla()

    fecha_transferencia = obtener_fecha_valida()
    
    # Verificar disponibilidad del dorsal en el nuevo equipo
    jugadores_equipo_destino = jugadores_controller.obtenerJugadoresPorEquipo(equipo_destino_id)
    dorsales_ocupados = [j['dorsal'] for j in jugadores_equipo_destino.values()]
    
    nuevo_dorsal = jugador_a_transferir['dorsal']
    if nuevo_dorsal in dorsales_ocupados:
        print(f"\nAdvertencia: El dorsal {nuevo_dorsal} ya está ocupado en {nombre_destino}.")
        while True:
            try:
                nuevo_dorsal = int(input("Ingrese un nuevo dorsal (1-99): "))
                if 1 <= nuevo_dorsal <= 99 and nuevo_dorsal not in dorsales_ocupados:
                    break
                else:
                    print("Error: Dorsal no válido o ya ocupado.")
            except ValueError:
                print("Error: Debe ingresar un número válido.")

    # Generar ID único numérico ascendente
    nuevo_id_transferencia = cf.generateId(list(transferencias.keys()))
    
    nueva_transferencia = {
        "jugador_id": jugador_id,
        "jugador_nombre": jugador_a_transferir['nombre'],
        "equipo_origen_id": equipo_origen_id,
        "equipo_origen_nombre": nombre_origen,
        "equipo_destino_id": equipo_destino_id,
        "equipo_destino_nombre": nombre_destino,
        "tipo": tipo_transferencia,
        "fecha": fecha_transferencia,
        "dorsal_anterior": jugador_a_transferir['dorsal'],
        "dorsal_nuevo": nuevo_dorsal
    }
    
    transferencias[nuevo_id_transferencia] = nueva_transferencia
    cf.guardarTransferencias(transferencias)

    # Actualizar datos del jugador
    jugador_a_transferir['equipo_id'] = equipo_destino_id
    jugador_a_transferir['dorsal'] = nuevo_dorsal
    
    # Agregar al historial de equipos si no existe
    if 'historial_equipos' not in jugador_a_transferir:
        jugador_a_transferir['historial_equipos'] = [equipo_origen_id]
    
    if equipo_destino_id not in jugador_a_transferir['historial_equipos']:
        jugador_a_transferir['historial_equipos'].append(equipo_destino_id)
    
    jugadores[jugador_id] = jugador_a_transferir
    cf.guardarJugadores(jugadores)
    
    print("\n" + "="*60)
    print("¡TRANSFERENCIA COMPLETADA Y REGISTRADA EXITOSAMENTE!")
    print("="*60)
    print(f"Jugador: {jugador_a_transferir['nombre']}")
    print(f"De: {nombre_origen} → A: {nombre_destino}")
    print(f"Tipo: {tipo_transferencia}")
    print(f"Dorsal: #{jugador_a_transferir['dorsal']}")
    print("="*60)
    pausar_pantalla()

def ver_transferencias():
    limpiar_pantalla()
    print("--- Historial de Transferencias Realizadas ---")

    transferencias = cf.obtenerTransferencias()
    
    if not transferencias:
        print("No hay transferencias registradas aún.")
    else:
        for transfer_id, trans in transferencias.items():
            print(f"ID Transferencia: {transfer_id}")
            print(f"Fecha: {trans['fecha']}")
            print(f"Jugador: {trans.get('jugador_nombre', 'N/A')} (ID: {trans['jugador_id']})")
            print(f"Origen: {trans.get('equipo_origen_nombre', 'N/A')} → Destino: {trans.get('equipo_destino_nombre', 'N/A')}")
            print(f"Tipo: {trans['tipo']}")
            if trans.get('dorsal_anterior') != trans.get('dorsal_nuevo'):
                print(f"Dorsal: #{trans.get('dorsal_anterior')} → #{trans.get('dorsal_nuevo')}")
            else:
                print(f"Dorsal: #{trans.get('dorsal_nuevo', 'N/A')}")
            print("-" * 60)
    
    print("Presione Enter para continuar...")
    pausar_pantalla()

def estadisticas_transferencias():
    """Función auxiliar para obtener estadísticas (usado por el módulo de estadísticas)"""
    transferencias = cf.obtenerTransferencias()
    
    total = len(transferencias)
    
    # Estadísticas por tipo
    por_tipo = {}
    for trans in transferencias.values():
        tipo = trans.get('tipo', 'N/A')
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    
    return {
        'total': total,
        'monto_total': 0,  # Sin monto según requerimientos
        'promedio_monto': 0,
        'por_tipo': por_tipo
    }

def obtener_transferencias_por_equipo(equipo_id: str, tipo_participacion: str):
    """Función auxiliar para obtener transferencias de un equipo
    tipo_participacion: 'origen' o 'destino'
    """
    transferencias = cf.obtenerTransferencias()
    
    if tipo_participacion == 'origen':
        return {tid: t for tid, t in transferencias.items()
                if t.get('equipo_origen_id') == equipo_id}
    elif tipo_participacion == 'destino':
        return {tid: t for tid, t in transferencias.items()
                if t.get('equipo_destino_id') == equipo_id}
    else:
        return {}