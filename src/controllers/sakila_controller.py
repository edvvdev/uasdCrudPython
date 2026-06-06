# =====================================================================
# CONTROLLER - Orquestador de Flujo de Negocio
# =====================================================================
# Controlador central que orquesta el flujo de operaciones de negocio.
# Separa la lógica de aplicación de la lógica de acceso a datos.

from typing import List
from src.dbcontext import DbContext
from src.models.data_repository import DataRepository
from src.entities import CountryEntity, CityEntity, FilmEntity


class SakilaWorkflowController:
    """
    Controlador que orquesta el flujo de negocio e interactúa con el cliente.
    Implementa el patrón Controller para desacoplar lógica de negocio de datos.
    """

    def __init__(self):
        self.context = DbContext()
        self.repository = DataRepository(self.context)

    def crear_pais(self, nombre: str) -> CountryEntity:
        """Crea un nuevo país en el sistema."""
        pais = CountryEntity(country_id=None, country=nombre)
        if self.repository.guardar_pais(pais):
            return pais
        return pais

    def crear_ciudad(self, nombre: str, country_id: int) -> CityEntity:
        """Crea una nueva ciudad vinculada a un país."""
        ciudad = CityEntity(city_id=None, city=nombre, country_id=country_id)
        if self.repository.guardar_ciudad(ciudad):
            return ciudad
        return ciudad

    def obtener_paises(self, limite: int = 10) -> List[CountryEntity]:
        """Obtiene lista de países ordenados por ID."""
        return self.repository.listar_paises(limite)

    def obtener_ciudades(self, limite: int = 10) -> List[CityEntity]:
        """Obtiene lista de ciudades ordenadas por ID."""
        return self.repository.listar_ciudades(limite)

    def obtener_pelicula(self, film_id: int) -> FilmEntity:
        """Obtiene una película por su ID."""
        return self.repository.buscar_pelicula_por_id(film_id)

    def obtener_peliculas(self, limite: int = 10) -> List[FilmEntity]:
        """Obtiene lista de películas."""
        return self.repository.listar_peliculas(limite)

    def actualizar_tarifa(self, film_id: int, nueva_tarifa: float) -> bool:
        """Actualiza la tarifa de alquiler de una película."""
        pelicula = self.repository.buscar_pelicula_por_id(film_id)
        if pelicula:
            pelicula.rental_rate = nueva_tarifa
            return self.repository.actualizar_tarifa_pelicula(pelicula)
        return False

    def eliminar_ciudad(self, city_id: int) -> bool:
        """Elimina una ciudad por su ID."""
        return self.repository.eliminar_ciudad_por_id(city_id)

    def eliminar_pelicula(self, film_id: int) -> bool:
        """Elimina una película por su ID."""
        return self.repository.eliminar_pelicula_por_id(film_id)

    def procesar_flujo_completo(self) -> None:
        """Ejecuta el flujo completo de demostración del ORM."""
        print("=" * 70)
        print("    INGENIERÍA DE SOFTWARE FASE II: ORM POO - ARQUITECTURA MODULAR")
        print("=" * 70)

        # 1. Crear país
        print("\n[CONTROLLER] -> Creando entidad Country en memoria...")
        pais = CountryEntity(country_id=None, country="Portugal")
        print(f"   Estado pre-persistencia: {pais}")

        if self.repository.guardar_pais(pais):
            print(f"   Estado post-persistencia (ID generado): {pais}")

        # 2. Forzar duplicado para auditar Unique Constraint
        print("\n[CONTROLLER] -> Forzando duplicado para auditar robustez...")
        pais_duplicado = CountryEntity(country_id=None, country="Portugal")
        self.repository.guardar_pais(pais_duplicado)

        # 3. Hidratar List<CountryEntity>
        print("\n[CONTROLLER] -> Hidratando List<CountryEntity> desde repositorio...")
        coleccion_paises: List[CountryEntity] = self.repository.listar_paises(limite=3)
        print(f"   Tipo de estructura: {type(coleccion_paises)}")
        for pais_item in coleccion_paises:
            print(f"     -> {pais_item} | Tipo: {type(pais_item).__name__}")

        # 4. Crear ciudad vinculada
        if pais.country_id:
            print("\n[CONTROLLER] -> Creando ciudad vinculada a país...")
            ciudad = CityEntity(city_id=None, city="Lisboa", country_id=pais.country_id)
            if self.repository.guardar_ciudad(ciudad):
                print(f"   Ciudad persistida: {ciudad}")

        # 5. Modificar película y sincronizar
        print("\n[CONTROLLER] -> Modificando estado de FilmEntity y sincronizando...")
        pelicula = self.repository.buscar_pelicula_por_id(id_pelicula=2)
        if pelicula:
            print(f"   Estado original: {pelicula}")
            pelicula.rental_rate = 8.99
            if self.repository.actualizar_tarifa_pelicula(pelicula):
                actualizada = self.repository.buscar_pelicula_por_id(2)
                print(f"   Estado sincronizado: {actualizada}")

        # 6. Eliminar entidad
        print("\n[CONTROLLER] -> Eliminando entidad via capa intermedia...")
        self.repository.eliminar_ciudad_por_id(id_ciudad=1)

        print("\n" + "=" * 70)
        print(" 🏁 ARQUITECTURA MODULAR COMPLETADA - FASE II VALIDADA")
        print("=" * 70)
