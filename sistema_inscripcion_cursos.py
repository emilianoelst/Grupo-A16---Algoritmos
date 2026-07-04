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
import sys
import re
from dataclasses import dataclass, asdict

# Utilidades
def limpiar_pantalla():
  """
  Limpia la terminal
  """
  
  try:
    comando = "cls" if os.name == "nt" else "clear"
    resultado = os.system(comando)
    
    if resultado != 0:
      raise RuntimeError("Comando no disponible")
  except Exception:
    sys.stdout.write("\033[H\033[2J")
    sys.stdout.flush()


def leer_confirmacion(etiqueta : str) -> bool:
  """
  Espera una confirmación del usuario.
  """
  while True:
    entrada = input(f"{etiqueta} (S, n): ").strip().lower()
    
    if entrada in ["s", "n", ""]:
      return entrada != "n"


# =======================================================================
# REGISTROS: Estudiante y Curso
# =======================================================================

# NOTE: Registros Antes (Diccionario)
# estudiante = {"nombre": "Ana Pérez", "email": "ana@mail.com"}
# curso = { "nombre": "Python Inicial", "cupo": 20, "inscriptos": [], "espera": [] }

# NOTE: Registros Ahora (dataclasses)
@dataclass
class Estudiante:
    """
    Registro que contiene los datos de un estudiante.
    """
    nombre: str
    email: str

    
@dataclass
class Curso:
    """
    Registro que contiene los datos de un curso.
    """
    nombre: str
    cupo: int
    inscriptos: list[str]
    espera: list[str]


# =======================================================================
# ARCHIVOS: Base de datos en memoria interna del Sistema.
# ---------------------------------------------------------------------
# Formato del archivo en JSON
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
# =======================================================================
RUTA_ARCHIVO_DATOS = "datos_sistema.json"

estudiantes : dict[str, Estudiante] = {}
cursos : dict[str, Curso] = {}


