# =====================================================================
# MAIN.PY - ORQUESTADOR PRINCIPAL
# =====================================================================
# Punto de entrada unificado para el proyecto uasdCrudPython.
# Soporta ejecución via CLI flags o menú interactivo.
#
# MAESTRANTES:
#   - Framiel Trinidad
#   - Edwing Perez
#   - Jharol Duran
#
# Universidad Autónoma de Santo Domingo (UASD)
# INF-8237-C2: Ciencias de Datos 1
# Profesora: Silveria del Orbe Abad

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fase1 import CrudService, ExportService, MetricsService
from src.controllers import SakilaWorkflowController
from src.utils.helpers import print_header, print_subheader
from src.dbcontext import DbContext


QUERIES = [
    ("Películas con costo de reemplazo > $15.00", """
SELECT title, release_year, replacement_cost, rating
FROM film WHERE replacement_cost > 15.00;
"""),
    ("Join ciudades con países", """
SELECT ci.city_id, ci.city, co.country
FROM city ci INNER JOIN country co ON ci.country_id = co.country_id;
"""),
    ("Ciudades por país (conteo)", """
SELECT co.country, COUNT(ci.city_id) AS total_ciudades
FROM country co LEFT JOIN city ci ON co.country_id = co.country_id
GROUP BY co.country_id ORDER BY total_ciudades DESC;
"""),
    ("Duración promedio por clasificación", """
SELECT rating, ROUND(AVG(length), 2) AS duracion_promedio
FROM film GROUP BY rating;
"""),
    ("Búsqueda por patrón en títulos", """
SELECT film_id, title, rental_rate, rating
FROM film WHERE title LIKE '%Matrix%' OR title LIKE '%Inception%';
"""),
    ("Inventario activo por tienda", """
SELECT i.inventory_id, f.title, i.store_id
FROM inventory i JOIN film f ON i.film_id = f.film_id WHERE i.store_id = 1;
"""),
    ("Películas con tarifa 3-6 y duración > 120", """
SELECT title, rental_rate, length FROM film
WHERE rental_rate BETWEEN 3.00 AND 6.00 AND length > 120;
"""),
    ("Conteo de copias por título", """
SELECT f.title, COUNT(i.inventory_id) AS copias_disponibles
FROM film f LEFT JOIN inventory i ON f.film_id = i.film_id GROUP BY f.film_id;
"""),
    ("Países sin ciudades asociadas", """
SELECT co.country FROM country co
LEFT JOIN city ci ON co.country_id = ci.country_id WHERE ci.city_id IS NULL;
"""),
    ("Máximo costo operativo", """
SELECT title, replacement_cost FROM film
WHERE replacement_cost = (SELECT MAX(replacement_cost) FROM film);
"""),
]


def ejecutar_consulta_individual(numero):
    """Ejecuta una consulta individual y muestra el resultado."""
    if numero < 1 or numero > len(QUERIES):
        print("Número de consulta inválido.")
        return

    descripcion, query = QUERIES[numero - 1]
    print_subheader(f"Consulta {numero}: {descripcion}")
    print(f"\nSQL:\n{query.strip()}\n")

    context = DbContext()
    resultados = context.ejecutar_consulta(query.strip())

    if resultados:
        print("RESULTADO:")
        for fila in resultados:
            print(f"  {fila}")
    else:
        print("Sin resultados.")


def ejecutar_queries():
    """Submenú para ejecutar consultas SQL individualmente."""
    while True:
        print_header("CONSULTAS SQL - SUBMENÚ DE 10 QUERIES")
        print()
        for i, (descripcion, _) in enumerate(QUERIES, 1):
            print(f"  {i}. {descripcion}")
        print()
        print("  A. Ejecutar TODAS las consultas")
        print("  0. Volver al menú principal")
        print()

        opcion = input("Seleccione una consulta (1-10) o 'A'/'0': ").strip()

        if opcion == "0":
            break
        elif opcion.upper() == "A":
            print_header("EJECUTANDO TODAS LAS CONSULTAS")
            context = DbContext()
            for i, (descripcion, query) in enumerate(QUERIES, 1):
                print_subheader(f"Consulta {i}: {descripcion}")
                resultados = context.ejecutar_consulta(query.strip())
                if resultados:
                    for fila in resultados:
                        print(f"  {fila}")
                else:
                    print("  Sin resultados.")
                print()
        else:
            try:
                num = int(opcion)
                ejecutar_consulta_individual(num)
            except ValueError:
                print("Opción no válida.")


# =====================================================================
# SUBMENÚ FASE I - INTERACTIVO
# =====================================================================

