# =====================================================================
# MODELS - List<Entity> y Repository Pattern
# =====================================================================
# Transforma filas relacionales en colecciones tipadas List<Entity>.
# Abstrae el DbContext proporcionando métodos de negocio.

from typing import List, Optional
from src.dbcontext import DbContext
from src.entities import (
    CountryEntity, CityEntity, FilmEntity, InventoryEntity,
    LanguageEntity, AddressEntity, StoreEntity, ActorEntity,
    CategoryEntity, StaffEntity, CustomerEntity, RentalEntity, PaymentEntity,
    FilmTextEntity
)


class DataRepository:
    """
    Abstrae el DbContext transformando conjuntos relacionales en
    colecciones estructuradas List<Entity>.
    """

    def __init__(self, context: DbContext):
        self.context: DbContext = context

    # --- Country Operations ---

    def guardar_pais(self, entity: CountryEntity) -> bool:
        """Inserta un país y actualiza el entity con el ID generado."""
        query = "INSERT INTO country (country) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.country,))
        if last_id is not None:
            entity.country_id = last_id
            return True
        return False

    def listar_paises(self, limite: int = 10) -> List[CountryEntity]:
        """Transforma filas relacionales en List<CountryEntity>."""
        query = "SELECT country_id, country, last_update FROM country ORDER BY country_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        lista_modelos: List[CountryEntity] = []
        for f in filas:
            lista_modelos.append(CountryEntity(
                country_id=f[0],
                country=f[1],
                last_update=str(f[2])
            ))
        return lista_modelos

    def buscar_pais_por_nombre(self, nombre: str) -> Optional[CountryEntity]:
        """Busca un país por nombre exacto."""
        query = "SELECT country_id, country, last_update FROM country WHERE country = %s"
        filas = self.context.ejecutar_consulta(query, (nombre,))
        if filas:
            f = filas[0]
            return CountryEntity(country_id=f[0], country=f[1], last_update=str(f[2]))
        return None

    # --- City Operations ---

    def guardar_ciudad(self, entity: CityEntity) -> bool:
        """Inserta una ciudad y actualiza el entity con el ID generado."""
        query = "INSERT INTO city (city, country_id) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.city, entity.country_id))
        if last_id is not None:
            entity.city_id = last_id
            return True
        return False

    def listar_ciudades(self, limite: int = 10) -> List[CityEntity]:
        """Transforma filas relacionales en List<CityEntity>."""
        query = "SELECT city_id, city, country_id, last_update FROM city ORDER BY city_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        lista_modelos: List[CityEntity] = []
        for f in filas:
            lista_modelos.append(CityEntity(
                city_id=f[0],
                city=f[1],
                country_id=f[2],
                last_update=str(f[3])
            ))
        return lista_modelos

    def listar_ciudades_con_pais(self, limite: int = 10) -> List[tuple]:
        """Retorna ciudades con nombre del país (JOIN)."""
        query = """SELECT c.city_id, c.city, c.country_id, co.country, c.last_update
                   FROM city c
                   INNER JOIN country co ON c.country_id = co.country_id
                   ORDER BY c.city_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return filas

    def eliminar_ciudad_por_id(self, id_ciudad: int) -> bool:
        """Elimina una ciudad por su ID."""
        query = "DELETE FROM city WHERE city_id = %s"
        last_id = self.context.ejecutar_comando(query, (id_ciudad,))
        return last_id is not None

    # --- Film Operations ---

    def guardar_pelicula(self, entity: FilmEntity) -> bool:
        """Inserta una película y actualiza el entity con el ID generado."""
        query = """INSERT INTO film (title, description, release_year, rental_rate, length, replacement_cost, rating)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        params = (entity.title, entity.description, entity.release_year,
                  entity.rental_rate, entity.length, entity.replacement_cost, entity.rating)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.film_id = last_id
            return True
        return False

    def buscar_pelicula_por_id(self, id_pelicula: int) -> Optional[FilmEntity]:
        """Busca una película por su ID."""
        query = """SELECT film_id, title, rental_rate, length, replacement_cost, release_year,
                   description, rating FROM film WHERE film_id = %s"""
        filas = self.context.ejecutar_consulta(query, (id_pelicula,))
        if filas:
            f = filas[0]
            return FilmEntity(
                film_id=f[0], title=f[1], rental_rate=f[2], length=f[3],
                replacement_cost=f[4], release_year=f[5], description=f[6], rating=f[7]
            )
        return None

    def listar_peliculas(self, limite: int = 10) -> List[FilmEntity]:
        """Transforma filas relacionales en List<FilmEntity>."""
        query = """SELECT film_id, title, rental_rate, length, replacement_cost, release_year,
                   description, rating FROM film ORDER BY film_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        lista_modelos: List[FilmEntity] = []
        for f in filas:
            lista_modelos.append(FilmEntity(
                film_id=f[0], title=f[1], rental_rate=f[2], length=f[3],
                replacement_cost=f[4], release_year=f[5], description=f[6], rating=f[7]
            ))
        return lista_modelos

    def actualizar_tarifa_pelicula(self, entity: FilmEntity) -> bool:
        """Actualiza la tarifa de alquiler de una película."""
        query = "UPDATE film SET rental_rate = %s WHERE film_id = %s"
        last_id = self.context.ejecutar_comando(query, (entity.rental_rate, entity.film_id))
        return last_id is not None

    def eliminar_pelicula_por_id(self, id_pelicula: int) -> bool:
        """Elimina una película por su ID."""
        query = "DELETE FROM film WHERE film_id = %s"
        last_id = self.context.ejecutar_comando(query, (id_pelicula,))
        return last_id is not None

    # --- Inventory Operations ---

    def guardar_inventario(self, entity: InventoryEntity) -> bool:
        """Inserta un registro de inventario."""
        query = "INSERT INTO inventory (film_id, store_id) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.film_id, entity.store_id))
        if last_id is not None:
            entity.inventory_id = last_id
            return True
        return False

    def listar_inventario_por_tienda(self, store_id: int) -> List[InventoryEntity]:
        """Lista inventario de una tienda específica."""
        query = "SELECT inventory_id, film_id, store_id, last_update FROM inventory WHERE store_id = %s"
        filas = self.context.ejecutar_consulta(query, (store_id,))
        lista_modelos: List[InventoryEntity] = []
        for f in filas:
            lista_modelos.append(InventoryEntity(
                inventory_id=f[0], film_id=f[1], store_id=f[2], last_update=str(f[3])
            ))
        return lista_modelos

    # --- Language Operations ---

    def guardar_idioma(self, entity: LanguageEntity) -> bool:
        """Inserta un idioma."""
        query = "INSERT INTO language (name) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.name,))
        if last_id is not None:
            entity.language_id = last_id
            return True
        return False

    def listar_idiomas(self, limite: int = 10) -> List[LanguageEntity]:
        """Lista idiomas."""
        query = "SELECT language_id, name, last_update FROM language ORDER BY language_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [LanguageEntity(language_id=f[0], name=f[1], last_update=str(f[2])) for f in filas]

    # --- Address Operations ---

    def guardar_direccion(self, entity: AddressEntity) -> bool:
        """Inserta una dirección."""
        query = """INSERT INTO address (address, address2, district, city_id, postal_code, phone)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (entity.address, entity.address2, entity.district, entity.city_id,
                  entity.postal_code, entity.phone)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.address_id = last_id
            return True
        return False

    def listar_direcciones(self, limite: int = 10) -> List[AddressEntity]:
        """Lista direcciones."""
        query = """SELECT address_id, address, address2, district, city_id, postal_code, phone, last_update
                   FROM address ORDER BY address_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [AddressEntity(
            address_id=f[0], address=f[1], address2=f[2], district=f[3],
            city_id=f[4], postal_code=f[5], phone=f[6], last_update=str(f[7])
        ) for f in filas]

    # --- Store Operations ---

    def guardar_tienda(self, entity: StoreEntity) -> bool:
        """Inserta una tienda."""
        query = "INSERT INTO store (manager_staff_id, address_id) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.manager_staff_id, entity.address_id))
        if last_id is not None:
            entity.store_id = last_id
            return True
        return False

    def listar_tiendas(self, limite: int = 10) -> List[StoreEntity]:
        """Lista tiendas."""
        query = "SELECT store_id, manager_staff_id, address_id, last_update FROM store ORDER BY store_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [StoreEntity(
            store_id=f[0], manager_staff_id=f[1], address_id=f[2], last_update=str(f[3])
        ) for f in filas]

    # --- Actor Operations ---

    def guardar_actor(self, entity: ActorEntity) -> bool:
        """Inserta un actor."""
        query = "INSERT INTO actor (first_name, last_name) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.first_name, entity.last_name))
        if last_id is not None:
            entity.actor_id = last_id
            return True
        return False

    def listar_actores(self, limite: int = 10) -> List[ActorEntity]:
        """Lista actores."""
        query = "SELECT actor_id, first_name, last_name, last_update FROM actor ORDER BY actor_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [ActorEntity(
            actor_id=f[0], first_name=f[1], last_name=f[2], last_update=str(f[3])
        ) for f in filas]

    def buscar_actor_por_nombre(self, nombre: str) -> List[ActorEntity]:
        """Busca actores por nombre ( LIKE %nombre% )."""
        query = "SELECT actor_id, first_name, last_name, last_update FROM actor WHERE first_name LIKE %s OR last_name LIKE %s"
        pattern = f"%{nombre}%"
        filas = self.context.ejecutar_consulta(query, (pattern, pattern))
        return [ActorEntity(
            actor_id=f[0], first_name=f[1], last_name=f[2], last_update=str(f[3])
        ) for f in filas]

    # --- Category Operations ---

    def guardar_categoria(self, entity: CategoryEntity) -> bool:
        """Inserta una categoría."""
        query = "INSERT INTO category (name) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.name,))
        if last_id is not None:
            entity.category_id = last_id
            return True
        return False

    def listar_categorias(self, limite: int = 10) -> List[CategoryEntity]:
        """Lista categorías."""
        query = "SELECT category_id, name, last_update FROM category ORDER BY category_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [CategoryEntity(
            category_id=f[0], name=f[1], last_update=str(f[2])
        ) for f in filas]

    # --- Staff Operations ---

    def guardar_staff(self, entity: StaffEntity) -> bool:
        """Inserta un empleado."""
        query = """INSERT INTO staff (first_name, last_name, address_id, email, store_id, active, username, password)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (entity.first_name, entity.last_name, entity.address_id, entity.email,
                  entity.store_id, entity.active, entity.username, entity.password)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.staff_id = last_id
            return True
        return False

    def listar_staff(self, limite: int = 10) -> List[StaffEntity]:
        """Lista empleados."""
        query = """SELECT staff_id, first_name, last_name, address_id, email, store_id, active, username, password, last_update
                   FROM staff ORDER BY staff_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [StaffEntity(
            staff_id=f[0], first_name=f[1], last_name=f[2], address_id=f[3],
            email=f[4], store_id=f[5], active=f[6], username=f[7], password=f[8], last_update=str(f[9])
        ) for f in filas]

    # --- Customer Operations ---

    def guardar_cliente(self, entity: CustomerEntity) -> bool:
        """Inserta un cliente."""
        query = """INSERT INTO customer (store_id, first_name, last_name, email, address_id, create_date)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        params = (entity.store_id, entity.first_name, entity.last_name, entity.email,
                  entity.address_id, entity.create_date)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.customer_id = last_id
            return True
        return False

    def listar_clientes(self, limite: int = 10) -> List[CustomerEntity]:
        """Lista clientes."""
        query = """SELECT customer_id, store_id, first_name, last_name, email, address_id, create_date, last_update
                   FROM customer ORDER BY customer_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [CustomerEntity(
            customer_id=f[0], store_id=f[1], first_name=f[2], last_name=f[3],
            email=f[4], address_id=f[5], create_date=str(f[6]), last_update=str(f[7])
        ) for f in filas]

    # --- Rental Operations ---

    def guardar_alquiler(self, entity: RentalEntity) -> bool:
        """Inserta un alquiler."""
        query = """INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id)
                   VALUES (%s, %s, %s, %s, %s)"""
        params = (entity.rental_date, entity.inventory_id, entity.customer_id,
                  entity.return_date, entity.staff_id)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.rental_id = last_id
            return True
        return False

    def listar_alquileres(self, limite: int = 10) -> List[RentalEntity]:
        """Lista alquileres."""
        query = """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
                   FROM rental ORDER BY rental_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [RentalEntity(
            rental_id=f[0], rental_date=str(f[1]), inventory_id=f[2], customer_id=f[3],
            return_date=str(f[4]) if f[4] else None, staff_id=f[5], last_update=str(f[6])
        ) for f in filas]

    def listar_alquileres_activos(self) -> List[RentalEntity]:
        """Lista alquileres sin devolver (return_date IS NULL)."""
        query = """SELECT rental_id, rental_date, inventory_id, customer_id, return_date, staff_id, last_update
                   FROM rental WHERE return_date IS NULL ORDER BY rental_id DESC"""
        filas = self.context.ejecutar_consulta(query)
        return [RentalEntity(
            rental_id=f[0], rental_date=str(f[1]), inventory_id=f[2], customer_id=f[3],
            return_date=str(f[4]) if f[4] else None, staff_id=f[5], last_update=str(f[6])
        ) for f in filas]

    # --- Payment Operations ---

    def guardar_pago(self, entity: PaymentEntity) -> bool:
        """Inserta un pago."""
        query = """INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date)
                   VALUES (%s, %s, %s, %s, %s)"""
        params = (entity.customer_id, entity.staff_id, entity.rental_id,
                  entity.amount, entity.payment_date)
        last_id = self.context.ejecutar_comando(query, params)
        if last_id is not None:
            entity.payment_id = last_id
            return True
        return False

    def listar_pagos(self, limite: int = 10) -> List[PaymentEntity]:
        """Lista pagos."""
        query = """SELECT payment_id, customer_id, staff_id, rental_id, amount, payment_date, last_update
                   FROM payment ORDER BY payment_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [PaymentEntity(
            payment_id=f[0], customer_id=f[1], staff_id=f[2], rental_id=f[3],
            amount=f[4], payment_date=str(f[5]), last_update=str(f[6])
        ) for f in filas]

    def calcular_total_pagos_por_cliente(self, customer_id: int) -> float:
        """Calcula el total de pagos de un cliente."""
        query = "SELECT COALESCE(SUM(amount), 0) FROM payment WHERE customer_id = %s"
        filas = self.context.ejecutar_consulta(query, (customer_id,))
        return float(filas[0][0]) if filas else 0.0

    # --- Film Text Operations ---

    def guardar_film_text(self, entity: FilmTextEntity) -> bool:
        """Inserta un registro film_text."""
        query = "INSERT INTO film_text (film_id, title, description) VALUES (%s, %s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.film_id, entity.title, entity.description))
        return last_id is not None

    def listar_film_text(self, limite: int = 10) -> List[FilmTextEntity]:
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