def cargar_datos():
    """Carga estudiantes y cursos desde el archivo JSON, si existe."""
    
    # NOTE: No hace falta el global si la función no reasigna la variable.
    #global estudiantes, cursos
    try:
        # Caso 1: Existe el archivo y lo lee.
        with open(RUTA_ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            estudiantes_dicts = datos.get("estudiantes", {})
            cursos_dicts = datos.get("cursos", {})
            
            # Convertir los diccionarios en registros. (Deserialización)
            for dni, datos_estudiante in estudiantes_dicts.items():
                estudiantes[dni] = Estudiante(**datos_estudiante)
            
            for codigo, datos_estudiante in cursos_dicts.items():
                cursos[codigo] = Curso(**datos_estudiante)
            
            print("INFO: Los datos se cargaron con éxito.")
            _ = input("\nPresione enter para continuar...")

    except (json.JSONDecodeError, OSError) as error:
        # Caso 2: El archivo no existe o no es 
        print(f"ADVERTENCIA: NO se cargaron los datos del sistema. Mensaje: {error}")
        _ = input("\nPresione enter para continuar...")


def guardar_datos():
    """Guarda estudiantes y cursos en el archivo JSON."""

    try:
        with open(RUTA_ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
            # Convertir los registros en diccionarios. (Serialización)
            estudiantes_dict = {}
            cursos_dict = {}
            
            # NOTE: Con una compresión de diccionarios se puede hacer lo mismo, 
            # pero mantenemos el for para facilitar su lectura y comparación con el pseudocódigo.
            for dni, estudiante in estudiantes.items():
                estudiantes_dict[dni] = asdict(estudiante)
                
            for codigo, curso in cursos.items():
                cursos_dict[codigo] = asdict(curso)
            
            json.dump(
                {"estudiantes": estudiantes_dict, "cursos": cursos_dict},
                archivo, ensure_ascii=False, indent=4
            )

        print("INFO: Los datos se guardaron con éxito")
        
    except OSError as error:
        print(f"ERROR: No se guardaron los datos. Mensaje: {error}")


# =======================================================================
# FUNCIONES DE VALIDACIÓN
# =======================================================================

def validar_dni(dni):
    """Un DNI válido: solo dígitos, entre 7 y 8 caracteres."""
    return dni.isdecimal() and (7 <= len(dni) <= 8)


def validar_email(email):
    """Validación básica de formato de email con expresión regular."""
    # NOTE: expresión regular? 
    patron = r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$"
    return re.match(patron, email) is not None


# =======================================================================
# FUNCIONES DE ENTRADA
# =======================================================================

def pedir_entero(mensaje, minimo=None, maximo=None) -> int:
    """Pide un número entero por consola, repite hasta obtener uno válido."""
    
    while True:
        entrada = input(mensaje).strip()
        try:
            numero = int(entrada)
            
            if minimo is not None and numero < minimo:
                print(f"ADVERTENCIA: el número ingresado fuera de rango. El valor debe ser mayor o igual a {minimo}.")
                continue
            
            if maximo is not None and numero > maximo:
                print(f"ADVERTENCIA: el número ingresado fuera de rango. El valor ingresado debe ser menor o igual a {maximo}.")
                continue
            
            return numero
        
        except ValueError:
            print("ERROR: debe ingresar un número entero válido.")


def pedir_texto(mensaje) -> str:
    """Pide un texto no vacío por consola."""
    while True:
        texto = input(mensaje).strip()
        if len(texto) != 0:
            return texto
        print("ADVERTENCIA: El campo no puede estar vacío.")


def pedir_dni(validar_si_esta_registrado = False) -> str:
    """Pide un DNI válido por consola."""
    while True:
        dni = input("DNI: ").strip()
        
        if validar_si_esta_registrado and dni in estudiantes:
            print(f"ADVERTENCIA: Ya existe un estudiante registrado con DNI {dni} ({estudiantes[dni].nombre}).")
            continue
        
        if validar_dni(dni):
            return dni
        
        print("ADVERTENCIA: El DNI debe contener solo números (7 u 8 dígitos).")


def pedir_email(mensaje) -> str:
    """Pide un email válido por consola."""
    while True:
        email = input(mensaje).strip()
        
        if validar_email(email):
            return email
        
        print("ADVERTENCIA: formato de email inválido (ejemplo: nombre@dominio.com).")


def pedir_curso() -> Curso|None:
    """Pide un código de curso y valida que exista. Devuelve el código o None."""
    
    if not cursos:
        print("INFO: No hay cursos registrados todavía.")
        return None

    while True:
        codigo = pedir_texto("Código del curso: ").upper()
    
        if codigo not in cursos:
            print(f"ADVERTENCIA: No existe un curso con código {codigo}.")
            
            if not leer_confirmacion("Intentar de nuevo?"):
                return None
        else:
            return cursos[codigo]


# =======================================================================
# GESTIÓN DE ESTUDIANTES
# =======================================================================

def registrar_estudiante():
    """Registra un nuevo estudiante en el sistema."""
    while True:
        limpiar_pantalla()
        
        print("\n--- Registro de Estudiante ---")
        
        dni = pedir_dni(validar_si_esta_registrado=True)
        nombre = pedir_texto("Nombre y apellido: ")
        email = pedir_email("Email: ")

        estudiantes[dni] = Estudiante(nombre=nombre, email=email)
        guardar_datos()
        print(f"Estudiante '{nombre}' registrado con éxito (DNI: {dni}).")
        
        if not leer_confirmacion("Registrar otro estudiante?"):
            return


def listar_estudiantes():
    """Muestra todos los estudiantes registrados."""
    limpiar_pantalla()
    
    print(" Listado de Estudiantes ".center(45, "="))
    
    # Caso 1: No hay estudiantes registrados
    if len(estudiantes) == 0:
        print("No hay estudiantes registrados.")
        _ = input("\nPresione enter para volver...")
        return

    # Caso 2: Hay estudiantes registrados, mostrar lista.
    contador = 0
    for dni, estudiante in estudiantes.items():
        contador += 1
        print(f"{contador}. DNI: {dni} | Nombre: {estudiante.nombre} | Email: {estudiante.email}")
    
    print("=" * 45)
    print(f"Total de estudiantes: {contador}")
    print("=" * 45)
    _ = input("\nPresione enter para volver...")


def buscar_estudiante_interactivo():
    """Busca un estudiante por DNI y muestra sus datos e inscripciones."""
    
    while True:
        limpiar_pantalla()
        print("--- Buscar Estudiante ---\n")
        dni = pedir_dni()
        
        # Caso 1: El estudiante no está registrado.
        if dni not in estudiantes:
            print("INFO: No se encontró ningún estudiante con ese DNI.")
            if leer_confirmacion("Buscar otra vez?"):
                continue
            return
        
        # Caso 2: Estudiante está registrado.
        estudiante = estudiantes[dni]
        print(f"Nombre: {estudiante.nombre} | Email: {estudiante.email}")

        cursos_inscripto = []
        cursos_en_espera = []
        for codigo, curso in cursos.items():
            if dni in curso.inscriptos:
                cursos_inscripto.append(curso.nombre)
            if dni in curso.espera:
                cursos_en_espera.append(curso.nombre)

        if cursos_inscripto:
            print("Cursos inscripto:", ", ".join(cursos_inscripto))
        else:
            print("No tiene inscripciones activas.")

        if cursos_en_espera:
            print("En lista de espera de:", ", ".join(cursos_en_espera))
            
        if not leer_confirmacion("Buscar otra vez?"):
            return


# =======================================================================
# GESTIÓN DE CURSOS
# =======================================================================

def registrar_curso():
    """Registra un nuevo curso con su cupo máximo."""
    
    while True:
        limpiar_pantalla()
        print("--- Registro de Curso ---\n")
        codigo = pedir_texto("Código del curso (ej: PY101): ").upper()

        # Caso 1: El código no está disponible.
        if codigo in cursos:
            print(f"Ya existe un curso con el código {codigo}.")
            if not leer_confirmacion("Intentar con otro código?"):
                return

        # Caso 2: El código está disponible.
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
        
        if not leer_confirmacion("Registrar otro curso?"):
            return


def listar_cursos():
    """Muestra todos los cursos con su ocupación de cupos."""
    
    limpiar_pantalla()
    print("--- Listado de Cursos ---")
    
    # Caso 1: No hay cursos registrados
    if not cursos:
        print("INFO: No hay cursos registrados.")
        _ = input("\nPresione enter para volver...")
        return

    # Caso 2: Hay cursos registrados
    for codigo, curso in cursos.items():
        ocupados = len(curso.inscriptos)
        disponibles = curso.cupo - ocupados
        en_espera = len(curso.espera)
        estado = "CUPO LLENO" if disponibles <= 0 else f"{disponibles} lugares libres"
        print(f"[{codigo}] {curso.nombre} | Cupo: {curso.cupo} | Inscriptos: {ocupados} | {estado} | En espera: {en_espera}")
    
    _ = input("\nPresione enter para volver...") 


# =======================================================================
# GESTIÓN DE INSCRIPCIONES Y LISTA DE ESPERA
# =======================================================================

def esta_inscripto(dni, curso) -> bool:
    """Comprueba si un estudiante ya se encuentra inscripto a un curso."""

    if dni in curso["inscriptos"]:
        print(f"El estudiante ya está inscripto en '{curso['nombre']}'.")
        return True
        
    if dni in curso["espera"]:
        print(f"El estudiante ya está en la lista de espera de '{curso['nombre']}'.")
        return True
    
    return False


def inscribir(dni, curso):
    if len(curso["inscriptos"]) < curso["cupo"]:
        curso["inscriptos"].append(dni)
        print(f"INFO: Inscripción exitosa en '{curso['nombre']}'.")
    else:
        curso["espera"].append(dni)
        posicion = len(curso["espera"]) + 1
        print(f"INFO: Cupo lleno. El estudiante fue agregado a la lista de espera "
            f"en la posición {posicion}.")
    
    guardar_datos()


def inscribir_estudiante():
    """Inscribe un estudiante a un curso, o lo agrega a la lista de espera
    si el cupo está lleno."""
    
    while True:
        limpiar_pantalla()
        print("--- Inscripción a Curso ---")

        dni = pedir_dni()
        if dni not in estudiantes:
            print("ADVERTENCIA: DNI ingresado no corresponde a un estudiante registrado.")
            
            if not leer_confirmacion("Continuar inscribiendo?"):
                return

        curso = pedir_curso()
        if curso is None:
            return

        if not esta_inscripto(dni, curso):
            inscribir(dni, curso)

        if not leer_confirmacion("Continuar inscribiendo?"):
            break


def dar_baja_inscripcion():
    """Da de baja a un estudiante de un curso. Si hay lista de espera,
    promueve automáticamente al primero de la lista."""
    
    while True:
        limpiar_pantalla()
        print("--- Baja de Inscripción ---")

        curso = pedir_curso()
        if curso is None:
            return
        
        dni = pedir_dni(validar_si_esta_registrado=True)
        
        # NOTE: Al ser excluyentes los dos estados (inscripto y en espera), se elimina el elif
        
        # Caso 1: No está inscripto
        if not (dni in curso.inscriptos or dni in curso.espera):
            print("INFO: Ese estudiante no está inscripto ni en espera en este curso.")
        
        # Caso 2: La inscripción está aceptada
        if dni in curso.inscriptos:
            curso.inscriptos.remove(dni)
            estudiante = estudiantes[dni]
            
            print(f"INFO: Se dio de baja a {estudiante.nombre} de '{curso.nombre}'.")

            # TODO: Preguntar si desea promover automáticamente o manualmente
            # Si hay lista de espera, se promueve automáticamente al primero
            if len(curso.espera) > 0:
                siguiente_dni = curso.espera.pop(0)
                curso.inscriptos.append(siguiente_dni)
                print(f"INFO: Se liberó un cupo: estudiante con DNI:{siguiente_dni} fue promovido automáticamente desde la lista de espera.")
            
            guardar_datos()

        # Caso 3: La inscripción está en espera
        if dni in curso.espera:
            curso.espera.remove(dni)
            guardar_datos()
            print(f"INFO: El estudiante con DNI:{dni} fue removido de la lista de espera.")
        
        if not leer_confirmacion("Continuar dando de baja?"):
            break


def ver_lista_espera():
    """Muestra la lista de espera de un curso puntual."""
    
    limpiar_pantalla()
    print("--- Lista de Espera ---")
    
    curso = pedir_curso()
    if curso is None:
        return

    # Caso 1: Lista de espera vacía
    if len(curso.espera) == 0:
        print(f"El curso '{curso.nombre}' no tiene lista de espera.")
        _ = input("\nPresione enter para volver...")
        return
        
    # Caso 2: El curso tiene inscripciones en espera. Mostrar
    print(f"Lista de espera de '{curso.nombre}':")
    for posicion, dni in enumerate(curso.espera, start=1):
        estudiante = estudiantes[dni]
        print(f"  {posicion}. {estudiante.nombre} (DNI: {dni})")
    
    _ = input("\nPresione enter para volver...")


# =======================================================================
# ESTADÍSTICAS
# =======================================================================

def mostrar_estadisticas():
    """Calcula y muestra estadísticas generales del sistema usando
    acumuladores y contadores."""
    
    limpiar_pantalla()
    print("--- Estadísticas del Sistema ---")

    if len(cursos) == 0:
        print("INFO: No hay cursos registrados todavía.")
        _ = input("\nPresione enter para volver...")

    total_cursos = 0
    total_inscriptos = 0          # acumulador de inscripciones totales
    total_en_espera = 0           # acumulador de gente en espera
    cursos_llenos = 0             # contador de cursos con cupo lleno
    curso_mas_demandado = None
    max_demanda = -1

    for codigo, curso in cursos.items():
        total_cursos += 1
        cantidad_inscriptos = len(curso.inscriptos)
        cantidad_espera = len(curso.espera)

        total_inscriptos += cantidad_inscriptos
        total_en_espera += cantidad_espera

        if cantidad_inscriptos >= curso.cupo:
            cursos_llenos += 1

        # La demanda se mide como inscriptos + gente en espera
        demanda = cantidad_inscriptos + cantidad_espera
        if demanda > max_demanda:
            max_demanda = demanda
            curso_mas_demandado = curso.nombre

    # NOTE: Cambio del operador ternario a un if simple. Motivo: Mantener la fácil comparación con el pseudocódigo.
    promedio_ocupacion = 0
    if total_cursos != 0:
        promedio_ocupacion = total_inscriptos / total_cursos

    print(f"Total de cursos registrados: {total_cursos}")
    print(f"Total de estudiantes registrados: {len(estudiantes)}")
    print(f"Total de inscripciones activas: {total_inscriptos}")
    print(f"Total de estudiantes en listas de espera: {total_en_espera}")
    print(f"Cursos con cupo completo: {cursos_llenos}")
    print(f"Promedio de inscriptos por curso: {promedio_ocupacion:.2f}")
    if curso_mas_demandado is not None and max_demanda > 0:
        print(f"Curso con mayor demanda: '{curso_mas_demandado}' "
              f"({max_demanda} personas entre inscriptos y en espera)")
        
    _ = input("\nPresione enter para volver...")


# =======================================================================
# MENÚ PRINCIPAL
# =======================================================================

def acerca_de():
  """
  Imprime en pantalla sobre el programa y los integrantes del grupo.
  """
  limpiar_pantalla()
  
  ascii_art_grupo= """
 ▄▄▄▄▄▄▄ ▄▄▄▄ ▄▄▄     
█       █    █   █    
█   ▄   ██   █   █▄▄▄ 
█  █▄█  ██   █    ▄  █
█       ██   █   █ █ █
█   ▄   ██   █   █▄█ █
█▄▄█ █▄▄██▄▄▄█▄▄▄▄▄▄▄█
  """
  
  print(ascii_art_grupo)
  print("\033[1mSISTEMA DE INSCRIPCIÓN A CURSOS\033[0m")
  
  print("\nIntegrantes Grupo A16: ")
  print("• Enzo Solis")
  print("• Emiliano Elst")
  print("• Jussara Aylen Pablo Sandoval")
  print("• Vanesa Rocío Pereyra Aponte")
  print("• Aixa Geraldine Silva")
  
  print("\nAlgoritmos y Estructura de Datos")
  print("Ingeniería en Sistemas de Información")
  print("UTN FRRE\n2026")
  
  _ = input("\nPresione enter para volver...")


def salir():
    guardar_datos()
    print("INFO: Saliendo del programa...")
    sys.exit(0)


def mostrar_menu():
    """Imprime en pantalla las operaciones disponibles."""
    limpiar_pantalla()
    print("=" * 45)
    print(" SISTEMA DE INSCRIPCIÓN A CURSOS Y TALLERES")
    print("=" * 45)
    print("OPCIÓN - OPERACIÓN")
    print(" 1 - Registrar estudiante")
    print(" 2 - Listar estudiantes")
    print(" 3 - Buscar estudiante")
    print(" 4 - Registrar curso")
    print(" 5 - Listar cursos y cupos")
    print(" 6 - Inscribir estudiante a curso")
    print(" 7 - Dar de baja una inscripción")
    print(" 8 - Ver lista de espera de un curso")
    print(" 9 - Ver estadísticas")
    print(" A - Acerca de")
    print(" Q - Salir")
    print("=" * 45)


def ejecutar_operacion(opcion):
    """Ejecuta una operación del sistema según la opción."""
    
    # Simular un match o switch para las versiones de python<=3.9
    operaciones = {
        "1": registrar_estudiante,
        "2": listar_estudiantes,
        "3": buscar_estudiante_interactivo,
        "4": registrar_curso,
        "5": listar_cursos,
        "6": inscribir_estudiante,
        "7": dar_baja_inscripcion,
        "8": ver_lista_espera,
        "9": mostrar_estadisticas,
        "A": acerca_de,
        "Q": salir
    }
    
    if not opcion in operaciones:
        print("ADVERTENCIA: Opción inválida. Por favor ingrese una de las opciones del menú.")
        _ = input("Presione enter para continuar...")
        return
    
    operaciones[opcion]()


def main():
    """Función principal: bucle del menú con manejo de errores."""
    cargar_datos()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        ejecutar_operacion(opcion)


if __name__ == "__main__":
    main()