def submenu_fase1():
    """Submenú interactivo para operaciones de Fase I."""
    crud = CrudService()
    export = ExportService()
    metrics = MetricsService()

    while True:
        print_header("FASE I - SUBMENÚ CRUD INTERACTIVO")
        print()
        print(" 1. Crear País")
        print("  2. Leer Países")
        print("  3. Crear Ciudad")
        print("  4. Leer Ciudades")
        print("  5. Eliminar Ciudad")
        print("  6. Actualizar Tarifa Película")
        print("  7. Buscar Película por ID")
        print("  8. Exportar a CSV")
        print("  9. Exportar a JSON")
        print("  10. Métricas Descriptivas")
        print("  0. Volver al menú principal")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            print_subheader("Crear País")
            nombre = input("  Ingrese nombre del país: ").strip()
            if nombre:
                crud.crear_pais(nombre)
            else:
                print("  Nombre no puede estar vacío.")
        elif opcion == "2":
            print_subheader("Leer Países")
            limite = input("  Cantidad a mostrar (default10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            paises = crud.leer_paises(limite)
            print(f"  Países recuperados: {len(paises)}")
            for p in paises:
                print(f"    - {p.country_id}: {p.country}")
        elif opcion == "3":
            print_subheader("Crear Ciudad")
            nombre = input("  Ingrese nombre de la ciudad: ").strip()
            country_id = input("  Ingrese ID del país: ").strip()
            if nombre and country_id.isdigit():
                crud.crear_ciudad(nombre, int(country_id))
            else:
                print("  Datos inválidos.")
        elif opcion == "4":
            print_subheader("Leer Ciudades")
            limite = input("  Cantidad a mostrar (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            ciudades = crud.leer_ciudades(limite)
            print(f"  Ciudades recuperadas: {len(ciudades)}")
            for c in ciudades:
                print(f"    - {c.city_id}: {c.city} (country_id: {c.country_id})")
        elif opcion == "5":
            print_subheader("Eliminar Ciudad")
            city_id = input("  Ingrese ID de la ciudad a eliminar: ").strip()
            if city_id.isdigit():
                crud.eliminar_ciudad(int(city_id))
            else:
                print("  ID inválido.")
        elif opcion == "6":
            print_subheader("Actualizar Tarifa de Película")
            film_id = input("  Ingrese ID de la película: ").strip()
            nueva_tarifa = input("  Nueva tarifa: ").strip()
            if film_id.isdigit() and nueva_tarifa.replace('.', '').isdigit():
                crud.actualizar_tarifa_pelicula(int(film_id), float(nueva_tarifa))
            else:
                print("  Datos inválidos.")
        elif opcion == "7":
            print_subheader("Buscar Película por ID")
            film_id = input("  Ingrese ID de la película: ").strip()
            if film_id.isdigit():
                pelicula = crud.buscar_pelicula_por_id(int(film_id))
                if pelicula:
                    print(f"  {pelicula}")
                else:
                    print("  Película no encontrada.")
            else:
                print("  ID inválido.")
        elif opcion == "8":
            print_subheader("Exportar a CSV")
            tabla = input("  Nombre de la tabla (film, city, country, inventory): ").strip()
            if tabla:
                export.exportar_a_csv(tabla, f"data/{tabla}.csv")
            else:
                print("  Nombre de tabla requerido.")
        elif opcion == "9":
            print_subheader("Exportar a JSON")
            tabla = input("  Nombre de la tabla (film, city, country, inventory): ").strip()
            if tabla:
                export.exportar_a_json(tabla, f"data/{tabla}.json")
            else:
                print("  Nombre de tabla requerido.")
        elif opcion == "10":
            print_subheader("Métricas Descriptivas")
            metrics.calcular_metricas_descriptivas()
        else:
            print("Opción no válida.")


# =====================================================================
# SUBMENÚ FASE II - INTERACTIVO
# =====================================================================

def submenu_fase2():
    """Submenú interactivo para operaciones de Fase II ORM."""
    controlador = SakilaWorkflowController()

    while True:
        print_header("FASE II - SUBMENÚ ORM INTERACTIVO")
        print()
        print("  1. Crear País (Entity)")
        print("  2. Leer Países (List<CountryEntity>)")
        print("  3. Crear Ciudad (Entity)")
        print("  4. Leer Ciudades (List<CityEntity>)")
        print("  5. Buscar Película (Entity)")
        print("  6. Leer Películas (List<FilmEntity>)")
        print("  7. Actualizar Tarifa Película")
        print("  8. Eliminar Ciudad por ID")
        print("  9. Ejecutar Flujo Completo ORM")
        print("  0. Volver al menú principal")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            print_subheader("Crear País (Entity)")
            nombre = input("  Ingrese nombre del país: ").strip()
            if nombre:
                pais = controlador.crear_pais(nombre)
                print(f"  País creado: {pais}")
            else:
                print("  Nombre no puede estar vacío.")
        elif opcion == "2":
            print_subheader("Leer Países (List<CountryEntity>)")
            limite = input("  Cantidad a mostrar (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            paises = controlador.obtener_paises(limite)
            print(f"  List<CountryEntity>: {len(paises)} elementos")
            for p in paises:
                print(f"    - {p}")
        elif opcion == "3":
            print_subheader("Crear Ciudad (Entity)")
            nombre = input("  Ingrese nombre de la ciudad: ").strip()
            country_id = input("  Ingrese ID del país: ").strip()
            if nombre and country_id.isdigit():
                ciudad = controlador.crear_ciudad(nombre, int(country_id))
                print(f"  Ciudad creada: {ciudad}")
            else:
                print("  Datos inválidos.")
        elif opcion == "4":
            print_subheader("Leer Ciudades (List<CityEntity>)")
            limite = input("  Cantidad a mostrar (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            ciudades = controlador.obtener_ciudades(limite)
            print(f"  List<CityEntity>: {len(ciudades)} elementos")
            for c in ciudades:
                print(f"    - {c}")
        elif opcion == "5":
            print_subheader("Buscar Película (Entity)")
            film_id = input("  Ingrese ID de la película: ").strip()
            if film_id.isdigit():
                pelicula = controlador.obtener_pelicula(int(film_id))
                if pelicula:
                    print(f"  {pelicula}")
                else:
                    print("  Película no encontrada.")
            else:
                print("  ID inválido.")
        elif opcion == "6":
            print_subheader("Leer Películas (List<FilmEntity>)")
            limite = input("  Cantidad a mostrar (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            peliculas = controlador.obtener_peliculas(limite)
            print(f"  List<FilmEntity>: {len(peliculas)} elementos")
            for p in peliculas:
                print(f"    - {p}")
        elif opcion == "7":
            print_subheader("Actualizar Tarifa Película")
            film_id = input("  Ingrese ID de la película: ").strip()
            nueva_tarifa = input("  Nueva tarifa: ").strip()
            if film_id.isdigit() and nueva_tarifa.replace('.', '').isdigit():
                if controlador.actualizar_tarifa(int(film_id), float(nueva_tarifa)):
                    print("  Tarifa actualizada exitosamente.")
                else:
                    print("  No se pudo actualizar.")
            else:
                print("  Datos inválidos.")
        elif opcion == "8":
            print_subheader("Eliminar Ciudad por ID")
            city_id = input("  Ingrese ID de la ciudad: ").strip()
            if city_id.isdigit():
                if controlador.eliminar_ciudad(int(city_id)):
                    print("  Ciudad eliminada.")
                else:
                    print("  No se pudo eliminar (posible FK constraint).")
            else:
                print("  ID inválido.")
        elif opcion == "9":
            print_subheader("Ejecutar Flujo Completo ORM")
            controlador.procesar_flujo_completo()
        else:
            print("Opción no válida.")


def mostrar_menu_interactivo():
    """Muestra el menú interactivo y procesa la selección del usuario."""
    while True:
        print_header("MENÚ PRINCIPAL - uasdCrudPython")
        print("  Maestría en Ciencia de Datos e Inteligencia Artificial")
        print()
        print(" 1. FASE I: CRUD + Import/Export + Métricas")
        print("2. FASE II: Arquitectura ORM")
        print("  3. CONSULTAS SQL (10 queries)")
        print("  4. DOCUMENTACIÓN")
        print("  0. Salir")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            submenu_fase1()
        elif opcion == "2":
            submenu_fase2()
        elif opcion == "3":
            ejecutar_queries()
        elif opcion == "4":
            print("\nDocumentación disponible en:")
            print("  - docs/README.md")
            print("  - docs/DESIGN.md")
            print("  - docs/criterios.md")
            print("  - docs/ensayo/ensayo.md")
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Intente de nuevo.")


def main():
    """Entry point principal con soporte para CLI flags."""
    parser = argparse.ArgumentParser(
        description="uasdCrudPython - CRUD/ORM nativo en Python con MariaDB"
    )
    parser.add_argument(
        "--fase1", action="store_true",
        help="Ejecutar Fase I (CRUD + Import/Export + Métricas)"
    )
    parser.add_argument(
        "--fase2", action="store_true",
        help="Ejecutar Fase II (Arquitectura ORM)"
    )
    parser.add_argument(
        "--queries", action="store_true",
        help="Mostrar las 10 consultas SQL"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Ejecutar todas las fases"
    )
    parser.add_argument(
        "--menu", action="store_true",
        help="Forzar menú interactivo"
    )

    args = parser.parse_args()

    if args.all:
        submenu_fase1()
        print()
        submenu_fase2()
    elif args.fase1:
        submenu_fase1()
    elif args.fase2:
        submenu_fase2()
    elif args.queries:
        ejecutar_queries()
    else:
        mostrar_menu_interactivo()


if __name__ == "__main__":
    main()
