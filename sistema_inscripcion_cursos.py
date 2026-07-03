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





