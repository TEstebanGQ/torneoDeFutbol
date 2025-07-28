import utils.corefiles as cf

def mostrar_estadisticas():
    print("ESTADÍSTICAS PRINCIPALES DEL SISTEMA")
    print("=" * 50)
    
    equipos = cf.obtenerEquipos()
    jugadores = cf.obtenerJugadores()
    partidos = cf.readJson("data/partidos.json")
    
    jugadoresactivos = {k: v for k, v in jugadores.items() if v.get("activo", True)}
    equiposactivos = {k: v for k, v in equipos.items() if v.get("activo", True)}
    

    mostrarJugadoRmasJoven(jugadoresactivos, equiposactivos)
    
    if partidos:
        mostrarEquiposVictoriasDerrotas(partidos, equiposactivos)
    else:
        print("      EQUIPO CON MÁS VICTORIAS:    ")
        print("   No hay partidos registrados aún.")
        
        print("      EQUIPO CON MÁS DERROTAS:")
        print("   No hay partidos registrados aún.")

def mostrarJugadoRmasJoven(jugadoresactivos, equiposactivos):
    print("    JUGADOR MÁS JOVEN DEL SISTEMA:")
    print("-" * 35)
    
    if not jugadoresactivos:
        print("   No hay jugadores registrados.")
        return
    
    jugadorMasJoven = None
    edad_minima = float('inf')
    
    for jugador_id, jugador in jugadoresactivos.items():
        edad = jugador.get('edad')
        if edad and edad < edad_minima:
            edad_minima = edad
            jugadorMasJoven = jugador
            jugadorMasJoven['id'] = jugador_id
    
    if jugadorMasJoven:
        equipo_id = jugadorMasJoven.get('equipo_id')
        equipo_nombre = "Sin equipo"
        equipo_pais = "N/A"
        
        if equipo_id and equipo_id in equiposactivos:
            equipo_data = equiposactivos[equipo_id]
            equipo_nombre = equipo_data.get('nombre', 'Sin equipo')
            equipo_pais = equipo_data.get('pais', 'N/A')
        
        print(f"   • Nombre: {jugadorMasJoven['nombre']}")
        print(f"   • Edad: {edad_minima} años")
        print(f"   • Posición: {jugadorMasJoven.get('posicion', 'N/A')}")
        print(f"   • Dorsal: #{jugadorMasJoven.get('dorsal', 'N/A')}")
        print(f"   • Equipo: {equipo_nombre}")
        print(f"   • País del equipo: {equipo_pais}")
    else:
        print("   No se encontró información de edad en los jugadores.")

def calcular_estadisticas_equipos_partidos(partidos, equipos_activos):
    """Calcula victorias y derrotas por equipo"""
    estadisticas_equipos = {}
    
    for equipo_id in equipos_activos.keys():
        estadisticas_equipos[equipo_id] = {
            'victorias': 0,
            'derrotas': 0,
            'partidos_jugados': 0
        }
    
    for partido in partidos.values():
        equipo_local_id = partido.get('equipo_local_id')
        equipo_visitante_id = partido.get('equipo_visitante_id')
        resultado = partido.get('resultado')
        
        if equipo_local_id in estadisticas_equipos and equipo_visitante_id in estadisticas_equipos:
            estadisticas_equipos[equipo_local_id]['partidos_jugados'] += 1
            estadisticas_equipos[equipo_visitante_id]['partidos_jugados'] += 1
            
            if resultado == "Victoria Local":
                estadisticas_equipos[equipo_local_id]['victorias'] += 1
                estadisticas_equipos[equipo_visitante_id]['derrotas'] += 1
            elif resultado == "Victoria Visitante":
                estadisticas_equipos[equipo_visitante_id]['victorias'] += 1
                estadisticas_equipos[equipo_local_id]['derrotas'] += 1

    return estadisticas_equipos

def mostrarEquiposVictoriasDerrotas(partidos, equipos_activos):
    estadisticas_equipos = calcular_estadisticas_equipos_partidos(partidos, equipos_activos)
    
    print("      EQUIPO CON MÁS VICTORIAS:")
    print("-" * 28)
    
    equipo_max_victorias = None
    max_victorias = -1
    
    for equipo_id, stats in estadisticas_equipos.items():
        if stats['victorias'] > max_victorias:
            max_victorias = stats['victorias']
            equipo_max_victorias = (equipo_id, stats)
    
    if equipo_max_victorias and max_victorias > 0:
        equipo_id, stats = equipo_max_victorias
        equipo_data = equipos_activos.get(equipo_id, {})
        
        print(f"   • Equipo: {equipo_data.get('nombre', 'N/A')}")
        print(f"   • Victorias: {max_victorias}")
        print(f"   • País: {equipo_data.get('pais', 'N/A')}")
        print(f"   • Ciudad: {equipo_data.get('ciudad', 'N/A')}")
        print(f"   • Partidos jugados: {stats['partidos_jugados']}")
    else:
        print("   Ningún equipo tiene victorias registradas aún.")
    
    print("      EQUIPO CON MÁS DERROTAS:")
    print("-" * 27)
    
    equipo_max_derrotas = None
    max_derrotas = -1
    
    for equipo_id, stats in estadisticas_equipos.items():
        if stats['derrotas'] > max_derrotas:
            max_derrotas = stats['derrotas']
            equipo_max_derrotas = (equipo_id, stats)
    
    if equipo_max_derrotas and max_derrotas > 0:
        equipo_id, stats = equipo_max_derrotas
        equipo_data = equipos_activos.get(equipo_id, {})
        
        print(f"   • Equipo: {equipo_data.get('nombre', 'N/A')}")
        print(f"   • Derrotas: {max_derrotas}")
        print(f"   • País: {equipo_data.get('pais', 'N/A')}")
        print(f"   • Ciudad: {equipo_data.get('ciudad', 'N/A')}")
        print(f"   • Partidos jugados: {stats['partidos_jugados']}")
    else:
        print("   Ningún equipo tiene derrotas registradas aún.")

def estadisticas_transferencias():
    transferencias = cf.obtenerTransferencias()
    total = len(transferencias)
    por_tipo = {}
    for trans in transferencias.values():
        tipo = trans.get('tipo', 'N/A')
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
    
    return {
        'total': total,
        'monto_total': 0,
        'promedio_monto': 0,
        'por_tipo': por_tipo
    }
