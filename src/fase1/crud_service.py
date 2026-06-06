# =====================================================================
# CRUD SERVICE - Operaciones de Creación, Lectura, Actualización, Eliminación
# =====================================================================

from typing import List, Optional
from src.dbcontext import DbContext
from src.entities import CountryEntity, CityEntity, FilmEntity


class CrudService:
    """Servicio para operaciones CRUD sobre Country, City y Film."""

    def __init__(self):
        self.context = DbContext()

    def crear_pais(self, nombre: str) -> Optional[CountryEntity]:
        """Crea un nuevo país. Retorna el entity con ID generado."""
        entity = CountryEntity(country_id=None, country=nombre)
        query = "INSERT INTO country (country) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.country,))
        if last_id is not None:
            entity.country_id = last_id
            print(f"[CREATE] País '{nombre}' insertado (ID: {last_id})")
            return entity
        return None

    def leer_paises(self, limite: int = 10) -> List[CountryEntity]:
        """Retorna lista de países ordenados por ID descendente."""
        query = "SELECT country_id, country, last_update FROM country ORDER BY country_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [CountryEntity(country_id=f[0], country=f[1], last_update=str(f[2])) for f in filas]

    def crear_ciudad(self, nombre: str, country_id: int) -> Optional[CityEntity]:
        """Crea una ciudad vinculada a un país."""
        entity = CityEntity(city_id=None, city=nombre, country_id=country_id)
        query = "INSERT INTO city (city, country_id) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.city, entity.country_id))
        if last_id is not None:
            entity.city_id = last_id
            print(f"[CREATE] Ciudad '{nombre}' vinculada al país ID {country_id} (ID: {last_id})")
            return entity
        return None

    def leer_ciudades(self, limite: int = 10) -> List[tuple]:
        """Retorna lista de ciudades con nombre del país (JOIN)."""
        query = """SELECT c.city_id, c.city, c.country_id, co.country, c.last_update
                   FROM city c
                   INNER JOIN country co ON c.country_id = co.country_id
                   ORDER BY c.city_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return filas

    def actualizar_tarifa_pelicula(self, film_id: int, nueva_tarifa: float) -> bool:
        """Actualiza la tarifa de alquiler de una película."""
        query = "UPDATE film SET rental_rate = %s WHERE film_id = %s"
        result = self.context.ejecutar_comando(query, (nueva_tarifa, film_id))
        if result:
            print(f"[UPDATE] Película ID {film_id} actualizada con tarifa ${nueva_tarifa}")
        return result is not None

    def leer_peliculas(self, limite: int = 10) -> List[FilmEntity]:
        """Retorna lista de películas ordenadas por ID descendente."""
        query = """SELECT film_id, title, rental_rate, length, replacement_cost,
 release_year, description, rating FROM film ORDER BY film_id DESC LIMIT %s"""
        filas = self.context.ejecutar_consulta(query, (limite,))
        return [FilmEntity(
            film_id=f[0], title=f[1], rental_rate=f[2], length=f[3],
            replacement_cost=f[4], release_year=f[5], description=f[6], rating=f[7]
        ) for f in filas]

    def eliminar_ciudad(self, city_id: int) -> bool:
        """Elimina una ciudad por su ID."""
        query = "DELETE FROM city WHERE city_id = %s"
        result = self.context.ejecutar_comando(query, (city_id,))
        if result:
            print(f"[DELETE] Ciudad ID {city_id} eliminada")
        return result is not None

    def buscar_pelicula_por_id(self, film_id: int) -> Optional[FilmEntity]:
        """Busca una película por su ID."""
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
