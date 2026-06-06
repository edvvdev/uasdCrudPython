# =====================================================================
# CRUD SERVICE - Operaciones de Creación, Lectura, Actualización, Eliminación
# =====================================================================

from typing import List, Optional
from src.dbcontext import DbContext
from src.entities import (
    CountryEntity, CityEntity, FilmEntity, InventoryEntity,
    LanguageEntity, AddressEntity, StoreEntity, ActorEntity,
    CategoryEntity, StaffEntity, CustomerEntity, RentalEntity, PaymentEntity,
    FilmTextEntity
)


class CrudService:
    """Servicio para operaciones CRUD sobre todas las tablas Sakila."""

    def __init__(self):
        self.context = DbContext()

    # --- Country ---

    def crear_pais(self, nombre: str) -> Optional[CountryEntity]:
        entity = CountryEntity(country_id=None, country=nombre)
        query = "INSERT INTO country (country) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.country,))
        if last_id is not None:
            entity.country_id = last_id
            print(f"[CREATE] País '{nombre}' insertado (ID: {last_id})")
            return entity
        return None

    def leer_paises(self, limite: int = 10) -> List[CountryEntity]:
        query = "SELECT country_id, country, last_update FROM country ORDER BY country_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [CountryEntity(country_id=f[0], country=f[1], last_update=str(f[2])) for f in filas]

    # --- City ---

    def crear_ciudad(self, nombre: str, country_id: int) -> Optional[CityEntity]:
        entity = CityEntity(city_id=None, city=nombre, country_id=country_id)
        query = "INSERT INTO city (city, country_id) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.city, entity.country_id))
        if last_id is not None:
            entity.city_id = last_id
            print(f"[CREATE] Ciudad '{nombre}' vinculada al país ID {country_id} (ID: {last_id})")
            return entity
        return None

    def leer_ciudades(self, limite: int = 10) -> List[tuple]:
        query = """SELECT c.city_id, c.city, c.country_id, co.country, c.last_update
                   FROM city c INNER JOIN country co ON c.country_id = co.country_id
                   ORDER BY c.city_id DESC LIMIT %s"""
        return self.context.ejecutar_consulta(query, (limite,))

    def eliminar_ciudad(self, city_id: int) -> bool:
        query = "DELETE FROM city WHERE city_id = %s"
        result = self.context.ejecutar_comando(query, (city_id,))
        if result:
            print(f"[DELETE] Ciudad ID {city_id} eliminada")
        return result is not None

    # --- Film ---

    def leer_peliculas(self, limite: int = 10) -> List[FilmEntity]:
        query = """SELECT film_id, title, rental_rate, length, replacement_cost,
                   release_year, description, rating FROM film ORDER BY film_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [FilmEntity(
            film_id=f[0], title=f[1], rental_rate=f[2], length=f[3],
            replacement_cost=f[4], release_year=f[5], description=f[6], rating=f[7]
        ) for f in filas]

    def buscar_pelicula_por_id(self, film_id: int) -> Optional[FilmEntity]:
        query = """SELECT film_id, title, rental_rate, length, replacement_cost,
                   release_year, description, rating FROM film WHERE film_id = %s"""
        filas = self.context.ejecutar_consulta(query, (film_id,))
        if filas:
            f = filas[0]
            return FilmEntity(
                film_id=f[0], title=f[1], rental_rate=f[2], length=f[3],
                replacement_cost=f[4], release_year=f[5], description=f[6], rating=f[7]
            )
        return None

    def actualizar_tarifa_pelicula(self, film_id: int, nueva_tarifa: float) -> bool:
        query = "UPDATE film SET rental_rate = %s WHERE film_id = %s"
        result = self.context.ejecutar_comando(query, (nueva_tarifa, film_id))
        if result:
            print(f"[UPDATE] Película ID {film_id} actualizada con tarifa ${nueva_tarifa}")
        return result is not None

    # --- Language ---

    def crear_idioma(self, nombre: str) -> Optional[LanguageEntity]:
        entity = LanguageEntity(language_id=None, name=nombre)
        query = "INSERT INTO language (name) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.name,))
        if last_id is not None:
            entity.language_id = last_id
            print(f"[CREATE] Idioma '{nombre}' insertado (ID: {last_id})")
            return entity
        return None

    def leer_idiomas(self, limite: int = 10) -> List[LanguageEntity]:
        query = "SELECT language_id, name, last_update FROM language ORDER BY language_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [LanguageEntity(language_id=f[0], name=f[1], last_update=str(f[2])) for f in filas]

    # --- Address ---

    def crear_direccion(self, address: str, district: str, city_id: int,
 phone: str, address2: str = None, postal_code: str = None) -> Optional[AddressEntity]:
        entity = AddressEntity(address_id=None, address=address, address2=address2,
                               district=district, city_id=city_id,
                               postal_code=postal_code, phone=phone)
        query = """INSERT INTO address (address, address2, district, city_id, postal_code, phone)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (entity.address, entity.address2, entity.district,
                  entity.city_id, entity.postal_code, entity.phone)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.address_id = last_id
            print(f"[CREATE] Dirección '{address}' insertada (ID: {last_id})")
            return entity
        return None

    def leer_direcciones(self, limite: int = 10) -> List[AddressEntity]:
        query = """SELECT address_id, address, address2, district, city_id, postal_code, phone, last_update
                   FROM address ORDER BY address_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [AddressEntity(
            address_id=f[0], address=f[1], address2=f[2], district=f[3],
            city_id=f[4], postal_code=f[5], phone=f[6], last_update=str(f[7])
        ) for f in filas]

    # --- Store ---

    def crear_tienda(self, manager_staff_id: int, address_id: int) -> Optional[StoreEntity]:
        entity = StoreEntity(store_id=None, manager_staff_id=manager_staff_id,
                             address_id=address_id)
        query = "INSERT INTO store (manager_staff_id, address_id) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.manager_staff_id, entity.address_id))
        if last_id is not None:
            entity.store_id = last_id
            print(f"[CREATE] Tienda insertada (ID: {last_id})")
            return entity
        return None

    def leer_tiendas(self, limite: int = 10) -> List[StoreEntity]:
        query = "SELECT store_id, manager_staff_id, address_id, last_update FROM store ORDER BY store_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [StoreEntity(
            store_id=f[0], manager_staff_id=f[1], address_id=f[2], last_update=str(f[3])
        ) for f in filas]

    # --- Actor ---

    def crear_actor(self, first_name: str, last_name: str) -> Optional[ActorEntity]:
        entity = ActorEntity(actor_id=None, first_name=first_name, last_name=last_name)
        query = "INSERT INTO actor (first_name, last_name) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.first_name, entity.last_name))
        if last_id is not None:
            entity.actor_id = last_id
            print(f"[CREATE] Actor '{first_name} {last_name}' insertado (ID: {last_id})")
            return entity
        return None

    def leer_actores(self, limite: int = 10) -> List[ActorEntity]:
        query = "SELECT actor_id, first_name, last_name, last_update FROM actor ORDER BY actor_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [ActorEntity(
            actor_id=f[0], first_name=f[1], last_name=f[2], last_update=str(f[3])
        ) for f in filas]

    def buscar_actor_por_nombre(self, nombre: str) -> List[ActorEntity]:
        query = "SELECT actor_id, first_name, last_name, last_update FROM actor WHERE first_name LIKE %s OR last_name LIKE %s"
        pattern = f"%{nombre}%"
        filas = self.context.ejecutar_consulta(query, (pattern, pattern))
        return [ActorEntity(
            actor_id=f[0], first_name=f[1], last_name=f[2], last_update=str(f[3])
        ) for f in filas]

    # --- Category ---

    def crear_categoria(self, nombre: str) -> Optional[CategoryEntity]:
        entity = CategoryEntity(category_id=None, name=nombre)
        query = "INSERT INTO category (name) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.name,))
        if last_id is not None:
            entity.category_id = last_id
            print(f"[CREATE] Categoría '{nombre}' insertada (ID: {last_id})")
            return entity
        return None

    def leer_categorias(self, limite: int = 20) -> List[CategoryEntity]:
        query = "SELECT category_id, name, last_update FROM category ORDER BY category_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [CategoryEntity(category_id=f[0], name=f[1], last_update=str(f[2])) for f in filas]

    # --- Staff ---

    def crear_staff(self, first_name: str, last_name: str, address_id: int,
                    store_id: int, username: str, email: str = None) -> Optional[StaffEntity]:
        entity = StaffEntity(staff_id=None, first_name=first_name, last_name=last_name,
                             address_id=address_id, email=email, store_id=store_id,
                             active=1, username=username, password=None)
        query = """INSERT INTO staff (first_name, last_name, address_id, email, store_id, active, username, password)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (entity.first_name, entity.last_name, entity.address_id,
                  entity.email, entity.store_id, entity.active, entity.username, entity.password)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.staff_id = last_id
            print(f"[CREATE] Staff '{username}' insertado (ID: {last_id})")
            return entity
        return None

    def leer_staff(self, limite: int = 10) -> List[StaffEntity]:
        query = """SELECT staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update
                   FROM staff ORDER BY staff_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [StaffEntity(
            staff_id=f[0], first_name=f[1], last_name=f[2], address_id=f[3],
            email=f[4], store_id=f[5], active=f[6], username=f[7], password=f[8], last_update=str(f[9])
        ) for f in filas]

    # --- Customer ---

    def crear_cliente(self, store_id: int, first_name: str, last_name: str,
                      address_id: int, email: str = None) -> Optional[CustomerEntity]:
        entity = CustomerEntity(customer_id=None, store_id=store_id, first_name=first_name,
                                last_name=last_name, email=email, address_id=address_id)
        query = """INSERT INTO customer (store_id, first_name, last_name, email, address_id, create_date)
                   VALUES (%s, %s, %s, %s, %s, NOW())"""
        params = (entity.store_id, entity.first_name, entity.last_name, entity.email, entity.address_id)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.customer_id = last_id
            print(f"[CREATE] Cliente '{first_name} {last_name}' insertado (ID: {last_id})")
            return entity
        return None

    def leer_clientes(self, limite: int = 10) -> List[CustomerEntity]:
        query = """SELECT customer_id, store_id, first_name, last_name, email, address_id, create_date, last_update
                   FROM customer ORDER BY customer_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [CustomerEntity(
            customer_id=f[0], store_id=f[1], first_name=f[2], last_name=f[3],
            email=f[4], address_id=f[5], create_date=str(f[6]), last_update=str(f[7])
        ) for f in filas]

    # --- Rental ---

    def crear_alquiler(self, inventory_id: int, customer_id: int, staff_id: int) -> Optional[RentalEntity]:
        entity = RentalEntity(rental_id=None, rental_date="NOW()", inventory_id=inventory_id,
                              customer_id=customer_id, return_date=None, staff_id=staff_id)
        query = """INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id)
                   VALUES (NOW(), %s, %s, NULL, %s)"""
        last_id = self.context.ejecutar_comando(query, (entity.inventory_id, entity.customer_id, entity.staff_id))
        if last_id is not None:
            entity.rental_id = last_id
            print(f"[CREATE] Rental insertado (ID: {last_id})")
            return entity
        return None

    def leer_alquileres(self, limite: int = 10) -> List[RentalEntity]:
        query = """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
                   FROM rental ORDER BY rental_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [RentalEntity(
            rental_id=f[0], rental_date=str(f[1]), inventory_id=f[2], customer_id=f[3],
            return_date=str(f[4]) if f[4] else None, staff_id=f[5], last_update=str(f[6])
        ) for f in filas]

    def leer_alquileres_activos(self) -> List[RentalEntity]:
        query = """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
                   FROM rental WHERE return_date IS NULL ORDER BY rental_id DESC"""
        filas = self.context.ejecutar_consulta(query)
        return [RentalEntity(
            rental_id=f[0], rental_date=str(f[1]), inventory_id=f[2], customer_id=f[3],
            return_date=str(f[4]) if f[4] else None, staff_id=f[5], last_update=str(f[6])
        ) for f in filas]

    # --- Payment ---

    def crear_pago(self, customer_id: int, staff_id: int, amount: float,
                   rental_id: int = None) -> Optional[PaymentEntity]:
        entity = PaymentEntity(payment_id=None, customer_id=customer_id, staff_id=staff_id,
                                rental_id=rental_id, amount=amount, payment_date="NOW()")
        query = """INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date)
                   VALUES (%s, %s, %s, %s, NOW())"""
        params = (entity.customer_id, entity.staff_id, entity.rental_id, entity.amount)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.payment_id = last_id
            print(f"[CREATE] Pago insertado (ID: {last_id}, Amount: ${amount})")
            return entity
        return None

    def leer_pagos(self, limite: int = 10) -> List[PaymentEntity]:
        query = """SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date, last_update
                   FROM payment ORDER BY payment_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [PaymentEntity(
            payment_id=f[0], customer_id=f[1], staff_id=f[2], rental_id=f[3],
            amount=f[4], payment_date=str(f[5]), last_update=str(f[6])
        ) for f in filas]

    def total_pagos_cliente(self, customer_id: int) -> float:
        query = "SELECT COALESCE(SUM(amount), 0) FROM payment WHERE customer_id = %s"
        filas = self.context.ejecutar_consulta(query, (customer_id,))
        return float(filas[0][0]) if filas else 0.0

    # --- Inventory ---

    def crear_inventario(self, film_id: int, store_id: int) -> Optional[InventoryEntity]:
        entity = InventoryEntity(inventory_id=None, film_id=film_id, store_id=store_id)
        query = "INSERT INTO inventory (film_id, store_id) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.film_id, entity.store_id))
        if last_id is not None:
            entity.inventory_id = last_id
            print(f"[CREATE] Inventario insertado (ID: {last_id})")
            return entity
        return None

    def leer_inventario_por_tienda(self, store_id: int) -> List[InventoryEntity]:
        query = "SELECT inventory_id, film_id, store_id, last_update FROM inventory WHERE store_id = %s"
        filas = self.context.ejecutar_consulta(query, (store_id,))
        return [InventoryEntity(
            inventory_id=f[0], film_id=f[1], store_id=f[2], last_update=str(f[3])
        ) for f in filas]

    # --- Film Text ---

    def crear_film_text(self, film_id: int, title: str, description: str = None) -> Optional[FilmTextEntity]:
        """Inserta un registro film_text."""
        entity = FilmTextEntity(film_id=film_id, title=title, description=description)
        query = "INSERT INTO film_text (film_id, title, description) VALUES (%s, %s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.film_id, entity.title, entity.description))
        if last_id is not None:
            print(f"[CREATE] FilmText insertado (film_id: {film_id})")
            return entity
        return None

    def leer_film_text(self, limite: int = 10) -> List[FilmTextEntity]:
        """Lista registros film_text."""
        query = "SELECT film_id, title, description FROM film_text ORDER BY film_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [FilmTextEntity(film_id=f[0], title=f[1], description=f[2]) for f in filas]

    def buscar_film_text_por_titulo(self, titulo: str) -> List[FilmTextEntity]:
        """Busca film_text por patrón en título."""
        query = "SELECT film_id, title, description FROM film_text WHERE title LIKE %s"
        pattern = f"%{titulo}%"
        filas = self.context.ejecutar_consulta(query, (pattern,))
        return [FilmTextEntity(film_id=f[0], title=f[1], description=f[2]) for f in filas]
