# =====================================================================
# FASE1_MAIN.PY - VALIDACIÓN DE FASE I (SAKILA COMPLETO)
# =====================================================================
# Punto de entrada para validación de Fase I: CRUD + Import/Export + Métricas
#
# MAESTRANTES:
#   - Framiel Trinidad
#   - Edwing Perez
#   - Jharol Duran
#
# Universidad Autónoma de Santo Domingo (UASD)
# INF-8237-C2: Ciencias de Datos 1
# Profesora: Silveria del Orbe Abad

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fase1 import CrudService, ExportService, MetricsService
from src.utils.helpers import clear_screen, pausa


def main():
    """Ejecuta la validación completa de la Fase I."""
    clear_screen()
    print("=" * 60)
    print("   PROCESANDO VALIDACION DE LA FASE I - SAKILA COMPLETO")
    print("=" * 60)
    print()

    crud = CrudService()
    export = ExportService()
    metrics = MetricsService()

    # === COUNTRY ===
    print("[COUNTRY] Intentando crear país duplicado (UNIQUE constraint)...")
    crud.crear_pais("Brasil")
    print()

    # === CITY ===
    print("[CITY] Creando ciudad vinculada a país...")
    crud.crear_ciudad("Santo Domingo", 1)
    print()

    # === FILM ===
    print("[FILM] Actualizando película ID 1...")
    crud.actualizar_tarifa_pelicula(1, 4.99)
    print()

    print("[FILM] Buscando película por ID...")
    pelicula = crud.buscar_pelicula_por_id(1)
    if pelicula:
        print(f"   Encontrada: {pelicula}")
    print()

    # === ACTOR ===
    print("[ACTOR] Creando actor...")
    actor = crud.crear_actor("Keanu", "Reeves")
    print()

    print("[ACTOR] Leyendo actores...")
    actores = crud.leer_actores(5)
    for a in actores:
        print(f"   {a}")
    print()

    # === CATEGORY ===
    print("[CATEGORY] Creando categoría...")
    crud.crear_categoria("Sci-Fi")
    print()

    print("[CATEGORY] Leyendo categorías...")
    cats = crud.leer_categorias(10)
    for c in cats:
        print(f"   {c}")
    print()

    # === STAFF ===
    print("[STAFF] Creando empleado...")
    crud.crear_staff("Pedro", "Martinez", 1, 1, "PedroM")
    print()

    # === CUSTOMER ===
    print("[CUSTOMER] Creando cliente...")
    crud.crear_cliente(1, "Juan", "Perez", 1, "juan@email.com")
    print()

    # === RENTAL ===
    print("[RENTAL] Creando alquiler...")
    crud.crear_alquiler(1, 1, 1)
    print()

    print("[RENTAL] Leyendo alquileres activos...")
    activos = crud.leer_alquileres_activos()
    print(f"   Activos: {len(activos)}")
    print()

    # === PAYMENT ===
    print("[PAYMENT] Creando pago...")
    crud.crear_pago(1, 1, 4.99)
    print()

    print("[PAYMENT] Total gastado por cliente 1:")
    total = crud.total_pagos_cliente(1)
    print(f"   ${total:.2f}")
    print()

    # === DELETE ===
    print("[DELETE] Eliminando ciudad con ID 1...")
    crud.eliminar_ciudad(1)
    print()

    # === EXPORT ===
    print("[EXPORT CSV] Exportando tabla 'film'...")
    export.exportar_a_csv("film", "data/peliculas_fase1.csv")
    print()

    print("[EXPORT JSON] Exportando tabla 'city'...")
    export.exportar_a_json("city", "data/ciudades_fase1.json")
    print()

    # === MÉTRICAS ===
    print("=" * 60)
    print("      REPORTING ESTADISTICO - FILM")
    print("=" * 60)
    metrics.calcular_metricas_descriptivas()

    print("=" * 60)
    print("      REPORTING ESTADISTICO - PAYMENTS")
    print("=" * 60)
    metrics.metricas_payments()

    print("=" * 60)
    print("      REPORTING ESTADISTICO - DURACIÓN ALQUILERES")
    print("=" * 60)
    metrics.metricas_rental_duration()

    print("=" * 60)
    print("      REPORTING ESTADISTICO - INVENTARIO POR TIENDA")
    print("=" * 60)
    metrics.metricas_inventory_by_store()

    print()
    print("=" * 60)
    print("--- FASE I COMPLETADA CON EXITO ---")
    print("=" * 60)


if __name__ == "__main__":
    main()
