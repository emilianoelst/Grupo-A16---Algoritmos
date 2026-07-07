![Logo](./docs/utn_frre_logo.png)

# Sistema de Inscripción a Cursos

Implementación de un escenario en el lenguaje Python para la presentación del Trabajo Práctico Integrador de Python para la cátedra Algoritmos y Estructura de Datos.

## Descripción general del sistema:

Este proyecto implementa, en Python y por consola, un sistema de inscripción a cursos o talleres. Permite:
* Registrar estudiantes (con validación de DNI y email).
* Registrar cursos con un cupo máximo de inscriptos.
* Inscribir estudiantes a cursos, controlando el cupo disponible.
* Cuando un curso está lleno, los nuevos interesados se agregan automáticamente a una lista de espera; si un inscripto se da de baja, el primero de la lista de espera pasa a ocupar el cupo liberado.
* Dar de baja inscripciones.
* Consultar el listado de cursos con su ocupación de cupos.
* Consultar la lista de espera de un curso puntual.
* Buscar un estudiante y ver en qué cursos está inscripto o en espera.
* Ver estadísticas generales: total de inscriptos, total en listas de espera, cursos con cupo completo, promedio de inscriptos por curso y el curso con mayor demanda.

Los datos (estudiantes y cursos) se guardan automáticamente en un archivo datos_sistema.json, por lo que persisten entre distintas ejecuciones del programa.

El código está modularizado en funciones (una por cada operación: validación, registro, listado, inscripción, baja, estadísticas, persistencia, etc.) e incluye manejo de errores para evitar que el programa se cierre ante datos inválidos o errores inesperados.

### Demostración Prática:

Se puede visualizar el funcionamiento completo del sistema a través del siguiente video demostrativo.

[![Video Demostrativo](https://img.youtube.com/vi/A0M79LBIUa4/2.jpg)](https://youtu.be/A0M79LBIUa4)

## Uso de Inteligencia Artificial:

Durante el desarrollo de este proyecto se utilizó Claude (Anthropic) como asistente de IA. Su uso incluyó:

* ***Para qué***: apoyar el diseño de la estructura general del sistema (organización de funciones, manejo de cupos y listas de espera) y la revisión de validaciones de datos (DNI, email, enteros). Para generar el archivo 'datos_sistema.json' como registro base para el sistema.

* ***Cómo***: se le solicitó generar una primera versión del código siguiendo la consigna de la cátedra, la cual luego fue revisada, probada y ajustada por el grupo. También se usó para verificar que el programa no presentara errores de ejecución mediante pruebas manuales de los distintos flujos del menú.

## Requisitos

* Tener instalado Python 3.8 o superior.

## Ejecutar localmente

Clona el proyecto

```bash
  git clone https://github.com/emilianoelst/Grupo-A16---Algoritmos.git
```

Ve al directorio del proyecto

```bash
  cd Grupo-A16---Algoritmos/src
```

Ejecutar el programa

```bash
  python sistema_inscripcion_cursos.py
```


## Integrantes del grupo A16 - Comision 1.1

- [Emiliano Elst](https://github.com/emilianoelst)
- [Enzo Solis](https://github.com/EnzoSolis)
- [Silva Aixa Geraldine]()
- [Pablo Sandoval Jussara Aylen]()
- [Vanesa Rocío Pereyra Aponte]()


## Licencia

[MIT](https://choosealicense.com/licenses/mit/)