# =====================================================================
# MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
# CASO PRÁCTICO 2: CRUD/ORM NATIVO Y ESTRUCTURAS DE DATOS
# FASE II: ARQUITECTURA ORM POO, CONTEXTO DE DATOS Y CAPA DE CONTROL
# =====================================================================

import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Dict, Any

# =====================================================================
# COMPONENTE 2: ENTITY OBJECTS (Mapeo 1:1 de campos del DBMS) [1 PUNTO]
# =====================================================================

class CountryEntity:
    """Copia exacta de los campos de la tabla 'country' en el DBMS."""
    def __init__(self, country_id: Optional[int], country: str, last_update: Optional[str] = None):
        self.country_id: Optional[int] = country_id
        self.country: str = country
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<Entity.Country id={self.country_id} name='{self.country}'>"


class CityEntity:
    """Copia exacta de los campos de la tabla 'city' en el DBMS."""
    def __init__(self, city_id: Optional[int], city: str, country_id: int, last_update: Optional[str] = None):
        self.city_id: Optional[int] = city_id
        self.city: str = city
        self.country_id: int = country_id
        self.last_update: Optional[str] = last_update

    def __repr__(self) -> str:
        return f"<Entity.City id={self.city_id} name='{self.city}' fk_country={self.country_id}>"


class FilmEntity:
    """Copia exacta de los campos de la tabla 'film' en el DBMS."""
    def __init__(self, film_id: Optional[int], title: str, rental_rate: float, length: int, replacement_cost: float, release_year: Optional[int] = None):
        self.film_id: Optional[int] = film_id
        self.title: str = title
        self.rental_rate: float = float(rental_rate)
        self.length: int = length
        self.replacement_cost: float = float(replacement_cost)
        self.release_year: Optional[int] = release_year

    def __repr__(self) -> str:
        return f"<Entity.Film id={self.film_id} title='{self.title}' rate=${self.rental_rate}>"


# =====================================================================
# COMPONENTE 1: DBCONTEXT (Mapeador Relacional Nativo) [1 PUNTO]
# =====================================================================

class DbContext:
    """Gestiona el ciclo de vida de las conexiones y transacciones con MySQL."""
    def __init__(self):
        self.host: str = "localhost"
        self.port: int = 3306
        self.user: str = "root"
        self.password: str = "8095224147Gael"  # Tu clave maestra validada
        self.database: str = "sakila"

    def _conectar(self):
        """Método privado para instanciar la conexión cruda del Driver."""
        return mysql.connector.connect(
            host=self.host, port=self.port, user=self.user,
            password=self.password, database=self.database
        )

    def ejecutar_comando(self, query: str, params: tuple) -> Optional[int]:
        """Ejecuta operaciones de escritura (INSERT, UPDATE, DELETE) parametrizadas."""
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"  [DbContext Error] Restricción de Integridad activada: {e.msg}")
            return None
        finally:
            cursor.close()
            conn.close()

    def ejecutar_consulta(self, query: str, params: tuple = ()) -> List[tuple]:
        """Ejecuta operaciones de lectura relacional (SELECT)."""
        conn = self._conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"  [DbContext Error] Fallo en Query: {e.msg}")
            return []
        finally:
            cursor.close()
            conn.close()


# =====================================================================
# COMPONENTE 3: MODEL LAYER (Estructuras List<Entity>) [1 PUNTO]
# =====================================================================

class DataRepository:
    """Abstrae el DbContext transformando conjuntos relacionales en colecciones estructuradas."""
    def __init__(self, context: DbContext):
        self.context: DbContext = context

    # --- Persistencia de Objetos Puros ---
    def guardar_pais(self, entity: CountryEntity) -> bool:
        query = "INSERT INTO country (country) VALUES (%s)"
        last_id = self.context.ejecutar_comando(query, (entity.country,))
        if last_id is not None:
            entity.country_id = last_id
            return True
        return False

    def guardar_ciudad(self, entity: CityEntity) -> bool:
        query = "INSERT INTO city (city, country_id) VALUES (%s, %s)"
        last_id = self.context.ejecutar_comando(query, (entity.city, entity.country_id))
        if last_id is not None:
            entity.city_id = last_id
            return True
        return False

    def actualizar_tarifa_pelicula(self, entity: FilmEntity) -> bool:
        query = "UPDATE film SET rental_rate = %s WHERE film_id = %s"
        last_id = self.context.ejecutar_comando(query, (entity.rental_rate, entity.film_id))
        return last_id is not None

    def eliminar_ciudad_por_id(self, id_ciudad: int) -> bool:
        query = "DELETE FROM city WHERE city_id = %s"
        last_id = self.context.ejecutar_comando(query, (id_ciudad,))
        return last_id is not None

    # --- Hidratación de List<Entity> ---
    def listar_paises(self, limite: int) -> List[CountryEntity]:
        """Transforma filas relacionales en una estructura pura List<CountryEntity>."""
        query = "SELECT country_id, country, last_update FROM country ORDER BY country_id DESC LIMIT %s"
        filas = self.context.ejecutar_consulta(query, (limite,))
        
        # Estructura de datos requerida: List<Entity>
        lista_modelos: List[CountryEntity] = []
        for f in filas:
            lista_modelos.append(CountryEntity(country_id=f[0], country=f[1], last_update=str(f[2])))
        return lista_modelos

    def buscar_pelicula_por_id(self, id_pelicula: int) -> Optional[FilmEntity]:
        query = "SELECT film_id, title, rental_rate, length, replacement_cost, release_year FROM film WHERE film_id = %s"
        filas = self.context.ejecutar_consulta(query, (id_pelicula,))
        if filas:
            f = filas[0]
            return FilmEntity(film_id=f[0], title=f[1], rental_rate=f[2], length=f[3], replacement_cost=f[4], release_year=f[5])
        return None


