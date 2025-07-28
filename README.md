Autor: Tomas Esteban Gonzalez Quintero J-3

Fecha: 27 de julio del 2025

------

# 🏆 Sistema de Gestión de Torneo de Fútbol

El **Sistema de Gestión de Torneo de Fútbol** SE TRABAJA EN PYTHON ESTE ES EL ENCARAGDO DE QUE EL USUARIO SUMINISTRE INFORMACION PARA hacer la experiencias mas agradable . Su arquitectura modular y enfoque en persistencia de datos mediante archivos JSON .

------

## 🚀 Características principales

- **Gestión de equipos:** Alta, baja, modificación y consulta de equipos.
- **Administración de jugadores:** Registro de jugadores con control de posiciones, edad y asignación a equipos.
- **Transferencias de jugadores:** Soporte para transferencias definitivas, préstamos, cláusulas de rescisión, intercambios y más.
- **Ligas y torneos:** Creación, configuración y administración de ligas y torneos personalizados.
- **Estadísticas globales:** Generación de estadísticas detalladas por torneo, equipo o jugador.
- **Gestión de dirigentes:** Administración de cargos directivos y personal relacionado a la organización.
- **Control de partidos:** Registro de resultados, programación de encuentros y seguimiento de fixture.
- **Persistencia de datos:** Almacenamiento en formato **JSON** con estructura configurable.

------

## 🏗️ Arquitectura y estructura del proyecto

El proyecto sigue una **arquitectura modular**..

```
bashCopiarEditartorneoDeFutbol-main/
├── app.py                # Punto de entrada principal (menú interactivo)
├── config.py             # Configuración global y constantes del sistema
├── controllers/          # Controladores: gestión de cada módulo funcional
│   ├── equipos.py        # CRUD de equipos
│   ├── jugadores.py      # CRUD de jugadores
│   ├── transferencias.py # Gestión de transferencias
│   ├── ligas.py          # Administración de ligas
│   ├── torneos.py        # Administración de torneos
│   ├── estadisticas.py   # Visualización de estadísticas
│   ├── dirigentes.py     # Control de cargos directivos
│   └── partidos.py       # Gestión de partidos
├── utils/                # Utilidades compartidas
│   ├── corefiles.py      # Manejo de lectura/escritura en JSON
│   ├── screenControllers.py # Limpieza y control de la interfaz CLI
│   └── validata.py       # Validaciones y sanitización de datos
├── data/                 # Almacenamiento persistente en JSON
│   ├── equipos.json
│   ├── jugadores.json
│   ├── transferencias.json
│   ├── ligas.json
│   ├── torneos.json
│   ├── dirigentes.json
│   └── partidos.json
```

## 

------

## 🔑 Flujo de uso de la aplicación

1. Al ejecutar `app.py`, se carga un **menú interactivo en la consola**:
   - Gestión de equipos
   - Gestión de jugadores
   - Transferencias
   - Ligas
   - Torneos
   - Estadísticas
   - Dirigentes
   - Partidos
   - Salir
2. El usuario selecciona la opción deseada ingresando el número correspondiente.
3. Los controladores gestionan las operaciones CRUD y actualizan automáticamente los archivos JSON.

------

## 1️⃣ **app.py **

Este archivo es el **núcleo principal de ejecución**.

- Importa todos los controladores: `equipos`, `jugadores`, `transferencias`, `ligas`, `torneos`, `estadisticas`, `dirigentes` y `partidos`.
- Carga utilidades como `limpiar_pantalla` desde `utils/screenControllers.py`.
- Define el menú principal con opciones numéricas.
- Usa un bucle `while True` que:
  1. Limpia la pantalla.
  2. Muestra el menú principal.
  3. Espera la selección del usuario.
  4. Valida la entrada (con `try/except ValueError`).
  5. Ejecuta la opción elegida mediante `match case`:
     - **1:** Llama a `subMenuEquipos()` (gestión de equipos).
     - **2:** Llama a `subMenuJugadores()` (gestión de jugadores).
     - … y así con cada módulo.
  6. Permite salir mostrando un mensaje de despedida.



------

## 2️⃣ **config.py **

Define todas las **constantes** y rutas del sistema:

- **Rutas de datos:** Apuntan a los JSON dentro de la carpeta `data/`.
- **Estructura inicial de la base de datos:** Un diccionario vacío con claves para cada entidad (`equipos`, `jugadores`, etc.).
- **Reglas del sistema:**
  - Jugadores por equipo: `MAX_JUGADORES_POR_EQUIPO = 25`, `MIN_JUGADORES_POR_EQUIPO = 11`.
  - Equipos por liga: mínimo 4, máximo 20.
  - Posiciones de jugadores (portero, defensa, delantero, etc.).
  - Tipos de transferencias válidas.
  - Cargos administrativos de dirigentes.

------

## 3️⃣ **controllers**

Aquí está la funcionalidad de cada módulo:

- **equipos.py:**
  - Crear equipos.
  - Modificar datos de un equipo.
  - Eliminar equipos.
  - Listar equipos existentes.
- **jugadores.py:**
  - Registrar nuevos jugadores.
  - Asignar jugadores a equipos.
  - Validar límites de jugadores.
- **transferencias.py:**
  - Transferir jugadores entre equipos.
  - Soporta tipos: préstamo, transferencia definitiva, libre, cláusula, etc.
- **ligas.py:**
  - Crear ligas.
  - Añadir equipos a ligas (respetando límites).
- **torneos.py:**
  - Organizar torneos con equipos participantes.
  - (Posible integración futura: fixtures automáticos).
- **estadisticas.py:**
  - Mostrar estadísticas globales: jugadores, equipos, torneos.
- **dirigentes.py:**
  - Registrar dirigentes y sus cargos.
  - Asociar dirigentes con equipos.
- **partidos.py:**
  - Programar partidos.
  - Registrar resultados.

------

## 4️⃣ **utils**

- **corefiles.py:**
  - Lee y escribe en archivos JSON.
  - Carga los datos y los guarda automáticamente tras cambios.
- **screenControllers.py:**
  - Contiene funciones de **interfaz CLI**, como limpiar la pantalla.
- **validata.py:**
  - Validaciones: asegura que los datos ingresados cumplen formatos (edad válida, posiciones correctas, rangos numéricos, etc.).

------

## 5️⃣ **data/** 

- Cada entidad tiene su archivo JSON (`equipos.json`, `jugadores.json`, etc.).
- Simula una **base de datos ligera**, donde toda la información se almacena y se actualiza automáticamente.



------

## 🔄 **Flujo completo del sistema**

1. El usuario ejecuta `app.py`.
2. Aparece el menú CLI.
3. Selecciona una opción (ej. gestionar jugadores).
4. El controlador correspondiente:
   - Pide datos.
   - Valida entradas (con `validata`).
   - Actualiza archivos JSON (con `corefiles`).
5. Los cambios persisten y están disponibles en futuras ejecuciones.

## Conclusion:

Desarrollé este proyecto de forma modular para que fuera fácil de mantener y escalar. Usé un menú en consola simple, archivos JSON para guardar los datos y controladores separados para cada parte del sistema, lo que hace que sea claro y ordenado, además de dejarlo listo para futuras mejora
