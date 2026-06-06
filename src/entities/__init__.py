# src/entities/__init__.py
# Entities module - exports all entity classes

from typing import Optional


class CountryEntity:
    """Mapeo de la tabla 'country' en el DBMS."""

    def __init__(self, country_id: Optional[int], country: str, last_update: Optional[str] = None):
        self.country_id: Optional[int] = country_id
        self.country: str = country
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<CountryEntity id={self.country_id} name='{self.country}'>"


class CityEntity:
    """Mapeo de la tabla 'city' en el DBMS."""

    def __init__(self, city_id: Optional[int], city: str, country_id: int, last_update: Optional[str] = None):
        self.city_id: Optional[int] = city_id
        self.city: str = city
        self.country_id: int = country_id
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<CityEntity id={self.city_id} name='{self.city}' fk_country={self.country_id}>"


class FilmEntity:
    """Mapeo de la tabla 'film' en el DBMS."""

    def __init__(self, film_id: Optional[int], title: str, rental_rate: float,
                 length: int, replacement_cost: float, release_year: Optional[int] = None,
                 description: Optional[str] = None, rating: Optional[str] = None):
        self.film_id: Optional[int] = film_id
        self.title: str = title
        self.rental_rate: float = float(rental_rate)
        self.length: int = length
        self.replacement_cost: float = float(replacement_cost)
        self.release_year: Optional[int] = release_year
        self.description: Optional[str] = description
        self.rating: Optional[str] = rating

    def __repr__(self) -> str:
        return f"<FilmEntity id={self.film_id} title='{self.title}' rate=${self.rental_rate}>"


class InventoryEntity:
    """Mapeo de la tabla 'inventory' en el DBMS."""

    def __init__(self, inventory_id: Optional[int], film_id: int, store_id: int, last_update: Optional[str] = None):
        self.inventory_id: Optional[int] = inventory_id
        self.film_id: int = film_id
        self.store_id: int = store_id
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<InventoryEntity id={self.inventory_id} film_id={self.film_id} store_id={self.store_id}>"


__all__ = ['CountryEntity', 'CityEntity', 'FilmEntity', 'InventoryEntity']