# =====================================================================
# COMPONENTE 4: FRAMEWORK DE FLUJO (Capas del Patrón Controller) [2 PUNTOS]
# =====================================================================

class SakilaWorkflowController:
    """Controlador central que orquesta el flujo de negocio e interactúa con el cliente."""
    def __init__(self):
        self.context = DbContext()
        self.repository = DataRepository(self.context)

    def procesar_flujo_fase2(self) -> None:
        print("=====================================================================")
        print("      INICIANDO INGENIERÍA DE SOFTWARE DE LA FASE II: ORM POO        ")
        print("=====================================================================")
        
        # 1. Simulación e Inserción de Entidades de Negocio
        print("\n[CAPA CONTROLADOR] -> Inicializando Entidad de País en memoria...")
        pais_por_mapear = CountryEntity(country_id=None, country="Portugal")
        print(f"   Estado pre-persistencia: {pais_por_mapear}")
        
        # El controlador ordena guardar la Entidad pura
        if self.repository.guardar_pais(pais_por_mapear):
            print(f"   Estado post-persistencia en ORM (ID Generado): {pais_por_mapear}")
        
        # Forzar duplicado para evidenciar el Unique Constraint controlado por la arquitectura
        print("\n[CAPA CONTROLADOR] -> Forzando duplicado de País para auditar robustez de DbContext...")
        pais_duplicado = CountryEntity(country_id=None, country="Portugal")
        self.repository.guardar_pais(pais_duplicado)

        # 2. Rescate del flujo mapeado a Colecciones estructuradas List<Entity>
        print("\n[CAPA CONTROLADOR] -> Hidratando estructura List<Entity> desde el Repositorio...")
        coleccion_paises: List[CountryEntity] = self.repository.listar_paises(limite=3)
        print(f"   Tipo de Estructura de Datos Retornada: {type(coleccion_paises)}")
        for pais in coleccion_paises:
            print(f"     -> Objeto Mapeado: {pais} | Instancia de Clase: {type(pais).__name__}")

        # 3. Relación de Objetos dependientes (Ciudad -> País)
        print("\n[CAPA CONTROLADOR] -> Enlazando Entidades mediante llaves mapeadas en objetos...")
        if pais_por_mapear.country_id:
            ciudad_por_mapear = CityEntity(city_id=None, city="Lisboa", country_id=pais_por_mapear.country_id)
            self.repository.guardar_ciudad(ciudad_por_mapear)
            print(f"   Entidad Ciudad vinculada y persistida: {ciudad_por_mapear}")

        # 4. Modificación de Estado de Negocio (Película)
        print("\n[CAPA CONTROLADOR] -> Solicitando Entidad de Película por Identificador...")
        pelicula_business_obj = self.repository.buscar_pelicula_por_id(id_pelicula=2)
        if pelicula_business_obj:
            print(f"   Estado original recuperado por ORM: {pelicula_business_obj}")
            print("   Modificando propiedad 'rental_rate' a $8.99 dentro del objeto...")
            pelicula_business_obj.rental_rate = 8.99  # Cambio directo sobre el objeto en memoria
            
            # Sincronización del estado del objeto con la BD
            if self.repository.actualizar_tarifa_pelicula(pelicula_business_obj):
                print(f"   Sincronización Exitosa. Nuevo estado en BD: {self.repository.buscar_pelicula_por_id(2)}")

        # 5. Control Transaccional de Eliminación
        print("\n[CAPA CONTROLADOR] -> Solicitando remoción física mediante capa intermedia...")
        self.repository.eliminar_ciudad_por_id(id_ciudad=1)

        print("\n=====================================================================")
        print("      🏁 ARCHITECTURAL FLOW COMPLETADO - FASE II VALIDADA            ")
        print("=====================================================================")


# --- Punto de Entrada del Flujo de Software ---
if __name__ == "__main__":
    # Instanciamos el controlador empresarial para disparar el flujo operativo
    controlador = SakilaWorkflowController()
    controlador.procesar_flujo_fase2()