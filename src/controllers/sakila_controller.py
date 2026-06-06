# =====================================================================
# CONTROLLER - Orquestador de Flujo de Negocio
# =====================================================================
# Controlador central que orquesta el flujo de operaciones de negocio.
# Separa la lógica de aplicación de la lógica de acceso a datos.

from typing import List
from src.dbcontext import DbContext
from src.models.data_repository import DataRepository
from src.entities import (
    CountryEntity, CityEntity, FilmEntity, ActorEntity, CategoryEntity,
    StaffEntity, CustomerEntity, RentalEntity, PaymentEntity
)


class SakilaWorkflowController:
    """
    Controlador que orquesta el flujo de negocio e interactúa con el cliente.
    Implementa el patrón Controller para desacoplar lógica de negocio de datos.
    """

    def __init__(self):
        self.context = DbContext()
        self.repository = DataRepository(self.context)

    # --- Country / City ---

    def crear_pais(self, nombre: str) -> CountryEntity:
        pais = CountryEntity(country_id=None, country=nombre)
        if self.repository.guardar_pais(pais):
            return pais
        return pais

    def crear_ciudad(self, nombre: str, country_id: int) -> CityEntity:
        ciudad = CityEntity(city_id=None, city=nombre, country_id=country_id)
        if self.repository.guardar_ciudad(ciudad):
            return ciudad
        return ciudad

    def obtener_paises(self, limite: int = 10) -> List[CountryEntity]:
        return self.repository.listar_paises(limite)

    def obtener_ciudades(self, limite: int = 10) -> List[tuple]:
        return self.repository.listar_ciudades_con_pais(limite)

    def eliminar_ciudad(self, city_id: int) -> bool:
        return self.repository.eliminar_ciudad_por_id(city_id)

    # --- Film ---

    def obtener_pelicula(self, film_id: int) -> FilmEntity:
        return self.repository.buscar_pelicula_por_id(film_id)

    def obtener_peliculas(self, limite: int = 10) -> List[FilmEntity]:
        return self.repository.listar_peliculas(limite)

    def actualizar_tarifa(self, film_id: int, nueva_tarifa: float) -> bool:
        pelicula = self.repository.buscar_pelicula_por_id(film_id)
        if pelicula:
            pelicula.rental_rate = nueva_tarifa
            return self.repository.actualizar_tarifa_pelicula(pelicula)
        return False

    def eliminar_pelicula(self, film_id: int) -> bool:
        return self.repository.eliminar_pelicula_por_id(film_id)

    # --- Actor ---

    def crear_actor(self, first_name: str, last_name: str) -> ActorEntity:
        actor = ActorEntity(actor_id=None, first_name=first_name, last_name=last_name)
        if self.repository.guardar_actor(actor):
            return actor
        return actor

    def obtener_actores(self, limite: int = 10) -> List[ActorEntity]:
        return self.repository.listar_actores(limite)

    def buscar_actores(self, nombre: str) -> List[ActorEntity]:
        return self.repository.buscar_actor_por_nombre(nombre)

    # --- Category ---

    def crear_categoria(self, nombre: str) -> CategoryEntity:
        cat = CategoryEntity(category_id=None, name=nombre)
        if self.repository.guardar_categoria(cat):
            return cat
        return cat

    def obtener_categorias(self, limite: int = 20) -> List[CategoryEntity]:
        return self.repository.listar_categorias(limite)

    # --- Staff ---

    def crear_staff(self, first_name: str, last_name: str, address_id: int,
                    store_id: int, username: str, email: str = None) -> StaffEntity:
        staff = StaffEntity(staff_id=None, first_name=first_name, last_name=last_name,
                            address_id=address_id, email=email, store_id=store_id,
                            active=1, username=username, password=None)
        if self.repository.guardar_staff(staff):
            return staff
        return staff

    def obtener_staff(self, limite: int = 10) -> List[StaffEntity]:
        return self.repository.listar_staff(limite)

    # --- Customer ---

    def crear_cliente(self, store_id: int, first_name: str, last_name: str,
                      address_id: int, email: str = None) -> CustomerEntity:
        cust = CustomerEntity(customer_id=None, store_id=store_id, first_name=first_name,
                               last_name=last_name, email=email, address_id=address_id)
        if self.repository.guardar_cliente(cust):
            return cust
        return cust

    def obtener_clientes(self, limite: int = 10) -> List[CustomerEntity]:
        return self.repository.listar_clientes(limite)

    # --- Rental ---

    def crear_alquiler(self, inventory_id: int, customer_id: int, staff_id: int) -> RentalEntity:
        rental = RentalEntity(rental_id=None, rental_date="NOW()", inventory_id=inventory_id,
                              customer_id=customer_id, return_date=None, staff_id=staff_id)
        if self.repository.guardar_alquiler(rental):
            return rental
        return rental

    def obtener_alquileres(self, limite: int = 10) -> List[RentalEntity]:
        return self.repository.listar_alquileres(limite)

    def obtener_alquileres_activos(self) -> List[RentalEntity]:
        return self.repository.listar_alquileres_activos()

    # --- Payment ---

    def crear_pago(self, customer_id: int, staff_id: int, amount: float,
                   rental_id: int = None) -> PaymentEntity:
        payment = PaymentEntity(payment_id=None, customer_id=customer_id, staff_id=staff_id,
                                rental_id=rental_id, amount=amount, payment_date="NOW()")
        if self.repository.guardar_pago(payment):
            return payment
        return payment

    def obtener_pagos(self, limite: int = 10) -> List[PaymentEntity]:
        return self.repository.listar_pagos(limite)

    def total_pagos_cliente(self, customer_id: int) -> float:
        return self.repository.calcular_total_pagos_por_cliente(customer_id)

    # --- Flujo Completo ---

    def procesar_flujo_completo(self) -> None:
        """Ejecuta el flujo completo de demostración del ORM."""
        print("=" * 70)
        print("    INGENIERÍA DE SOFTWARE FASE II: ORM POO - ARQUITECTURA MODULAR")
        print("=" * 70)

        print("\n[1/8] Creando entidad Country en memoria...")
        pais = CountryEntity(country_id=None, country="Portugal")
        print(f"   Pre-persistencia: {pais}")
        if self.repository.guardar_pais(pais):
            print(f"   Post-persistencia (ID generado): {pais}")

        print("\n[2/8] Forzando duplicado para auditar Unique Constraint...")
        pais_duplicado = CountryEntity(country_id=None, country="Portugal")
        self.repository.guardar_pais(pais_duplicado)

        print("\n[3/8] Hidratando List<CountryEntity> desde repositorio...")
        coleccion_paises = self.repository.listar_paises(limite=3)
        print(f"   Tipo: {type(coleccion_paises)}")
        for p in coleccion_paises:
            print(f"     -> {p} | {type(p).__name__}")

        print("\n[4/8] Creando ciudad vinculada a país...")
        if pais.country_id:
            ciudad = CityEntity(city_id=None, city="Lisboa", country_id=pais.country_id)
            if self.repository.guardar_ciudad(ciudad):
                print(f"   Ciudad persistida: {ciudad}")

        print("\n[5/8] Modificando FilmEntity y sincronizando...")
        pelicula = self.repository.buscar_pelicula_por_id(id_pelicula=2)
        if pelicula:
            print(f"   Original: {pelicula}")
            pelicula.rental_rate = 8.99
            if self.repository.actualizar_tarifa_pelicula(pelicula):
                act = self.repository.buscar_pelicula_por_id(2)
                print(f"   Sincronizado: {act}")

        print("\n[6/8] Creando Actor (ORM Entity)...")
        actor = ActorEntity(actor_id=None, first_name="Tom", last_name="Cruise")
        if self.repository.guardar_actor(actor):
            print(f"   Actor persistido: {actor}")

        print("\n[7/8] Creando Category...")
        cat = CategoryEntity(category_id=None, name="Sci-Fi")
        if self.repository.guardar_categoria(cat):
            print(f"   Categoría persistida: {cat}")

        print("\n[8/8] Eliminando entidad via capa intermedia...")
        self.repository.eliminar_ciudad_por_id(id_ciudad=1)

        print("\n" + "=" * 70)
        print(" 🏁 ARQUITECTURA MODULAR COMPLETADA - FASE II VALIDADA")
        print("=" * 70)
