# =====================================================================
# MODELS - List<Entity> y Repository Pattern
# =====================================================================
# Transforma filas relacionales en colecciones tipadas List<Entity>.
# Abstrae el DbContext proporcionando métodos de negocio.

from typing import List, Optional
from src.dbcontext import DbContext
from src.entities import CountryEntity, CityEntity, FilmEntity, InventoryEntity


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
