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
from src.utils.helpers import print_header, print_subheader, clear_screen, pausa
from src.dbcontext import DbContext
from src.models import DataRepository


QUERIES_ORIGINALES = [
    ("Películas con costo > $15.00", """
SELECT title, release_year, replacement_cost, rating
FROM film WHERE replacement_cost > 15.00;
"""),
    ("Ciudades con países (JOIN)", """
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
    ("Búsqueda por título (Matrix/Inception)", """
SELECT film_id, title, rental_rate, rating
FROM film WHERE title LIKE '%Matrix%' OR title LIKE '%Inception%';
"""),
    ("Inventario activo Tienda 1", """
SELECT i.inventory_id, f.title, i.store_id
FROM inventory i JOIN film f ON i.film_id = f.film_id WHERE i.store_id = 1;
"""),
    ("Películas tarifa 3-6 y duración > 120", """
SELECT title, rental_rate, length FROM film
WHERE rental_rate BETWEEN 3.00 AND 6.00 AND length > 120;
"""),
    ("Conteo de copias por título", """
SELECT f.title, COUNT(i.inventory_id) AS copias_disponibles
FROM film f LEFT JOIN inventory i ON f.film_id = i.film_id GROUP BY f.film_id;
"""),
    ("Países sin ciudades", """
SELECT co.country FROM country co
LEFT JOIN city ci ON co.country_id = ci.country_id WHERE ci.city_id IS NULL;
"""),
    ("Máximo costo de reemplazo", """
SELECT title, replacement_cost FROM film
WHERE replacement_cost = (SELECT MAX(replacement_cost) FROM film);
"""),
]

QUERIES_EXTENDIDAS = [
    ("Actores por película", """
SELECT f.title, a.first_name, a.last_name
FROM film f INNER JOIN film_actor fa ON f.film_id = fa.film_id
INNER JOIN actor a ON fa.actor_id = a.actor_id ORDER BY f.title;
"""),
    ("Categorías por película", """
SELECT f.title, c.name AS category
FROM film f INNER JOIN film_category fc ON f.film_id = fc.film_id
INNER JOIN category c ON fc.category_id = c.category_id ORDER BY f.title;
"""),
    ("Películas por actor (Reeves)", """
SELECT a.first_name, a.last_name, f.title
FROM actor a INNER JOIN film_actor fa ON a.actor_id = fa.actor_id
INNER JOIN film f ON fa.film_id = f.film_id WHERE a.last_name LIKE '%Reeves%';
"""),
    ("Staff activo por tienda", """
SELECT s.username, s.first_name, s.last_name, st.store_id
FROM staff s INNER JOIN store st ON s.store_id = st.store_id WHERE s.active = 1;
"""),
    ("Direcciones completas (JOIN)", """
SELECT a.address, a.district, a.phone, c.city, co.country
FROM address a INNER JOIN city c ON a.city_id = c.city_id
INNER JOIN country co ON c.country_id = co.country_id;
"""),
    ("Clientes por tienda", """
SELECT c.first_name, c.last_name, c.email, st.store_id
FROM customer c INNER JOIN store st ON c.store_id = st.store_id ORDER BY st.store_id;
"""),
    ("Alquileres activos (sin devolver)", """
SELECT r.rental_id, r.rental_date, f.title, c.first_name, c.last_name
FROM rental r INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
INNER JOIN customer c ON r.customer_id = c.customer_id WHERE r.return_date IS NULL;
"""),
    ("Historial de pagos por cliente", """
SELECT c.first_name, c.last_name, p.amount, p.payment_date
FROM payment p INNER JOIN customer c ON p.customer_id = c.customer_id
ORDER BY c.customer_id, p.payment_date;
"""),
    ("Total ingresos por tienda", """
SELECT st.store_id, SUM(p.amount) AS total_ingresos
FROM payment p INNER JOIN staff s ON p.staff_id = s.staff_id
INNER JOIN store st ON s.store_id = st.store_id GROUP BY st.store_id;
"""),
    ("Empleado con más alquileres", """
SELECT s.first_name, s.last_name, COUNT(r.rental_id) AS total_alquileres
FROM staff s INNER JOIN rental r ON s.staff_id = r.staff_id
GROUP BY s.staff_id ORDER BY total_alquileres DESC;
"""),
    ("Cliente que más gasta", """
SELECT c.first_name, c.last_name, SUM(p.amount) AS total_gastado
FROM customer c INNER JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id ORDER BY total_gastado DESC;
"""),
    ("Películas más alquiladas", """
SELECT f.title, COUNT(r.rental_id) AS veces_alquilada
FROM film f INNER JOIN inventory i ON f.film_id = i.film_id
INNER JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id ORDER BY veces_alquilada DESC;
"""),
    ("Top 3 categorías populares", """
SELECT c.name, COUNT(r.rental_id) AS alquileres
FROM category c INNER JOIN film_category fc ON c.category_id = fc.category_id
INNER JOIN film f ON fc.film_id = f.film_id INNER JOIN inventory i ON f.film_id = i.film_id
INNER JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY c.category_id ORDER BY alquileres DESC LIMIT 3;
"""),
    ("Duración promedio por categoría", """
SELECT c.name, ROUND(AVG(f.length), 2) AS duracion_promedio
FROM category c INNER JOIN film_category fc ON c.category_id = fc.category_id
INNER JOIN film f ON fc.film_id = f.film_id GROUP BY c.category_id;
"""),
    ("Rental completo con detalles", """
SELECT r.rental_id, r.rental_date, r.return_date, f.title,
       c.first_name AS cliente_nombre, c.last_name AS cliente_apellido,
       s.username AS atendido_por
FROM rental r INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id INNER JOIN customer c ON r.customer_id = c.customer_id
INNER JOIN staff s ON r.staff_id = s.staff_id ORDER BY r.rental_date DESC;
"""),
]


def ejecutar_consulta(descripcion, query):
    """Ejecuta una consulta y muestra resultados."""
    print_subheader(descripcion)
    context = DbContext()
    resultados = context.ejecutar_consulta(query.strip())
    if resultados:
        for fila in resultados:
            print(f"  {fila}")
    else:
        print("  Sin resultados.")
    print()


def ejecutar_queries():
    """Submenú para ejecutar consultas SQL."""
    clear_screen()
    while True:
        print_header("CONSULTAS SQL - SAKILA COMPLETO")
        print()
        print(" [CONSULTAS BÁSICAS (1-10)]")
        for i, (desc, _) in enumerate(QUERIES_ORIGINALES, 1):
            print(f"  {i:2d}. {desc}")
        print()
        print(" [CONSULTAS EXTENDIDAS (11-25)]")
        for i, (desc, _) in enumerate(QUERIES_EXTENDIDAS, 11):
            print(f"  {i:2d}. {desc}")
        print()
        print("  A. Ejecutar TODAS (1-25)")
        print("  B. Solo básicas (1-10)")
        print("  C. Solo extendidas (11-25)")
        print("  0. Volver al menú principal")
        print()

        opcion = input("Seleccione opción: ").strip()

        if opcion == "0":
            break
        elif opcion.upper() == "A":
            print_header("EJECUTANDO TODAS LAS CONSULTAS")
            for i, (desc, query) in enumerate(QUERIES_ORIGINALES + QUERIES_EXTENDIDAS, 1):
                print(f"[{i:2d}]", end=" ")
                ejecutar_consulta(desc, query)
            pausa()
        elif opcion.upper() == "B":
            print_header("CONSULTAS BÁSICAS (1-10)")
            for i, (desc, query) in enumerate(QUERIES_ORIGINALES, 1):
                print(f"[{i:2d}]", end=" ")
                ejecutar_consulta(desc, query)
            pausa()
        elif opcion.upper() == "C":
            print_header("CONSULTAS EXTENDIDAS (11-25)")
            for i, (desc, query) in enumerate(QUERIES_EXTENDIDAS, 11):
                print(f"[{i:2d}]", end=" ")
                ejecutar_consulta(desc, query)
            pausa()
        else:
            try:
                num = int(opcion)
                todas = QUERIES_ORIGINALES + QUERIES_EXTENDIDAS
                if 1 <= num <= len(todas):
                    desc, query = todas[num - 1]
                    ejecutar_consulta(desc, query)
                    pausa()
                else:
                    print("Número fuera de rango.")
            except ValueError:
                print("Opción no válida.")


def submenu_fase1():
    """Submenú interactivo para operaciones de Fase I."""
    clear_screen()
    crud = CrudService()
    export = ExportService()
    metrics = MetricsService()

    while True:
        print_header("FASE I - CRUD + IMPORT/EXPORT + MÉTRICAS")
        print()
        print(" [PAÍS]")
        print("  1. Crear País")
        print("  2. Leer Países")
        print()
        print(" [CIUDAD]")
        print("  3. Crear Ciudad")
        print("  4. Leer Ciudades (con país)")
        print("  5. Eliminar Ciudad")
        print()
        print(" [PELÍCULA]")
        print("  6. Actualizar Tarifa")
        print("  7. Buscar por ID")
        print()
        print(" [EXPORT/IMPORT]")
        print("  8. Exportar a CSV")
        print("  9. Exportar a JSON")
        print(" 10. Importar de CSV")
        print(" 11. Importar de JSON")
        print()
        print(" [MÉTRICAS]")
        print(" 12. Métricas Descriptivas (Film)")
        print()
        print("  0. Volver al menú principal")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            print_subheader("Crear País")
            nombre = input("  Nombre del país: ").strip()
            if nombre:
                crud.crear_pais(nombre)
            else:
                print("  Nombre no puede estar vacío.")
            pausa()
        elif opcion == "2":
            print_subheader("Leer Países")
            limite = input("  Cantidad (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            paises = crud.leer_paises(limite)
            print(f"  Recuperados: {len(paises)}")
            for p in paises:
                print(f"    {p.country_id}: {p.country}")
            pausa()
        elif opcion == "3":
            print_subheader("Crear Ciudad")
            nombre = input("  Nombre de la ciudad: ").strip()
            country_id = input("  ID del país: ").strip()
            if nombre and country_id.isdigit():
                crud.crear_ciudad(nombre, int(country_id))
            else:
                print("  Datos inválidos.")
            pausa()
        elif opcion == "4":
            print_subheader("Leer Ciudades")
            limite = input("  Cantidad (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            ciudades = crud.leer_ciudades(limite)
            print(f"  Recuperadas: {len(ciudades)}")
            for c in ciudades:
                print(f"    {c[0]}: {c[1]} (País: {c[3]})")
            pausa()
        elif opcion == "5":
            print_subheader("Eliminar Ciudad")
            city_id = input("  ID de la ciudad: ").strip()
            if city_id.isdigit():
                crud.eliminar_ciudad(int(city_id))
            else:
                print("  ID inválido.")
            pausa()
        elif opcion == "6":
            print_subheader("Actualizar Tarifa Película")
            film_id = input("  ID de la película: ").strip()
            nueva_tarifa = input("  Nueva tarifa: ").strip()
            if film_id.isdigit() and nueva_tarifa.replace('.', '').isdigit():
                crud.actualizar_tarifa_pelicula(int(film_id), float(nueva_tarifa))
            else:
                print("  Datos inválidos.")
            pausa()
        elif opcion == "7":
            print_subheader("Buscar Película por ID")
            film_id = input("  ID de la película: ").strip()
            if film_id.isdigit():
                pelicula = crud.buscar_pelicula_por_id(int(film_id))
                if pelicula:
                    print(f"  {pelicula}")
                else:
                    print("  No encontrada.")
            else:
                print("  ID inválido.")
            pausa()
        elif opcion == "8":
            print_subheader("Exportar a CSV")
            tabla = input("  Tabla (film/city/country/inventory): ").strip()
            if tabla:
                export.exportar_a_csv(tabla, f"data/{tabla}.csv")
            pausa()
        elif opcion == "9":
            print_subheader("Exportar a JSON")
            tabla = input("  Tabla (film/city/country/inventory): ").strip()
            if tabla:
                export.exportar_a_json(tabla, f"data/{tabla}.json")
            pausa()
        elif opcion == "10":
            print_subheader("Importar de CSV")
            ruta = input("  Ruta del archivo CSV: ").strip()
            tabla = input("  Nombre de la tabla destino: ").strip()
            if ruta and tabla:
                export.importar_des_csv(ruta, tabla)
            pausa()
        elif opcion == "11":
            print_subheader("Importar de JSON")
            ruta = input("  Ruta del archivo JSON: ").strip()
            tabla = input("  Nombre de la tabla destino: ").strip()
            if ruta and tabla:
                export.importar_des_json(ruta, tabla)
            pausa()
        elif opcion == "12":
            print_subheader("Métricas Descriptivas")
            metrics.calcular_metricas_descriptivas()
            pausa()
        else:
            print("Opción no válida.")


def submenu_fase2():
    """Submenú interactivo para operaciones de Fase II ORM."""
    clear_screen()
    controlador = SakilaWorkflowController()
    repo = DataRepository(DbContext())

    while True:
        print_header("FASE II - ORM NATIVO (POO)")
        print()
        print(" [COUNTRY / CITY]")
        print("  1. Crear País")
        print("  2. Leer Países (List<Entity>)")
        print("  3. Crear Ciudad")
        print("  4. Leer Ciudades con país")
        print()
        print(" [FILM / INVENTORY]")
        print("  5. Buscar Película")
        print("  6. Leer Películas")
        print("  7. Actualizar Tarifa")
        print("  8. Leer Inventario por Tienda")
        print()
        print(" [NUEVAS ENTIDADES]")
        print("  9.  Menú Actor")
        print(" 10.  Menú Category")
        print(" 11.  Menú Staff")
        print(" 12.  Menú Customer")
        print(" 13.  Menú Rental")
        print(" 14.  Menú Payment")
        print()
        print(" 15. Ejecutar Flujo Completo ORM")
        print("  0. Volver al menú principal")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            break
        elif opcion == "1":
            print_subheader("Crear País (Entity)")
            nombre = input("  Nombre del país: ").strip()
            if nombre:
                pais = controlador.crear_pais(nombre)
                print(f"  Creado: {pais}")
            pausa()
        elif opcion == "2":
            print_subheader("Leer Países")
            limite = input("  Cantidad (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            paises = controlador.obtener_paises(limite)
            print(f"  List<CountryEntity>: {len(paises)} elementos")
            for p in paises:
                print(f"    {p}")
            pausa()
        elif opcion == "3":
            print_subheader("Crear Ciudad")
            nombre = input("  Nombre de la ciudad: ").strip()
            country_id = input("  ID del país: ").strip()
            if nombre and country_id.isdigit():
                ciudad = controlador.crear_ciudad(nombre, int(country_id))
                print(f"  Creada: {ciudad}")
            pausa()
        elif opcion == "4":
            print_subheader("Leer Ciudades con país")
            limite = input("  Cantidad (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            ciudades = controlador.obtener_ciudades(limite)
            print(f"  Recuperadas: {len(ciudades)}")
            for c in ciudades:
                print(f"    {c[0]}: {c[1]} (País: {c[3]})")
            pausa()
        elif opcion == "5":
            print_subheader("Buscar Película")
            film_id = input("  ID de la película: ").strip()
            if film_id.isdigit():
                pelicula = controlador.obtener_pelicula(int(film_id))
                if pelicula:
                    print(f"  {pelicula}")
                else:
                    print("  No encontrada.")
            pausa()
        elif opcion == "6":
            print_subheader("Leer Películas")
            limite = input("  Cantidad (default 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            peliculas = controlador.obtener_peliculas(limite)
            print(f"  List<FilmEntity>: {len(peliculas)} elementos")
            for p in peliculas:
                print(f"    {p}")
            pausa()
        elif opcion == "7":
            print_subheader("Actualizar Tarifa")
            film_id = input("  ID: ").strip()
            nueva_tarifa = input("  Nueva tarifa: ").strip()
            if film_id.isdigit() and nueva_tarifa.replace('.', '').isdigit():
                if controlador.actualizar_tarifa(int(film_id), float(nueva_tarifa)):
                    print("  Tarifa actualizada.")
                else:
                    print("  No se pudo actualizar.")
            pausa()
        elif opcion == "8":
            print_subheader("Inventario por Tienda")
            store_id = input("  ID de tienda (1/2): ").strip()
            if store_id.isdigit():
                inventarios = repo.listar_inventario_por_tienda(int(store_id))
                print(f"  Elementos: {len(inventarios)}")
                for i in inventarios:
                    print(f"    {i}")
            pausa()
        elif opcion == "9":
            submenu_actor(repo)
        elif opcion == "10":
            submenu_category(repo)
        elif opcion == "11":
            submenu_staff(repo)
        elif opcion == "12":
            submenu_customer(repo)
        elif opcion == "13":
            submenu_rental(repo)
        elif opcion == "14":
            submenu_payment(repo)
        elif opcion == "15":
            print_subheader("Flujo Completo ORM")
            controlador.procesar_flujo_completo()
            pausa()
        else:
            print("Opción no válida.")


def submenu_actor(repo):
    """Submenú para Actor."""
    clear_screen()
    while True:
        print_header("ACTOR - CRUD")
        print("1. Crear Actor")
        print("  2. Leer Actores")
        print("  3. Buscar por nombre")
        print("  0. Volver")
        print()
        opcion = input("Seleccione: ").strip()
        if opcion == "0":
            break
        elif opcion == "1":
            fname = input("  Primer nombre: ").strip()
            lname = input("  Apellido: ").strip()
            if fname and lname:
                from src.entities import ActorEntity
                actor = ActorEntity(None, fname, lname)
                if repo.guardar_actor(actor):
                    print(f"  Creado: {actor}")
            pausa()
        elif opcion == "2":
            actores = repo.listar_actores(10)
            for a in actores:
                print(f"    {a}")
            pausa()
        elif opcion == "3":
            nombre = input("  Nombre a buscar: ").strip()
            if nombre:
                actores = repo.buscar_actor_por_nombre(nombre)
                for a in actores:
                    print(f"    {a}")
            pausa()


def submenu_category(repo):
    """Submenú para Category."""
    clear_screen()
    while True:
        print_header("CATEGORY - CRUD")
        print("  1. Crear Categoría")
        print("  2. Leer Categorías")
        print("  0. Volver")
        print()
        opcion = input("Seleccione: ").strip()
        if opcion == "0":
            break
        elif opcion == "1":
            nombre = input("  Nombre: ").strip()
            if nombre:
                from src.entities import CategoryEntity
                cat = CategoryEntity(None, nombre)
                if repo.guardar_categoria(cat):
                    print(f"  Creada: {cat}")
            pausa()
        elif opcion == "2":
            cats = repo.listar_categorias(20)
            for c in cats:
                print(f"    {c}")
            pausa()


def submenu_staff(repo):
    """Submenú para Staff."""
    clear_screen()
    while True:
        print_header("STAFF - CRUD")
        print("  1. Crear Staff")
        print("  2. Leer Staff")
        print("  0. Volver")
        print()
        opcion = input("Seleccione: ").strip()
        if opcion == "0":
            break
        elif opcion == "1":
            fname = input("  Primer nombre: ").strip()
            lname = input("  Apellido: ").strip()
            address_id = input("  Address ID: ").strip()
            store_id = input("  Store ID: ").strip()
            username = input("  Username: ").strip()
            if fname and lname and address_id.isdigit() and store_id.isdigit() and username:
                from src.entities import StaffEntity
                staff = StaffEntity(None, fname, lname, int(address_id), None,
                                   int(store_id), 1, username, None)
                if repo.guardar_staff(staff):
                    print(f"  Creado: {staff}")
            pausa()
        elif opcion == "2":
            staff_list = repo.listar_staff(10)
            for s in staff_list:
                print(f"    {s}")
            pausa()


def submenu_customer(repo):
    """Submenú para Customer."""
    clear_screen()
    while True:
        print_header("CUSTOMER - CRUD")
        print("  1. Crear Customer")
        print("  2. Leer Customers")
        print("  0. Volver")
        print()
        opcion = input("Seleccione: ").strip()
        if opcion == "0":
            break
        elif opcion == "1":
            fname = input("  Primer nombre: ").strip()
            lname = input("  Apellido: ").strip()
            store_id = input("  Store ID: ").strip()
            address_id = input("  Address ID: ").strip()
            if fname and lname and store_id.isdigit() and address_id.isdigit():
                from src.entities import CustomerEntity
                cust = CustomerEntity(None, int(store_id), fname, lname,
                                      None, int(address_id), None)
                if repo.guardar_cliente(cust):
                    print(f"  Creado: {cust}")
            pausa()
        elif opcion == "2":
            customers = repo.listar_clientes(10)
            for c in customers:
                print(f"    {c}")
            pausa()


def submenu_rental(repo):
    """Submenú para Rental."""
    clear_screen()
    while True:
        print_header("RENTAL - CRUD")
        print("  1. Crear Rental")
        print("  2. Leer Rentals")
        print("  3. Ver alquileres activos")
        print("  0. Volver")
        print()
        opcion = input("Seleccione: ").strip()
        if opcion == "0":
            break
        elif opcion == "1":
            inventory_id = input("  Inventory ID: ").strip()
            customer_id = input("  Customer ID: ").strip()
            staff_id = input("  Staff ID: ").strip()
            if inventory_id.isdigit() and customer_id.isdigit() and staff_id.isdigit():
                from src.entities import RentalEntity
                rental = RentalEntity(None, "2026-06-06 10:00:00", int(inventory_id),
                                    int(customer_id), None, int(staff_id))
                if repo.guardar_alquiler(rental):
                    print(f"  Creado: {rental}")
            pausa()
        elif opcion == "2":
            rentals = repo.listar_alquileres(10)
            for r in rentals:
                print(f"    {r}")
            pausa()
        elif opcion == "3":
            rentals = repo.listar_alquileres_activos()
            print(f"  Activos: {len(rentals)}")
            for r in rentals:
                print(f"    {r}")
            pausa()


def submenu_payment(repo):
    """Submenú para Payment."""
    clear_screen()
    while True:
        print_header("PAYMENT - CRUD")
        print("  1. Crear Payment")
        print("  2. Leer Payments")
        print("  3. Total por cliente")
        print("  0. Volver")
        print()
        opcion = input("Seleccione: ").strip()
        if opcion == "0":
            break
        elif opcion == "1":
            customer_id = input("  Customer ID: ").strip()
            staff_id = input("  Staff ID: ").strip()
            amount = input("  Amount: ").strip()
            if customer_id.isdigit() and staff_id.isdigit() and amount.replace('.', '').isdigit():
                from src.entities import PaymentEntity
                payment = PaymentEntity(None, int(customer_id), int(staff_id),
                                      None, float(amount), "2026-06-06 10:00:00")
                if repo.guardar_pago(payment):
                    print(f"  Creado: {payment}")
            pausa()
        elif opcion == "2":
            payments = repo.listar_pagos(10)
            for p in payments:
                print(f"    {p}")
            pausa()
        elif opcion == "3":
            customer_id = input("  Customer ID: ").strip()
            if customer_id.isdigit():
                total = repo.calcular_total_pagos_por_cliente(int(customer_id))
                print(f"  Total gastado: ${total:.2f}")
            pausa()


def mostrar_menu_interactivo():
    """Muestra el menú principal interactivo."""
    clear_screen()
    while True:
        print_header("MENÚ PRINCIPAL - uasdCrudPython")
        print("  Maestría en Ciencia de Datos e Inteligencia Artificial")
        print()
        print(" 1. FASE I: CRUD + Import/Export + Métricas")
        print(" 2. FASE II: Arquitectura ORM (con submenús)")
        print(" 3. CONSULTAS SQL (25 queries)")
        print(" 4. DOCUMENTACIÓN")
        print(" 0. Salir")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            submenu_fase1()
        elif opcion == "2":
            submenu_fase2()
        elif opcion == "3":
            ejecutar_queries()
        elif opcion == "4":
            print("\nDocumentación en docs/:")
            print("  - README.md, DESIGN.md, criterios.md")
            print("  - ensayo/ensayo.md")
            print("  - evidencias/logs.md")
            pausa()
        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción no válida.")


def main():
    """Entry point con soporte CLI flags."""
    parser = argparse.ArgumentParser(
        description="uasdCrudPython - CRUD/ORM nativo en Python con MariaDB"
    )
    parser.add_argument("--fase1", action="store_true", help="Ejecutar Fase I")
    parser.add_argument("--fase2", action="store_true", help="Ejecutar Fase II")
    parser.add_argument("--queries", action="store_true", help="Ejecutar consultas")
    parser.add_argument("--all", action="store_true", help="Ejecutar todo")
    parser.add_argument("--menu", action="store_true", help="Forzar menú interactivo")

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
