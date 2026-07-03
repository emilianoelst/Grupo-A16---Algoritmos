"""
Sistema de Inscripción a Cursos
--------------------------------
Programa de consola para administrar inscripciones a cursos.
Permite registrar estudiantes, administrar cursos con cupos limitados,
inscribir o dar de baja estudiantes, gestionar listas de espera y
mostrar estadísticas de inscriptos.

Los datos se guardan en un archivo JSON (datos_sistema.json) para que
persistan entre ejecuciones del programa.
"""

import json
import os
import re

ARCHIVO_DATOS = "datos_sistema.json"

# ---------------------------------------------------------------------
# Estructuras de datos principales (se cargan/guardan en el JSON)
#
# estudiantes = {
#     "12345678": {"nombre": "Ana Pérez", "email": "ana@mail.com"},
#     ...
# }
#
# cursos = {
#     "PY101": {
#         "nombre": "Python Inicial",
#         "cupo": 20,
#         "inscriptos": ["12345678", ...],
#         "espera": ["87654321", ...]
#     },
#     ...
# }
# ---------------------------------------------------------------------

estudiantes = {}
cursos = {}


# =======================================================================
# FUNCIONES DE PERSISTENCIA (guardar y cargar datos en disco)
# =======================================================================

def cargar_datos():
    """Carga estudiantes y cursos desde el archivo JSON, si existe."""
    global estudiantes, cursos
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                estudiantes = datos.get("estudiantes", {})
                cursos = datos.get("cursos", {})
            print("Datos cargados correctamente desde", ARCHIVO_DATOS)
        except (json.JSONDecodeError, OSError) as error:
            print("Aviso: no se pudieron leer los datos guardados "
                  f"({error}). Se inicia con datos vacíos.")
            estudiantes = {}
            cursos = {}
    else:
        estudiantes = {}
        cursos = {}


def guardar_datos():
    """Guarda estudiantes y cursos en el archivo JSON."""
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            json.dump({"estudiantes": estudiantes, "cursos": cursos},
                      archivo, ensure_ascii=False, indent=4)
    except OSError as error:
        print(f"Error al guardar los datos: {error}")


# =======================================================================
# FUNCIONES DE VALIDACIÓN
# =======================================================================

def validar_dni(dni):
    """Un DNI válido: solo dígitos, entre 7 y 8 caracteres."""
    return dni.isdigit() and 7 <= len(dni) <= 8


def validar_email(email):
    """Validación básica de formato de email con expresión regular."""
    patron = r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email) is not None


def validar_texto_no_vacio(texto):
    """Verifica que el texto no esté vacío ni sea solo espacios."""
    return len(texto.strip()) > 0


def pedir_entero(mensaje, minimo=None):
    """Pide un número entero por consola, repite hasta obtener uno válido."""
    while True:
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)
            if minimo is not None and numero < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}.")
                continue
            return numero
        except ValueError:
            print("Error: debe ingresar un número entero válido.")


def pedir_texto(mensaje):
    """Pide un texto no vacío por consola."""
    while True:
        texto = input(mensaje).strip()
        if validar_texto_no_vacio(texto):
            return texto
        print("Error: el campo no puede estar vacío.")


def pedir_dni(mensaje):
    """Pide un DNI válido por consola."""
    while True:
        dni = input(mensaje).strip()
        if validar_dni(dni):
            return dni
        print("Error: el DNI debe contener solo números (7 u 8 dígitos).")


def pedir_email(mensaje):
    """Pide un email válido por consola."""
    while True:
        email = input(mensaje).strip()
        if validar_email(email):
            return email
        print("Error: formato de email inválido (ejemplo: nombre@dominio.com).")


# =======================================================================
# GESTIÓN DE ESTUDIANTES
# =======================================================================

def registrar_estudiante():
    """Registra un nuevo estudiante en el sistema."""
    print("\n--- Registro de Estudiante ---")
    dni = pedir_dni("DNI del estudiante: ")

    if dni in estudiantes:
        print(f"Ya existe un estudiante registrado con DNI {dni} "
              f"({estudiantes[dni]['nombre']}).")
        return

    nombre = pedir_texto("Nombre y apellido: ")
    email = pedir_email("Email: ")

    estudiantes[dni] = {"nombre": nombre, "email": email}
    guardar_datos()
    print(f"Estudiante '{nombre}' registrado con éxito (DNI: {dni}).")


def listar_estudiantes():
    """Muestra todos los estudiantes registrados."""
    print("\n--- Listado de Estudiantes ---")
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return

    contador = 0
    for dni, datos in estudiantes.items():
        contador += 1
        print(f"{contador}. DNI: {dni} | Nombre: {datos['nombre']} "
              f"| Email: {datos['email']}")
    print(f"Total de estudiantes: {contador}")


def buscar_estudiante_interactivo():
    """Busca un estudiante por DNI y muestra sus datos e inscripciones."""
    print("\n--- Buscar Estudiante ---")
    dni = pedir_dni("Ingrese el DNI a buscar: ")

    if dni not in estudiantes:
        print("No se encontró ningún estudiante con ese DNI.")
        return

    datos = estudiantes[dni]
    print(f"Nombre: {datos['nombre']} | Email: {datos['email']}")

    cursos_inscripto = []
    cursos_en_espera = []
    for codigo, curso in cursos.items():
        if dni in curso["inscriptos"]:
            cursos_inscripto.append(curso["nombre"])
        if dni in curso["espera"]:
            cursos_en_espera.append(curso["nombre"])

    if cursos_inscripto:
        print("Cursos inscripto:", ", ".join(cursos_inscripto))
    else:
        print("No tiene inscripciones activas.")

    if cursos_en_espera:
        print("En lista de espera de:", ", ".join(cursos_en_espera))


