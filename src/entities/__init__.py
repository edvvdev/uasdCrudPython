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


class LanguageEntity:
    """Mapeo de la tabla 'language' en el DBMS."""

    def __init__(self, language_id: Optional[int], name: str, last_update: Optional[str] = None):
        self.language_id: Optional[int] = language_id
        self.name: str = name
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<LanguageEntity id={self.language_id} name='{self.name}'>"


class AddressEntity:
    """Mapeo de la tabla 'address' en el DBMS."""

    def __init__(self, address_id: Optional[int], address: str, address2: Optional[str],
 district: str, city_id: int, postal_code: Optional[str], phone: str,
                 last_update: Optional[str] = None):
        self.address_id: Optional[int] = address_id
        self.address: str = address
        self.address2: Optional[str] = address2
        self.district: str = district
        self.city_id: int = city_id
        self.postal_code: Optional[str] = postal_code
        self.phone: str = phone
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<AddressEntity id={self.address_id} address='{self.address}' district='{self.district}'>"


class StoreEntity:
    """Mapeo de la tabla 'store' en el DBMS."""

    def __init__(self, store_id: Optional[int], manager_staff_id: int, address_id: int,
                 last_update: Optional[str] = None):
        self.store_id: Optional[int] = store_id
        self.manager_staff_id: int = manager_staff_id
        self.address_id: int = address_id
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<StoreEntity id={self.store_id} manager_staff_id={self.manager_staff_id}>"


class ActorEntity:
    """Mapeo de la tabla 'actor' en el DBMS."""

    def __init__(self, actor_id: Optional[int], first_name: str, last_name: str,
                 last_update: Optional[str] = None):
        self.actor_id: Optional[int] = actor_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<ActorEntity id={self.actor_id} name='{self.first_name} {self.last_name}'>"


class CategoryEntity:
    """Mapeo de la tabla 'category' en el DBMS."""

    def __init__(self, category_id: Optional[int], name: str, last_update: Optional[str] = None):
        self.category_id: Optional[int] = category_id
        self.name: str = name
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<CategoryEntity id={self.category_id} name='{self.name}'>"


class StaffEntity:
    """Mapeo de la tabla 'staff' en el DBMS."""

    def __init__(self, staff_id: Optional[int], first_name: str, last_name: str,
                 address_id: int, email: Optional[str], store_id: int, active: int,
                 username: str, password: Optional[str] = None, last_update: Optional[str] = None):
        self.staff_id: Optional[int] = staff_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.address_id: int = address_id
        self.email: Optional[str] = email
        self.store_id: int = store_id
        self.active: int = active
        self.username: str = username
        self.password: Optional[str] = password
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<StaffEntity id={self.staff_id} username='{self.username}'>"


class CustomerEntity:
    """Mapeo de la tabla 'customer' en el DBMS."""

    def __init__(self, customer_id: Optional[int], store_id: int, first_name: str,
                 last_name: str, email: Optional[str], address_id: int,
                 create_date: Optional[str] = None, last_update: Optional[str] = None):
        self.customer_id: Optional[int] = customer_id
        self.store_id: int = store_id
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: Optional[str] = email
        self.address_id: int = address_id
        self.create_date: Optional[str] = create_date
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<CustomerEntity id={self.customer_id} name='{self.first_name} {self.last_name}'>"


class RentalEntity:
    """Mapeo de la tabla 'rental' en el DBMS."""

    def __init__(self, rental_id: Optional[int], rental_date: str, inventory_id: int,
                 customer_id: int, return_date: Optional[str], staff_id: int,
                 last_update: Optional[str] = None):
        self.rental_id: Optional[int] = rental_id
        self.rental_date: str = rental_date
        self.inventory_id: int = inventory_id
        self.customer_id: int = customer_id
        self.return_date: Optional[str] = return_date
        self.staff_id: int = staff_id
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<RentalEntity id={self.rental_id} customer_id={self.customer_id} inventory_id={self.inventory_id}>"


class PaymentEntity:
    """Mapeo de la tabla 'payment' en el DBMS."""

    def __init__(self, payment_id: Optional[int], customer_id: int, staff_id: int,
                 rental_id: Optional[int], amount: float, payment_date: str,
                 last_update: Optional[str] = None):
        self.payment_id: Optional[int] = payment_id
        self.customer_id: int = customer_id
        self.staff_id: int = staff_id
        self.rental_id: Optional[int] = rental_id
        self.amount: float = float(amount)
        self.payment_date: str = payment_date
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<PaymentEntity id={self.payment_id} amount=${self.amount}>"


class FilmTextEntity:
    """Mapeo de la tabla 'film_text' en el DBMS."""

    def __init__(self, film_id: int, title: str, description: Optional[str] = None):
        self.film_id: int = film_id
        self.title: str = title
        self.description: Optional[str] = description

    def __repr__(self) -> str:
        return f"<FilmTextEntity id={self.film_id} title='{self.title}'>"


__all__ = [
    'CountryEntity', 'CityEntity', 'FilmEntity', 'InventoryEntity',
    'LanguageEntity', 'AddressEntity', 'StoreEntity', 'ActorEntity',
    'CategoryEntity', 'StaffEntity', 'CustomerEntity', 'RentalEntity', 'PaymentEntity',
    'FilmTextEntity'
]
