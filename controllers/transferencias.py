import os
import json
import datetime
from utils.screenControllers import limpiar_pantalla, pausar_pantalla
import utils.corefiles as cf
from config import TRANSFERENCIAS_FILE, TIPOS_TRANSFERENCIA
import controllers.jugadores as jugadores_controller
import controllers.equipos as equipos_controller

def obtener_fecha_valida():
    while True:
        fecha_str = input("Ingrese la fecha de la transferencia (DD/MM/YYYY): ").strip()
        try:
            datetime.datetime.strptime(fecha_str, "%d/%m/%Y")
            return fecha_str
        except ValueError:
            print("Error: Formato de fecha no válido. Por favor, use DD/MM/YYYY (ej: 28/07/2024).")

def obtener_monto_transferencia():
    while True:
        monto_str = input("Ingrese el monto de la transferencia (USD, 0 si es gratuita): ").strip()
        try:
            monto = float(monto_str)
            if monto >= 0:
                return monto
            else:
                print("Error: El monto no puede ser negativo.")
        except ValueError:
            print("Error: Debe ingresar un número válido.")

def subMenuTransferencias():
    while True:
        limpiar_pantalla()
        print("--- Submenú de Transferencias ---")
        print("1. Realizar una nueva transferencia")
        print("2. Ver historial de transferencias")
        print("3. Ver transferencias por jugador")
        print("4. Ver transferencias por equipo")
        print("5. Estadísticas de transferencias")
        print("6. Volver al Menú Principal")
        print("---------------------------------")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            transferir_jugador()
        elif opcion == '2':
            ver_transferencias()
        elif opcion == '3':
            ver_transferencias_por_jugador()
        elif opcion == '4':
            ver_transferencias_por_equipo()
        elif opcion == '5':
            mostrar_estadisticas()
        elif opcion == '6':
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
        print("--- Jugadores Disponibles para Transferir ---")
        
        if not jugadores_activos:
            print("No hay jugadores disponibles para transferir.")
            pausar_pantalla()
            return
        
        for jugador_id, jugador in jugadores_activos.items():
            equipo_actual = equipos.get(jugador.get('equipo_id'), {})
            nombre_equipo_actual = equipo_actual.get('nombre', "Sin Equipo")
            
            print(f"ID: {jugador_id} | Jugador: {jugador['nombre']}")
            print(f"   Equipo: {nombre_equipo_actual} | Posición: {jugador['posicion']} | Dorsal: {jugador['dorsal']}")
            print("-" * 70)
        
        jugador_id = input("\nIngrese el ID del jugador a transferir: ").strip()
        
        if jugador_id not in jugadores_activos:
            print("\nError: No se encontró un jugador activo con ese ID. Intente de nuevo.")
            pausar_pantalla()
            continue
        else:
            break

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
        for i, tipo in enumerate(TIPOS_TRANSFERENCIA, 1):
            print(f"{i}. {tipo}")
        print("----------------------------------------")
        try:
            opcion_tipo = int(input("Seleccione el número del tipo de transferencia: "))
            if 1 <= opcion_tipo <= len(TIPOS_TRANSFERENCIA):
                tipo_transferencia = TIPOS_TRANSFERENCIA[opcion_tipo - 1]
                break
            else:
                print("Error: Número de opción no válido. Intente de nuevo.")
                pausar_pantalla()
        except ValueError:
            print("Error: Debe ingresar un número. Intente de nuevo.")
            pausar_pantalla()

    fecha_transferencia = obtener_fecha_valida()
    monto = obtener_monto_transferencia()
    
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

    # Generar ID único para la transferencia
    nuevo_id_transferencia = cf.generateId("TR", list(transferencias.keys()))
    
    nueva_transferencia = {
        "jugador_id": jugador_id,
        "jugador_nombre": jugador_a_transferir['nombre'],
        "equipo_origen_id": equipo_origen_id,
        "equipo_origen_nombre": nombre_origen,
        "equipo_destino_id": equipo_destino_id,
        "equipo_destino_nombre": nombre_destino,
        "tipo": tipo_transferencia,
        "fecha": fecha_transferencia,
        "monto": monto,
        "dorsal_anterior": jugador_a_transferir['dorsal'],
        "dorsal_nuevo": nuevo_dorsal,
        "fecha_registro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
    print(f"Monto: ${monto:,.2f} USD")
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
        # Ordenar por fecha de registro (más recientes primero)
        transferencias_ordenadas = sorted(transferencias.items(), 
                                        key=lambda x: x[1].get('fecha_registro', ''), 
                                        reverse=True)
        
        for transfer_id, trans in transferencias_ordenadas:
            print(f"ID Transferencia: {transfer_id}")
            print(f"Fecha: {trans['fecha']}")
            print(f"Jugador: {trans.get('jugador_nombre', 'N/A')} (ID: {trans['jugador_id']})")
            print(f"Origen: {trans.get('equipo_origen_nombre', 'N/A')} → Destino: {trans.get('equipo_destino_nombre', 'N/A')}")
            print(f"Tipo: {trans['tipo']}")
            print(f"Monto: ${trans.get('monto', 0):,.2f} USD")
            if trans.get('dorsal_anterior') != trans.get('dorsal_nuevo'):
                print(f"Dorsal: #{trans.get('dorsal_anterior')} → #{trans.get('dorsal_nuevo')}")
            else:
                print(f"Dorsal: #{trans.get('dorsal_nuevo', 'N/A')}")
            print(f"Registrada: {trans.get('fecha_registro', 'N/A')}")
            print("-" * 60)
    
    print("Presione Enter para continuar...")
    pausar_pantalla()

def ver_transferencias_por_jugador():
    limpiar_pantalla()
    print("--- Transferencias por Jugador ---")
    
    jugadores = cf.obtenerJugadores()
    
    if not jugadores:
        print("No hay jugadores registrados.")
        pausar_pantalla()
        return
    
    print("Jugadores disponibles:")
    for jugador_id, jugador in jugadores.items():
        if jugador.get("activo", True):
            print(f"ID: {jugador_id} - {jugador['nombre']}")
    
    jugador_id = input("\nIngrese el ID del jugador: ").strip()
    
    if jugador_id not in jugadores:
        print("Jugador no encontrado.")
        pausar_pantalla()
        return
    
    jugador = jugadores[jugador_id]
    transferencias = cf.obtenerTransferencias()
    
    transferencias_jugador = {tid: t for tid, t in transferencias.items()
                             if t.get('jugador_id') == jugador_id}
    
    print(f"\n--- Transferencias de {jugador['nombre']} ---")
    
    if not transferencias_jugador:
        print("Este jugador no tiene transferencias registradas.")
    else:
        for transfer_id, trans in transferencias_jugador.items():
            print(f"\nFecha: {trans['fecha']}")
            print(f"De: {trans.get('equipo_origen_nombre', 'N/A')} → A: {trans.get('equipo_destino_nombre', 'N/A')}")
            print(f"Tipo: {trans['tipo']}")
            print(f"Monto: ${trans.get('monto', 0):,.2f} USD")
            print("-" * 40)
    
    pausar_pantalla()

def ver_transferencias_por_equipo():
    limpiar_pantalla()
    print("--- Transferencias por Equipo ---")
    
    equipos = cf.obtenerEquipos()
    
    if not equipos:
        print("No hay equipos registrados.")
        pausar_pantalla()
        return
    
    print("Equipos disponibles:")
    for equipo_id, equipo in equipos.items():
        if equipo.get("activo", True):
            print(f"ID: {equipo_id} - {equipo['nombre']}")
    
    equipo_id = input("\nIngrese el ID del equipo: ").strip()
    
    if equipo_id not in equipos:
        print("Equipo no encontrado.")
        pausar_pantalla()
        return
    
    equipo = equipos[equipo_id]
    transferencias = cf.obtenerTransferencias()
    
    # Transferencias donde el equipo fue origen o destino
    transferencias_equipo = {tid: t for tid, t in transferencias.items()
                           if t.get('equipo_origen_id') == equipo_id or t.get('equipo_destino_id') == equipo_id}
    
    print(f"\n--- Transferencias de {equipo['nombre']} ---")
    
    if not transferencias_equipo:
        print("Este equipo no tiene transferencias registradas.")
    else:
        fichajes = []
        salidas = []
        
        for transfer_id, trans in transferencias_equipo.items():
            if trans.get('equipo_destino_id') == equipo_id:
                fichajes.append(trans)
            else:
                salidas.append(trans)
        
        print(f"\n📥 FICHAJES ({len(fichajes)}):")
        for trans in fichajes:
            print(f"  • {trans.get('jugador_nombre', 'N/A')} desde {trans.get('equipo_origen_nombre', 'N/A')}")
            print(f"    Fecha: {trans['fecha']} | Monto: ${trans.get('monto', 0):,.2f}")
        
        print(f"\n📤 SALIDAS ({len(salidas)}):")
        for trans in salidas:
            print(f"  • {trans.get('jugador_nombre', 'N/A')} hacia {trans.get('equipo_destino_nombre', 'N/A')}")
            print(f"    Fecha: {trans['fecha']} | Monto: ${trans.get('monto', 0):,.2f}")
    
    pausar_pantalla()

def mostrar_estadisticas():
    limpiar_pantalla()
    print("--- Estadísticas de Transferencias ---")
    
    transferencias = cf.obtenerTransferencias()
    
    if not transferencias:
        print("No hay transferencias registradas para mostrar estadísticas.")
        pausar_pantalla()
        return
    
    total = len(transferencias)
    monto_total = sum(t.get('monto', 0) for t in transferencias.values())
    promedio_monto = monto_total / total if total > 0 else 0
    
    # Estadísticas por tipo
    por_tipo = {}
    for trans in transferencias.values():
        tipo = trans.get('tipo', 'N/A')
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    
    # Transferencia más cara
    transferencia_mas_cara = max(transferencias.values(), key=lambda x: x.get('monto', 0))
    
    print(f"📊 RESUMEN GENERAL")
    print(f"Total de transferencias: {total}")
    print(f"Monto total movido: ${monto_total:,.2f} USD")
    print(f"Promedio por transferencia: ${promedio_monto:,.2f} USD")
    
    print(f"\n📈 POR TIPO DE TRANSFERENCIA:")
    for tipo, cantidad in sorted(por_tipo.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (cantidad / total) * 100
        print(f"  • {tipo}: {cantidad} ({porcentaje:.1f}%)")
    
    print(f"\n💰 TRANSFERENCIA MÁS COSTOSA:")
    print(f"  Jugador: {transferencia_mas_cara.get('jugador_nombre', 'N/A')}")
    print(f"  Monto: ${transferencia_mas_cara.get('monto', 0):,.2f} USD")
    print(f"  De: {transferencia_mas_cara.get('equipo_origen_nombre', 'N/A')}")
    print(f"  A: {transferencia_mas_cara.get('equipo_destino_nombre', 'N/A')}")
    
    pausar_pantalla()

def estadisticas_transferencias():
    """Función auxiliar para obtener estadísticas (usado por el módulo de estadísticas)"""
    transferencias = cf.obtenerTransferencias()
    
    total = len(transferencias)
    monto_total = sum(t.get('monto', 0) for t in transferencias.values())
    promedio_monto = monto_total / total if total > 0 else 0
    
    # Estadísticas por tipo
    por_tipo = {}
    for trans in transferencias.values():
        tipo = trans.get('tipo', 'N/A')
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    
    return {
        'total': total,
        'monto_total': monto_total,
        'promedio_monto': promedio_monto,
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