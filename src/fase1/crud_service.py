# =====================================================================
# CRUD SERVICE - Operaciones CRUD con Manejo de Errores
# =====================================================================

import sys
from typing import List, Optional
from src.dbcontext import DbContext
from src.entities import (
    CountryEntity, CityEntity, FilmEntity, InventoryEntity,
    LanguageEntity, AddressEntity, StoreEntity, ActorEntity,
    CategoryEntity, StaffEntity, CustomerEntity, RentalEntity, PaymentEntity,
    FilmTextEntity
)


class CrudService:
    """Servicio CRUD con manejo completo de errores."""

    def __init__(self):
        try:
            self.context = DbContext()
        except Exception as e:
            print(f"[CRITICAL] No se pudo conectar a la base de datos: {e}")
            sys.exit(1)

    # --- Country ---

    def crear_pais(self, nombre: str) -> Optional[CountryEntity]:
        if not nombre or not nombre.strip():
            print("[ERROR] Nombre de país no puede estar vacío")
            return None
        try:
            entity = CountryEntity(country_id=None, country=nombre.strip())
            query = "INSERT INTO country (country) VALUES (%s)"
            last_id = self.context.ejecutar_comando(query, (entity.country,))
            if last_id is not None:
                entity.country_id = last_id
                print(f"[CREATE] País '{nombre}' insertado (ID: {last_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear país: {e}")
            return None

    def leer_paises(self, limite: int = 10) -> List[CountryEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = "SELECT country_id, country, last_update FROM country ORDER BY country_id DESC LIMIT %s"
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [CountryEntity(country_id=f[0], country=f[1], last_update=str(f[2])) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer países: {e}")
            return []

    # --- City ---

    def crear_ciudad(self, nombre: str, country_id: int) -> Optional[CityEntity]:
        if not nombre or not nombre.strip():
            print("[ERROR] Nombre de ciudad no puede estar vacío")
            return None
        if not isinstance(country_id, int) or country_id <= 0:
            print("[ERROR] country_id debe ser un entero positivo")
            return None
        try:
            entity = CityEntity(city_id=None, city=nombre.strip(), country_id=country_id)
            query = "INSERT INTO city (city, country_id) VALUES (%s, %s)"
            last_id = self.context.ejecutar_comando(query, (entity.city, entity.country_id))
            if last_id is not None:
                entity.city_id = last_id
                print(f"[CREATE] Ciudad '{nombre}' vinculada al país ID {country_id} (ID: {last_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear ciudad: {e}")
            return None

    def leer_ciudades(self, limite: int = 10) -> List[tuple]:
        if limite <= 0:
            limite = 10
        try:
            query = """SELECT c.city_id, c.city, c.country_id, co.country, c.last_update
                       FROM city c INNER JOIN country co ON c.country_id = co.country_id
                       ORDER BY c.city_id DESC LIMIT %s"""
            return self.context.ejecutar_consulta(query, (limite,))
        except Exception as e:
            print(f"[ERROR] No se pudieron leer ciudades: {e}")
            return []

    def eliminar_ciudad(self, city_id: int) -> bool:
        if not isinstance(city_id, int) or city_id <= 0:
            print("[ERROR] city_id debe ser un entero positivo")
            return False
        try:
            query = "DELETE FROM city WHERE city_id = %s"
            result = self.context.ejecutar_comando(query, (city_id,))
            if result:
                print(f"[DELETE] Ciudad ID {city_id} eliminada")
            return result is not None
        except Exception as e:
            print(f"[ERROR] No se pudo eliminar ciudad: {e}")
            return False

    # --- Film ---

    def leer_peliculas(self, limite: int = 10) -> List[FilmEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = """SELECT film_id, title, rental_rate, length, replacement_cost,
                       release_year, description, rating FROM film ORDER BY film_id DESC LIMIT %s"""
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [FilmEntity(
                film_id=f[0], title=f[1], rental_rate=f[2], length=f[3],
                replacement_cost=f[4], release_year=f[5], description=f[6], rating=f[7]
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer películas: {e}")
            return []

    def buscar_pelicula_por_id(self, film_id: int) -> Optional[FilmEntity]:
        if not isinstance(film_id, int) or film_id <= 0:
            print("[ERROR] film_id debe ser un entero positivo")
            return None
        try:
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
        except Exception as e:
            print(f"[ERROR] No se pudo buscar película: {e}")
            return None

    def actualizar_tarifa_pelicula(self, film_id: int, nueva_tarifa: float) -> bool:
        if not isinstance(film_id, int) or film_id <= 0:
            print("[ERROR] film_id debe ser un entero positivo")
            return False
        if not isinstance(nueva_tarifa, (int, float)) or nueva_tarifa < 0:
            print("[ERROR] nueva_tarifa debe ser un número no negativo")
            return False
        try:
            query = "UPDATE film SET rental_rate = %s WHERE film_id = %s"
            result = self.context.ejecutar_comando(query, (nueva_tarifa, film_id))
            if result:
                print(f"[UPDATE] Película ID {film_id} actualizada con tarifa ${nueva_tarifa}")
            return result is not None
        except Exception as e:
            print(f"[ERROR] No se pudo actualizar tarifa: {e}")
            return False

    # --- Language ---

    def crear_idioma(self, nombre: str) -> Optional[LanguageEntity]:
        if not nombre or not nombre.strip():
            print("[ERROR] Nombre de idioma no puede estar vacío")
            return None
        try:
            entity = LanguageEntity(language_id=None, name=nombre.strip())
            query = "INSERT INTO language (name) VALUES (%s)"
            last_id = self.context.ejecutar_comando(query, (entity.name,))
            if last_id is not None:
                entity.language_id = last_id
                print(f"[CREATE] Idioma '{nombre}' insertado (ID: {last_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear idioma: {e}")
            return None

    def leer_idiomas(self, limite: int = 10) -> List[LanguageEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = "SELECT language_id, name, last_update FROM language ORDER BY language_id DESC LIMIT %s"
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [LanguageEntity(language_id=f[0], name=f[1], last_update=str(f[2])) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer idiomas: {e}")
            return []

    # --- Address ---

    def crear_direccion(self, address: str, district: str, city_id: int,
                        phone: str, address2: str = None, postal_code: str = None) -> Optional[AddressEntity]:
        if not address or not address.strip():
            print("[ERROR] Dirección no puede estar vacía")
            return None
        if not isinstance(city_id, int) or city_id <= 0:
            print("[ERROR] city_id debe ser un entero positivo")
            return None
        try:
            entity = AddressEntity(address_id=None, address=address.strip(), address2=address2,
 district=district.strip() if district else None, city_id=city_id,
                                   postal_code=postal_code, phone=phone.strip())
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
        except Exception as e:
            print(f"[ERROR] No se pudo crear dirección: {e}")
            return None

    def leer_direcciones(self, limite: int = 10) -> List[AddressEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = """SELECT address_id, address, address2, district, city_id, postal_code, phone, last_update
                       FROM address ORDER BY address_id DESC LIMIT %s"""
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [AddressEntity(
                address_id=f[0], address=f[1], address2=f[2], district=f[3],
                city_id=f[4], postal_code=f[5], phone=f[6], last_update=str(f[7])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer direcciones: {e}")
            return []

    # --- Store ---

    def crear_tienda(self, manager_staff_id: int, address_id: int) -> Optional[StoreEntity]:
        if not isinstance(manager_staff_id, int) or manager_staff_id <= 0:
            print("[ERROR] manager_staff_id debe ser un entero positivo")
            return None
        if not isinstance(address_id, int) or address_id <= 0:
            print("[ERROR] address_id debe ser un entero positivo")
            return None
        try:
            entity = StoreEntity(store_id=None, manager_staff_id=manager_staff_id, address_id=address_id)
            query = "INSERT INTO store (manager_staff_id, address_id) VALUES (%s, %s)"
            last_id = self.context.ejecutar_comando(query, (entity.manager_staff_id, entity.address_id))
            if last_id is not None:
                entity.store_id = last_id
                print(f"[CREATE] Tienda insertada (ID: {last_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear tienda: {e}")
            return None

    def leer_tiendas(self, limite: int = 10) -> List[StoreEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = "SELECT store_id, manager_staff_id, address_id, last_update FROM store ORDER BY store_id DESC LIMIT %s"
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [StoreEntity(
                store_id=f[0], manager_staff_id=f[1], address_id=f[2], last_update=str(f[3])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer tiendas: {e}")
            return []

    # --- Actor ---

    def crear_actor(self, first_name: str, last_name: str) -> Optional[ActorEntity]:
        if not first_name or not first_name.strip():
            print("[ERROR] Primer nombre no puede estar vacío")
            return None
        if not last_name or not last_name.strip():
            print("[ERROR] Apellido no puede estar vacío")
            return None
        try:
            entity = ActorEntity(actor_id=None, first_name=first_name.strip(), last_name=last_name.strip())
            query = "INSERT INTO actor (first_name, last_name) VALUES (%s, %s)"
            last_id = self.context.ejecutar_comando(query, (entity.first_name, entity.last_name))
            if last_id is not None:
                entity.actor_id = last_id
                print(f"[CREATE] Actor '{first_name} {last_name}' insertado (ID: {last_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear actor: {e}")
            return None

    def leer_actores(self, limite: int = 10) -> List[ActorEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = "SELECT actor_id, first_name, last_name, last_update FROM actor ORDER BY actor_id DESC LIMIT %s"
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [ActorEntity(
                actor_id=f[0], first_name=f[1], last_name=f[2], last_update=str(f[3])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer actores: {e}")
            return []

    def buscar_actor_por_nombre(self, nombre: str) -> List[ActorEntity]:
        if not nombre or not nombre.strip():
            print("[ERROR] Nombre a buscar no puede estar vacío")
            return []
        try:
            query = "SELECT actor_id, first_name, last_name, last_update FROM actor WHERE first_name LIKE %s OR last_name LIKE %s"
            pattern = f"%{nombre.strip()}%"
            filas = self.context.ejecutar_consulta(query, (pattern, pattern))
            return [ActorEntity(
                actor_id=f[0], first_name=f[1], last_name=f[2], last_update=str(f[3])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudo buscar actor: {e}")
            return []

    # --- Category ---

    def crear_categoria(self, nombre: str) -> Optional[CategoryEntity]:
        if not nombre or not nombre.strip():
            print("[ERROR] Nombre de categoría no puede estar vacío")
            return None
        try:
            entity = CategoryEntity(category_id=None, name=nombre.strip())
            query = "INSERT INTO category (name) VALUES (%s)"
            last_id = self.context.ejecutar_comando(query, (entity.name,))
            if last_id is not None:
                entity.category_id = last_id
                print(f"[CREATE] Categoría '{nombre}' insertada (ID: {last_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear categoría: {e}")
            return None

    def leer_categorias(self, limite: int = 20) -> List[CategoryEntity]:
        if limite <= 0:
            limite = 20
        try:
            query = "SELECT category_id, name, last_update FROM category ORDER BY category_id DESC LIMIT %s"
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [CategoryEntity(category_id=f[0], name=f[1], last_update=str(f[2])) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer categorías: {e}")
            return []

    # --- Staff ---

    def crear_staff(self, first_name: str, last_name: str, address_id: int,
                    store_id: int, username: str, email: str = None) -> Optional[StaffEntity]:
        if not first_name or not first_name.strip():
            print("[ERROR] Primer nombre no puede estar vacío")
            return None
        if not last_name or not last_name.strip():
            print("[ERROR] Apellido no puede estar vacío")
            return None
        if not isinstance(address_id, int) or address_id <= 0:
            print("[ERROR] address_id debe ser un entero positivo")
            return None
        if not isinstance(store_id, int) or store_id <= 0:
            print("[ERROR] store_id debe ser un entero positivo")
            return None
        if not username or not username.strip():
            print("[ERROR] Username no puede estar vacío")
            return None
        try:
            entity = StaffEntity(staff_id=None, first_name=first_name.strip(), last_name=last_name.strip(),
                                 address_id=address_id, email=email.strip() if email else None, store_id=store_id,
                                 active=1, username=username.strip(), password=None)
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
        except Exception as e:
            print(f"[ERROR] No se pudo crear staff: {e}")
            return None

    def leer_staff(self, limite: int = 10) -> List[StaffEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = """SELECT staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update
                       FROM staff ORDER BY staff_id DESC LIMIT %s"""
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [StaffEntity(
                staff_id=f[0], first_name=f[1], last_name=f[2], address_id=f[3],
                email=f[4], store_id=f[5], active=f[6], username=f[7], password=f[8], last_update=str(f[9])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer staff: {e}")
            return []

    # --- Customer ---

    def crear_cliente(self, store_id: int, first_name: str, last_name: str,
                      address_id: int, email: str = None) -> Optional[CustomerEntity]:
        if not isinstance(store_id, int) or store_id <= 0:
            print("[ERROR] store_id debe ser un entero positivo")
            return None
        if not first_name or not first_name.strip():
            print("[ERROR] Primer nombre no puede estar vacío")
            return None
        if not last_name or not last_name.strip():
            print("[ERROR] Apellido no puede estar vacío")
            return None
        if not isinstance(address_id, int) or address_id <= 0:
            print("[ERROR] address_id debe ser un entero positivo")
            return None
        try:
            entity = CustomerEntity(customer_id=None, store_id=store_id, first_name=first_name.strip(),
                                     last_name=last_name.strip(), email=email.strip() if email else None, address_id=address_id)
            query = """INSERT INTO customer (store_id, first_name, last_name, email, address_id, create_date)
                       VALUES (%s, %s, %s, %s, %s, NOW())"""
            params = (entity.store_id, entity.first_name, entity.last_name, entity.email, entity.address_id)
            last_id = self.context.ejecutar_comando(query, params)
            if last_id is not None:
                entity.customer_id = last_id
                print(f"[CREATE] Cliente '{first_name} {last_name}' insertado (ID: {last_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear cliente: {e}")
            return None

    def leer_clientes(self, limite: int = 10) -> List[CustomerEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = """SELECT customer_id, store_id, first_name, last_name, email, address_id, create_date, last_update
                       FROM customer ORDER BY customer_id DESC LIMIT %s"""
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [CustomerEntity(
                customer_id=f[0], store_id=f[1], first_name=f[2], last_name=f[3],
                email=f[4], address_id=f[5], create_date=str(f[6]), last_update=str(f[7])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer clientes: {e}")
            return []

    # --- Rental ---

    def crear_alquiler(self, inventory_id: int, customer_id: int, staff_id: int) -> Optional[RentalEntity]:
        if not isinstance(inventory_id, int) or inventory_id <= 0:
            print("[ERROR] inventory_id debe ser un entero positivo")
            return None
        if not isinstance(customer_id, int) or customer_id <= 0:
            print("[ERROR] customer_id debe ser un entero positivo")
            return None
        if not isinstance(staff_id, int) or staff_id <= 0:
            print("[ERROR] staff_id debe ser un entero positivo")
            return None
        try:
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
        except Exception as e:
            print(f"[ERROR] No se pudo crear alquiler: {e}")
            return None

    def leer_alquileres(self, limite: int = 10) -> List[RentalEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
                       FROM rental ORDER BY rental_id DESC LIMIT %s"""
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [RentalEntity(
                rental_id=f[0], rental_date=str(f[1]), inventory_id=f[2], customer_id=f[3],
                return_date=str(f[4]) if f[4] else None, staff_id=f[5], last_update=str(f[6])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer alquileres: {e}")
            return []

    def leer_alquileres_activos(self) -> List[RentalEntity]:
        try:
            query = """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
                       FROM rental WHERE return_date IS NULL ORDER BY rental_id DESC"""
            filas = self.context.ejecutar_consulta(query)
            return [RentalEntity(
                rental_id=f[0], rental_date=str(f[1]), inventory_id=f[2], customer_id=f[3],
                return_date=str(f[4]) if f[4] else None, staff_id=f[5], last_update=str(f[6])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer alquileres activos: {e}")
            return []

    # --- Payment ---

    def crear_pago(self, customer_id: int, staff_id: int, amount: float,
                   rental_id: int = None) -> Optional[PaymentEntity]:
        if not isinstance(customer_id, int) or customer_id <= 0:
            print("[ERROR] customer_id debe ser un entero positivo")
            return None
        if not isinstance(staff_id, int) or staff_id <= 0:
            print("[ERROR] staff_id debe ser un entero positivo")
            return None
        if not isinstance(amount, (int, float)) or amount < 0:
            print("[ERROR] amount debe ser un número no negativo")
            return None
        try:
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
        except Exception as e:
            print(f"[ERROR] No se pudo crear pago: {e}")
            return None

    def leer_pagos(self, limite: int = 10) -> List[PaymentEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = """SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date, last_update
                       FROM payment ORDER BY payment_id DESC LIMIT %s"""
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [PaymentEntity(
                payment_id=f[0], customer_id=f[1], staff_id=f[2], rental_id=f[3],
                amount=f[4], payment_date=str(f[5]), last_update=str(f[6])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer pagos: {e}")
            return []

    def total_pagos_cliente(self, customer_id: int) -> float:
        if not isinstance(customer_id, int) or customer_id <= 0:
            print("[ERROR] customer_id debe ser un entero positivo")
            return 0.0
        try:
            query = "SELECT COALESCE(SUM(amount), 0) FROM payment WHERE customer_id = %s"
            filas = self.context.ejecutar_consulta(query, (customer_id,))
            return float(filas[0][0]) if filas else 0.0
        except Exception as e:
            print(f"[ERROR] No se pudo calcular total de pagos: {e}")
            return 0.0

    # --- Inventory ---

    def crear_inventario(self, film_id: int, store_id: int) -> Optional[InventoryEntity]:
        if not isinstance(film_id, int) or film_id <= 0:
            print("[ERROR] film_id debe ser un entero positivo")
            return None
        if not isinstance(store_id, int) or store_id <= 0:
            print("[ERROR] store_id debe ser un entero positivo")
            return None
        try:
            entity = InventoryEntity(inventory_id=None, film_id=film_id, store_id=store_id)
            query = "INSERT INTO inventory (film_id, store_id) VALUES (%s, %s)"
            last_id = self.context.ejecutar_comando(query, (entity.film_id, entity.store_id))
            if last_id is not None:
                entity.inventory_id = last_id
                print(f"[CREATE] Inventario insertado (ID: {last_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear inventario: {e}")
            return None

    def leer_inventario_por_tienda(self, store_id: int) -> List[InventoryEntity]:
        if not isinstance(store_id, int) or store_id <= 0:
            print("[ERROR] store_id debe ser un entero positivo")
            return []
        try:
            query = "SELECT inventory_id, film_id, store_id, last_update FROM inventory WHERE store_id = %s"
            filas = self.context.ejecutar_consulta(query, (store_id,))
            return [InventoryEntity(
                inventory_id=f[0], film_id=f[1], store_id=f[2], last_update=str(f[3])
            ) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudo leer inventario: {e}")
            return []

    # --- Film Text ---

    def crear_film_text(self, film_id: int, title: str, description: str = None) -> Optional[FilmTextEntity]:
        if not isinstance(film_id, int) or film_id <= 0:
            print("[ERROR] film_id debe ser un entero positivo")
            return None
        if not title or not title.strip():
            print("[ERROR] Título no puede estar vacío")
            return None
        try:
            entity = FilmTextEntity(film_id=film_id, title=title.strip(), description=description)
            query = "INSERT INTO film_text (film_id, title, description) VALUES (%s, %s, %s)"
            last_id = self.context.ejecutar_comando(query, (entity.film_id, entity.title, entity.description))
            if last_id is not None:
                print(f"[CREATE] FilmText insertado (film_id: {film_id})")
                return entity
            return None
        except Exception as e:
            print(f"[ERROR] No se pudo crear film_text: {e}")
            return None

    def leer_film_text(self, limite: int = 10) -> List[FilmTextEntity]:
        if limite <= 0:
            limite = 10
        try:
            query = "SELECT film_id, title, description FROM film_text ORDER BY film_id DESC LIMIT %s"
            filas = self.context.ejecutar_consulta(query, (limite,))
            return [FilmTextEntity(film_id=f[0], title=f[1], description=f[2]) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudieron leer film_text: {e}")
            return []

    def buscar_film_text_por_titulo(self, titulo: str) -> List[FilmTextEntity]:
        if not titulo or not titulo.strip():
            print("[ERROR] Título a buscar no puede estar vacío")
            return []
        try:
            query = "SELECT film_id, title, description FROM film_text WHERE title LIKE %s"
            pattern = f"%{titulo.strip()}%"
            filas = self.context.ejecutar_consulta(query, (pattern,))
            return [FilmTextEntity(film_id=f[0], title=f[1], description=f[2]) for f in filas]
        except Exception as e:
            print(f"[ERROR] No se pudo buscar film_text: {e}")
            return []
