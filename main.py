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
# SUBMENÚ FASE I
# =====================================================================

def submenu_fase1():
    """Submenú para operaciones de Fase I."""
    crud = CrudService()
    export = ExportService()
    metrics = MetricsService()

    while True:
        print_header("FASE I - SUBMENÚ")
        print()
        print("  1. CRUD Countries (Create, Read)")
        print("  2. CRUD Cities (Create, Read, Delete)")
        print("  3. CRUD Films (Update)")
        print("  4. Exportar a CSV")
        print("  5. Exportar a JSON")
        print("  6. Métricas Descriptivas")
        print("  A. Ejecutar TODO (completo)")
        print("  0. Volver al menú principal")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            print_subheader("CRUD Countries")
            crud.crear_pais("Argentina")
            paises = crud.leer_paises(5)
            print(f"Países recuperados: {len(paises)}")
        elif opcion == "2":
            print_subheader("CRUD Cities")
            crud.crear_ciudad("Buenos Aires", 10)
            ciudades = crud.leer_ciudades(5)
            print(f"Ciudades recuperadas: {len(ciudades)}")
        elif opcion == "3":
            print_subheader("CRUD Films - Actualizar tarifa")
            crud.actualizar_tarifa_pelicula(1, 5.99)
            pelicula = crud.buscar_pelicula_por_id(1)
            print(f"Película: {pelicula}")
        elif opcion == "4":
            print_subheader("Exportar a CSV")
            export.exportar_a_csv("film", "data/peliculas.csv")
        elif opcion == "5":
            print_subheader("Exportar a JSON")
            export.exportar_a_json("city", "data/ciudades.json")
        elif opcion == "6":
            print_subheader("Métricas Descriptivas")
            metrics.calcular_metricas_descriptivas()
        elif opcion.upper() == "A":
            print_subheader("Ejecutando FASE I completa")
            crud.crear_pais("Uruguay")
            paises = crud.leer_paises(3)
            print(f"Países: {len(paises)}")
            export.exportar_a_csv("film", "data/peliculas.csv")
            export.exportar_a_json("city", "data/ciudades.json")
            metrics.calcular_metricas_descriptivas()
            print("[FASE I] Completada exitosamente")
        else:
            print("Opción no válida.")


# =====================================================================
# SUBMENÚ FASE II
# =====================================================================

def submenu_fase2():
    """Submenú para operaciones de Fase II."""
    controlador = SakilaWorkflowController()

    while True:
        print_header("FASE II - SUBMENÚ ORM")
        print()
        print("  1. Gestionar Countries (Entity)")
        print("  2. Gestionar Cities (Entity)")
        print("  3. Gestionar Films (Entity)")
        print("  4. Ver List<Entity>")
        print("  5. Ejecutar flujo completo ORM")
        print("  0. Volver al menú principal")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            print_subheader("Gestionar Country Entity")
            pais = controlador.crear_pais("Chile")
            print(f"País creado: {pais}")
            paises = controlador.obtener_paises(3)
            print(f"Países en sistema: {len(paises)}")
        elif opcion == "2":
            print_subheader("Gestionar City Entity")
            ciudad = controlador.crear_ciudad("Santiago", 1)
            print(f"Ciudad creada: {ciudad}")
        elif opcion == "3":
            print_subheader("Gestionar Film Entity")
            pelicula = controlador.obtener_pelicula(1)
            print(f"Película recuperada: {pelicula}")
            if pelicula:
                controlador.actualizar_tarifa(1, 6.99)
                print("Tarifa actualizada")
        elif opcion == "4":
            print_subheader("Ver List<Entity>")
            paises = controlador.obtener_paises(5)
            print(f"List<CountryEntity>: {len(paises)} elementos")
            for p in paises:
                print(f"  {p}")
            peliculas = controlador.obtener_peliculas(3)
            print(f"List<FilmEntity>: {len(peliculas)} elementos")
            for p in peliculas:
                print(f"  {p}")
        elif opcion == "5":
            print_subheader("Flujo Completo ORM")
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
        print("  2. FASE II: Arquitectura ORM")
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