# =======================================================================
# GESTIÓN DE CURSOS
# =======================================================================

def registrar_curso():
    """Registra un nuevo curso con su cupo máximo."""
    print("\n--- Registro de Curso ---")
    codigo = pedir_texto("Código del curso (ej: PY101): ").upper()

    if codigo in cursos:
        print(f"Ya existe un curso con el código {codigo}.")
        return

    nombre = pedir_texto("Nombre del curso: ")
    cupo = pedir_entero("Cupo máximo de inscriptos: ", minimo=1)

    cursos[codigo] = {
        "nombre": nombre,
        "cupo": cupo,
        "inscriptos": [],
        "espera": []
    }
    guardar_datos()
    print(f"Curso '{nombre}' ({codigo}) registrado con cupo para {cupo} personas.")


def listar_cursos():
    """Muestra todos los cursos con su ocupación de cupos."""
    print("\n--- Listado de Cursos ---")
    if not cursos:
        print("No hay cursos registrados.")
        return

    for codigo, curso in cursos.items():
        ocupados = len(curso["inscriptos"])
        disponibles = curso["cupo"] - ocupados
        en_espera = len(curso["espera"])
        estado = "CUPO LLENO" if disponibles <= 0 else f"{disponibles} lugares libres"
        print(f"[{codigo}] {curso['nombre']} | Cupo: {curso['cupo']} "
              f"| Inscriptos: {ocupados} | {estado} | En espera: {en_espera}")


def seleccionar_curso_existente():
    """Pide un código de curso y valida que exista. Devuelve el código o None."""
    if not cursos:
        print("No hay cursos registrados todavía.")
        return None

    codigo = pedir_texto("Código del curso: ").upper()
    if codigo not in cursos:
        print(f"No existe un curso con código {codigo}.")
        return None
    return codigo


# =======================================================================
# GESTIÓN DE INSCRIPCIONES Y LISTA DE ESPERA
# =======================================================================

def inscribir_estudiante():
    """Inscribe un estudiante a un curso, o lo agrega a la lista de espera
    si el cupo está lleno."""
    print("\n--- Inscripción a Curso ---")

    if not estudiantes:
        print("Primero debe haber estudiantes registrados.")
        return

    dni = pedir_dni("DNI del estudiante: ")
    if dni not in estudiantes:
        print("No existe un estudiante con ese DNI. Regístrelo primero.")
        return

    codigo = seleccionar_curso_existente()
    if codigo is None:
        return

    curso = cursos[codigo]

    if dni in curso["inscriptos"]:
        print(f"El estudiante ya está inscripto en '{curso['nombre']}'.")
        return
    if dni in curso["espera"]:
        print(f"El estudiante ya está en la lista de espera de '{curso['nombre']}'.")
        return

    if len(curso["inscriptos"]) < curso["cupo"]:
        curso["inscriptos"].append(dni)
        guardar_datos()
        print(f"Inscripción exitosa en '{curso['nombre']}'.")
    else:
        curso["espera"].append(dni)
        guardar_datos()
        posicion = len(curso["espera"])
        print(f"Cupo lleno. El estudiante fue agregado a la lista de espera "
              f"en la posición {posicion}.")


def dar_baja_inscripcion():
    """Da de baja a un estudiante de un curso. Si hay lista de espera,
    promueve automáticamente al primero de la lista."""
    print("\n--- Baja de Inscripción ---")

    codigo = seleccionar_curso_existente()
    if codigo is None:
        return

    curso = cursos[codigo]
    dni = pedir_dni("DNI del estudiante a dar de baja: ")

    if dni in curso["inscriptos"]:
        curso["inscriptos"].remove(dni)
        print(f"Se dio de baja a {estudiantes[dni]['nombre']} de '{curso['nombre']}'.")

        # Si hay lista de espera, se promueve automáticamente al primero
        if curso["espera"]:
            siguiente_dni = curso["espera"].pop(0)
            curso["inscriptos"].append(siguiente_dni)
            nombre_siguiente = estudiantes.get(siguiente_dni, {}).get(
                "nombre", siguiente_dni)
            print(f"Se liberó un cupo: {nombre_siguiente} fue promovido "
                  f"automáticamente desde la lista de espera.")
        guardar_datos()

    elif dni in curso["espera"]:
        curso["espera"].remove(dni)
        guardar_datos()
        print("El estudiante estaba en lista de espera y fue removido.")

    else:
        print("Ese estudiante no está inscripto ni en espera en este curso.")


def ver_lista_espera():
    """Muestra la lista de espera de un curso puntual."""
    print("\n--- Lista de Espera ---")
    codigo = seleccionar_curso_existente()
    if codigo is None:
        return

    curso = cursos[codigo]
    if not curso["espera"]:
        print(f"El curso '{curso['nombre']}' no tiene lista de espera.")
        return

    print(f"Lista de espera de '{curso['nombre']}':")
    for posicion, dni in enumerate(curso["espera"], start=1):
        nombre = estudiantes.get(dni, {}).get("nombre", dni)
        print(f"  {posicion}. {nombre} (DNI: {dni})")



