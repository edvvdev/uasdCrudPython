# =====================================================================
# MAIN.PY - ORQUESTADOR PRINCIPAL
# =====================================================================
# Punto de entrada unificado para el proyecto uasdCrudPython.
# Soporta ejecución via CLI flags o menú interactivo.

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fase1 import CrudService, ExportService, MetricsService
from src.controllers import SakilaWorkflowController
from src.utils.helpers import print_header, print_subheader


def ejecutar_fase1():
    """Ejecuta todas las operaciones de la Fase I."""
    print_header("FASE I: CRUD + IMPORT/EXPORT + MÉTRICAS")

    crud = CrudService()
    export = ExportService()
    metrics = MetricsService()

    print_subheader("1. CRUD Operations")
    crud.crear_pais("Brasil")
    crud.crear_pais("Brasil")
    crud.crear_ciudad("Rio de Janeiro", 1)
    crud.actualizar_tarifa_pelicula(1, 4.99)
    paises = crud.leer_paises(3)
    print(f"Países recuperados: {len(paises)}")
    crud.eliminar_ciudad(1)

    print_subheader("2. Export/Import")
    export.exportar_a_csv("film", "data/peliculas.csv")
    export.exportar_a_json("city", "data/ciudades.json")

    print_subheader("3. Métricas Descriptivas")
    metrics.calcular_metricas_descriptivas()

    print("[FASE I] Completada exitosamente")


def ejecutar_fase2():
    """Ejecuta el flujo ORM completo de la Fase II."""
    print_header("FASE II: ARQUITECTURA ORM MODULAR")
    controlador = SakilaWorkflowController()
    controlador.procesar_flujo_completo()
    print("[FASE II] Completada exitosamente")


def ejecutar_queries():
    """Ejecuta las10 consultas SQL (mostrar query y resultado)."""
    print_header("CONSULTAS SQL -10 QUERIES ANALÍTICAS")

    queries = [
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
FROM country co LEFT JOIN city ci ON co.country_id = ci.country_id
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

    for i, (descripcion, query) in enumerate(queries, 1):
        print(f"\n--- Consulta {i}: {descripcion} ---")
        print(query.strip())


def mostrar_menu_interactivo():
    """Muestra el menú interactivo y procesa la selección del usuario."""
    while True:
        print_header("MENÚ PRINCIPAL - uasdCrudPython")
        print("  Maestría en Ciencia de Datos e Inteligencia Artificial")
        print()
        print("  1. FASE I: CRUD + Import/Export + Métricas")
        print("  2. FASE II: Arquitectura ORM")
        print("  3. CONSULTAS SQL (10 queries)")
        print("  4. DOCUMENTACIÓN")
        print("  0. Salir")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ejecutar_fase1()
        elif opcion == "2":
            ejecutar_fase2()
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
        ejecutar_fase1()
        print()
        ejecutar_fase2()
    elif args.fase1:
        ejecutar_fase1()
    elif args.fase2:
        ejecutar_fase2()
    elif args.queries:
        ejecutar_queries()
    else:
        mostrar_menu_interactivo()


if __name__ == "__main__":
    main()
