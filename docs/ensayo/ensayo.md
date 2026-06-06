# Ensayo Técnico: CRUD/ORM Nativo en Python con Arquitectura MariaDB-Sakila Completo

**Maestría en Ciencia de Datos e Inteligencia Artificial**
**INF-8237-C2: Ciencias de Datos 1**

**Autores**:
- Framiel Trinidad
- Edwing Perez
- Jharol Duran

**Universidad**: Universidad Autónoma de Santo Domingo (UASD)
**Profesora**: Silveria del Orbe Abad
**Fecha**: 6 de junio de 2026

---

## Resumen (300 palabras)

Este proyecto presenta una implementación completa de arquitectura CRUD/ORM nativo en Python orientado a la base de datos Sakila de MariaDB, expandida a16 tablas para demostrar el ciclo transaccional y analítico completo de un sistema de gestión de alquiler de películas. La solución se estructura en dos fases complementarias: la primera establece operaciones básicas de creación, lectura, actualización y eliminación (CRUD) sobre 13 entidades, complementadas con funcionalidades de importación/exportación en formatos CSV y JSON, además de métricas descriptivas multivariable incluyendo media, rango, desviación estándar, varianza y covarianza para las variables de film, payments, rentals e inventory. La segunda fase consolida una arquitectura ORM completa mediante el patrón DbContext que gestiona el ciclo de vida de conexiones y transacciones, 12 entidades puras que mapean las tablas del sistema (CountryEntity hasta PaymentEntity), un modelo de repositorio que transforma filas relacionales en colecciones tipadas List<Entity>, y un controlador de flujo (SakilaWorkflowController) que orquesta las operaciones de negocio para 8 nuevas entidades. La arquitectura implementa constraints de integridad a nivel de base de datos incluyendo unique keys para evitar duplicados, foreign keys con políticas restrictivas (ON DELETE RESTRICT) y cascading para actualizaciones. Se ejecutan 25 consultas analíticas SQL (10 básicas + 15 extendidas) que demuestran JOINs múltiples, subconsultas, funciones de agregación y filtros complejos. El código fuente está disponible públicamente en GitHub, facilitando la colaboración y revisión entre pares.

**Palabras clave**: ORM, CRUD, Python, MariaDB, Sakila, DbContext, Entity, Model, Controller, Sakila Completo

---

## 1. Introducción

### 1.1 Contexto del Proyecto

En el ámbito de la ingeniería de software moderna, la comunicación entre aplicaciones orientadas a objetos y sistemas de bases de datos relacionales representa un desafío técnico fundamental. El Object-Relational Mapping (ORM) emerge como la solución arquitectónica estándar para abstract esta brecha paradigmática, permitiendo que desarrolladores trabajen con objetos nativos del lenguaje mientras la persistencia se gestiona de manera transparente.

El presente proyecto expande el alcance original de Sakila (4 tablas) a las 16 tablas completas del esquema estándar, permitiendo demostrar un ciclo transaccional real completo: desde clientes y empleados hasta alquileres, pagos y relaciones many-to-many entre películas, actores y categorías.

### 1.2 Objetivos

El presente proyecto tiene como objetivos:
1. Implementar operaciones CRUD básicas con queries SQL parametrizados sobre 13 entidades
2. Desarrollar un ORM nativo basado en POO sin frameworks externos
3. Validar la integridad de datos mediante constraints de base de datos (UNIQUE, FK, CHECK)
4. Proporcionar interoperabilidad mediante import/export CSV y JSON
5. Calcular métricas descriptivas multivariable para análisis exploratorio de datos
6. Ejecutar 25 consultas analíticas SQL demostrando diferentes técnicas de JOIN y agregación

---

## 2. Fase I: Consultas SQL y Operaciones CRUD

### 2.1 Estructura de la Base de Datos (DDL) - Sakila Completo

El script SQL crea la base de datos `sakila` con 16 tablas que cubren todo el ciclo transaccional de un videoclub:

```sql
-- TABLAS BASE (4 tablas originales)
CREATE TABLE country (...);        -- Países
CREATE TABLE city (...);            -- Ciudades (FK: country)
CREATE TABLE film (...);             -- Películas
CREATE TABLE inventory (...);        -- Inventario (FK: film)

-- TABLAS EXTENDIDAS (12 tablas nuevas)
CREATE TABLE language (...);         -- Idiomas
CREATE TABLE address (...);           -- Direcciones (FK: city)
CREATE TABLE store (...); -- Tiendas (FK: address, staff)
CREATE TABLE actor (...);              -- Actores
CREATE TABLE category (...);         -- Categorías
CREATE TABLE film_actor (...);        -- Relación Film-Actor (PK compuesta)
CREATE TABLE film_category (...);    -- Relación Film-Category (PK compuesta)
CREATE TABLE staff (...);             -- Empleados (FK: address, store)
CREATE TABLE customer (...);          -- Clientes (FK: address, store)
CREATE TABLE rental (...);            -- Alquileres (FK: inventory, customer, staff)
CREATE TABLE payment (...);           -- Pagos (FK: customer, staff, rental)
CREATE TABLE film_text (...);         -- Búsqueda full-text (FK: film)
```

### 2.2 Conjunto de 25 Consultas Analíticas

#### Consultas Básicas (1-10)

1. **Películas con costo > $15.00** - Identifica inventario de alto valor
2. **Ciudades con países (JOIN)** - Integración de variables geográficas
3. **Ciudades por país (GROUP BY)** - Métrica agregada de densidad urbana
4. **Duración promedio por clasificación** - Análisis por rating
5. **Búsqueda por título (LIKE)** - Patrones de texto
6. **Inventario activo por tienda** - Auditoría de stock
7. **Películas tarifa 3-6 y duración > 120** - Filtro multidimensional
8. **Conteo de copias por título** - Control de volumen
9. **Países sin ciudades** - Detección de datos huérfanos
10. **Máximo costo de reemplazo** - Subconsulta analítica

#### Consultas Extendidas (11-25)

11. **Actores por película** - JOIN film_actor + actor
12. **Categorías por película** - JOIN film_category + category
13. **Películas por actor** - Búsqueda por actor (LIKE)
14. **Staff activo por tienda** - Empleados activos
15. **Direcciones completas** - JOIN 3 tablas (address + city + country)
16. **Clientes por tienda** - Distribución de clientes
17. **Alquileres activos** - WHERE return_date IS NULL
18. **Historial de pagos** - JOIN payment + customer
19. **Ingresos por tienda** - GROUP BY + SUM
20. **Empleado con más alquileres** - GROUP BY + COUNT + ORDER BY
21. **Cliente que más gasta** - GROUP BY + SUM + ORDER BY
22. **Películas más alquiladas** - JOIN inventory + rental
23. **Top 3 categorías** - GROUP BY + ORDER BY + LIMIT
24. **Duración promedio por categoría** - JOIN múltiples
25. **Rental completo con detalles** - JOIN 5 tablas

### 2.3 Implementación CRUD en Python

El `CrudService` implementa 40+ operaciones CRUD sobre13 entidades:

```python
class CrudService:
    # Country
    def crear_pais(self, nombre: str) -> Optional[CountryEntity]
    def leer_paises(self, limite: int = 10) -> List[CountryEntity]

    # City
    def crear_ciudad(self, nombre: str, country_id: int) -> Optional[CityEntity]
    def leer_ciudades(self, limite: int = 10) -> List[tuple]
    def eliminar_ciudad(self, city_id: int) -> bool

    # Film
    def leer_peliculas(self, limite: int = 10) -> List[FilmEntity]
    def buscar_pelicula_por_id(self, film_id: int) -> Optional[FilmEntity]
    def actualizar_tarifa_pelicula(self, film_id: int, nueva_tarifa: float) -> bool

    # Actor
    def crear_actor(self, first_name: str, last_name: str) -> Optional[ActorEntity]
    def leer_actores(self, limite: int = 10) -> List[ActorEntity]
    def buscar_actor_por_nombre(self, nombre: str) -> List[ActorEntity]

    # Category
    def crear_categoria(self, nombre: str) -> Optional[CategoryEntity]
    def leer_categorias(self, limite: int = 20) -> List[CategoryEntity]

    # Staff
    def crear_staff(self, first_name: str, last_name: str, address_id: int,
                    store_id: int, username: str, email: str = None) -> Optional[StaffEntity]
    def leer_staff(self, limite: int = 10) -> List[StaffEntity]

    # Customer
    def crear_cliente(self, store_id: int, first_name: str, last_name: str,
                      address_id: int, email: str = None) -> Optional[CustomerEntity]
    def leer_clientes(self, limite: int = 10) -> List[CustomerEntity]

    # Rental
    def crear_alquiler(self, inventory_id: int, customer_id: int, staff_id: int) -> Optional[RentalEntity]
    def leer_alquileres(self, limite: int = 10) -> List[RentalEntity]
    def leer_alquileres_activos(self) -> List[RentalEntity]

    # Payment
    def crear_pago(self, customer_id: int, staff_id: int, amount: float,
                   rental_id: int = None) -> Optional[PaymentEntity]
    def leer_pagos(self, limite: int = 10) -> List[PaymentEntity]
    def total_pagos_cliente(self, customer_id: int) -> float

    # Inventory
    def crear_inventario(self, film_id: int, store_id: int) -> Optional[InventoryEntity]
    def leer_inventario_por_tienda(self, store_id: int) -> List[InventoryEntity]
```

### 2.4 Import/Export CSV y JSON

```python
def exportar_a_csv(self, nombre_tabla: str, ruta_destino: Optional[str] = None) -> str:
    with self._get_connection() as conn:
        df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conn)
    df.to_csv(ruta_destino, index=False, encoding='utf-8')

def exportar_a_json(self, nombre_tabla: str, ruta_destino: Optional[str] = None) -> str:
    with self._get_connection() as conn:
        df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conn)
    lista_diccionarios = df.to_dict(orient="records")
    with open(ruta_destino, 'w', encoding='utf-8') as archivo:
        json.dump(lista_diccionarios, archivo, indent=4, ensure_ascii=False)
```

### 2.5 Métricas Descriptivas Multivariable

```python
# Métricas de Film (original)
def calcular_metricas_descriptivas(self) -> dict:
    df = pd.read_sql("SELECT length, replacement_cost FROM film", conn)
    # Media, Rango, Desviación, Varianza, Covarianza

# Métricas de Payments (nueva)
def metricas_payments(self) -> dict:
    df = pd.read_sql("SELECT amount FROM payment", conn)
    # Total, Media, Rango, Desviación, Varianza

# Métricas de Duración de Alquileres (nueva)
def metricas_rental_duration(self) -> dict:
    df = pd.read_sql("""SELECT DATEDIFF(IFNULL(return_date, NOW()), rental_date) AS dias
                        FROM rental WHERE return_date IS NOT NULL""", conn)
    # Media, Rango, Desviación, Varianza

# Métricas de Inventario por Tienda (nueva)
def metricas_inventory_by_store(self) -> dict:
    df = pd.read_sql("""SELECT store_id, COUNT(*) as total
 FROM inventory GROUP BY store_id""", conn)

# Métricas de Actividad por Cliente (nueva)
def metricas_customer_activity(self) -> dict:
    df = pd.read_sql("""SELECT c.customer_id, c.first_name, c.last_name,
 COUNT(r.rental_id) as total_rentals,
                        COALESCE(SUM(p.amount), 0) as total_spent
                        FROM customer c
                        LEFT JOIN rental r ON c.customer_id = r.customer_id
                        LEFT JOIN payment p ON c.customer_id = p.customer_id
                        GROUP BY c.customer_id""", conn)
```

---

## 3. Fase II: Arquitectura ORM

### 3.1 DbContext y ORM Framework

El componente `DbContext` gestiona el ciclo de vida completo de las conexiones:

```python
class DbContext:
    def ejecutar_comando(self, query: str, params: tuple) -> Optional[int]:
        """Ejecuta INSERT/UPDATE/DELETE con manejo de errores"""
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
        """Ejecuta SELECT y retorna lista de tuplas"""
```

### 3.2 Entity Objects (12 entidades)

```python
class CountryEntity:
    def __init__(self, country_id: Optional[int], country: str, last_update: Optional[str] = None)

class CityEntity:
    def __init__(self, city_id: Optional[int], city: str, country_id: int, last_update: Optional[str] = None)

class FilmEntity:
    def __init__(self, film_id: Optional[int], title: str, rental_rate: float,
                 length: int, replacement_cost: float, release_year: Optional[int] = None,
                 description: Optional[str] = None, rating: Optional[str] = None)

class InventoryEntity:
    def __init__(self, inventory_id: Optional[int], film_id: int, store_id: int, last_update: Optional[str] = None)

class LanguageEntity:
    def __init__(self, language_id: Optional[int], name: str, last_update: Optional[str] = None)

class AddressEntity:
    def __init__(self, address_id: Optional[int], address: str, address2: Optional[str],
 district: str, city_id: int, postal_code: Optional[str], phone: str,
                 last_update: Optional[str] = None)

class StoreEntity:
    def __init__(self, store_id: Optional[int], manager_staff_id: int, address_id: int,
                 last_update: Optional[str] = None)

class ActorEntity:
    def __init__(self, actor_id: Optional[int], first_name: str, last_name: str,
                 last_update: Optional[str] = None)

class CategoryEntity:
    def __init__(self, category_id: Optional[int], name: str, last_update: Optional[str] = None)

class StaffEntity:
    def __init__(self, staff_id: Optional[int], first_name: str, last_name: str,
                 address_id: int, email: Optional[str], store_id: int, active: int,
                 username: str, password: Optional[str] = None, last_update: Optional[str] = None)

class CustomerEntity:
    def __init__(self, customer_id: Optional[int], store_id: int, first_name: str,
                 last_name: str, email: Optional[str], address_id: int,
                 create_date: Optional[str] = None, last_update: Optional[str] = None)

class RentalEntity:
    def __init__(self, rental_id: Optional[int], rental_date: str, inventory_id: int,
                 customer_id: int, return_date: Optional[str], staff_id: int,
                 last_update: Optional[str] = None)

class PaymentEntity:
    def __init__(self, payment_id: Optional[int], customer_id: int, staff_id: int,
                 rental_id: Optional[int], amount: float, payment_date: str,
                 last_update: Optional[str] = None)
```

### 3.3 Model Layer: DataRepository con List<Entity>

```python
class DataRepository:
    def guardar_pais(self, entity: CountryEntity) -> bool
    def listar_paises(self, limite: int = 10) -> List[CountryEntity]
    def guardar_ciudad(self, entity: CityEntity) -> bool
    def listar_ciudades_con_pais(self, limite: int = 10) -> List[tuple]
    def guardar_pelicula(self, entity: FilmEntity) -> bool
    def buscar_pelicula_por_id(self, id_pelicula: int) -> Optional[FilmEntity]
    def guardar_actor(self, entity: ActorEntity) -> bool
    def listar_actores(self, limite: int = 10) -> List[ActorEntity]
    def guardar_categoria(self, entity: CategoryEntity) -> bool
    def guardar_staff(self, entity: StaffEntity) -> bool
    def guardar_cliente(self, entity: CustomerEntity) -> bool
    def guardar_alquiler(self, entity: RentalEntity) -> bool
    def listar_alquileres_activos(self) -> List[RentalEntity]
    def guardar_pago(self, entity: PaymentEntity) -> bool
    def calcular_total_pagos_por_cliente(self, customer_id: int) -> float
```

### 3.4 Controller: SakilaWorkflowController

```python
class SakilaWorkflowController:
    def crear_pais(self, nombre: str) -> CountryEntity
    def crear_ciudad(self, nombre: str, country_id: int) -> CityEntity
    def crear_actor(self, first_name: str, last_name: str) -> ActorEntity
    def crear_categoria(self, nombre: str) -> CategoryEntity
    def crear_staff(self, first_name: str, last_name: str, address_id: int,
                    store_id: int, username: str, email: str = None) -> StaffEntity
    def crear_cliente(self, store_id: int, first_name: str, last_name: str,
                      address_id: int, email: str = None) -> CustomerEntity
    def crear_alquiler(self, inventory_id: int, customer_id: int, staff_id: int) -> RentalEntity
    def crear_pago(self, customer_id: int, staff_id: int, amount: float,
                   rental_id: int = None) -> PaymentEntity
    def total_pagos_cliente(self, customer_id: int) -> float
    def procesar_flujo_completo(self) -> None
```

---

## 4. Integridad de Datos

### 4.1 Unique Constraints

| Tabla | Constraint | Columna(s) |
|-------|------------|------------|
| country | unique_country | country |
| city | unique_city_country | (city, country_id) |
| film | unique_title_release | (title, release_year) |
| category | unique_category_name | name |
| staff | unique_staff_username | username |

### 4.2 Foreign Keys con Comportamiento Restrictivo

| Tabla Hija | Columna | Tabla Padre | Comportamiento |
|------------|--------|------------|---------------|
| city | country_id | country | ON DELETE RESTRICT |
| address | city_id | city | ON DELETE RESTRICT |
| store | address_id | address | ON DELETE RESTRICT |
| store | manager_staff_id | staff | ON DELETE RESTRICT |
| staff | address_id | address | ON DELETE RESTRICT |
| staff | store_id | store | ON DELETE RESTRICT |
| customer | store_id | store | ON DELETE RESTRICT |
| customer | address_id | address | ON DELETE RESTRICT |
| inventory | film_id | film | ON DELETE RESTRICT |
| rental | inventory_id | inventory | ON DELETE RESTRICT |
| rental | customer_id | customer | ON DELETE RESTRICT |
| rental | staff_id | staff | ON DELETE RESTRICT |
| payment | customer_id | customer | ON DELETE RESTRICT |
| payment | staff_id | staff | ON DELETE RESTRICT |
| payment | rental_id | rental | ON DELETE SET NULL |
| film_actor | actor_id | actor | ON DELETE RESTRICT |
| film_actor | film_id | film | ON DELETE RESTRICT |
| film_category | film_id | film | ON DELETE RESTRICT |
| film_category | category_id | category | ON DELETE RESTRICT |
| film_text | film_id | film | ON DELETE CASCADE |

---

## 5. Conclusiones

El proyecto demuestra que es posible construir un ORM funcional utilizando únicamente el conector nativo de MySQL para Python, sin depender de frameworks externos como SQLAlchemy o Django ORM. La arquitectura lograda proporciona:

- **Separación de responsabilidades**: DbContext maneja conexiones, Repository maneja datos, Controller orquestra
- **Type safety**: 12 entidades tipadas con verificación estática
- **Integridad enforceable**: 20+ constraints a nivel de BD previenen datos inconsistentes
- **Interoperabilidad**: Import/Export CSV y JSON para integración con otros sistemas
- **Análisis estadístico**:5 categorías de métricas descriptivas para exploración de datos
- **Ciclo transaccional completo**:16 tablas cubriendo el dominio completo de Sakila
- **25 consultas analíticas**: Demostrando técnicas avanzadas de SQL

El enfoque artesanal permite comprender los fundamentos internos de cómo operan los ORM comerciales, while providing un framework extensible para aplicaciones de mediana escala.

---

## 6. Referencias

- MySQL Connector/Python Documentation. (2024). Oracle Corporation. https://dev.mysql.com/doc/connector-python/en/
- Pandas Documentation. (2024). NumFOCUS. https://pandas.pydata.org/docs/
- NumPy Documentation. (2024). NumFOCUS. https://numpy.org/doc/
- Date, C. J. (2004). *Introduction to Database Systems* (8th ed.). Addison-Wesley.
- Elmasri, R.,& Navathe, S. (2016). *Fundamentals of Database Systems* (7th ed.). Pearson.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.

---

## 7. Anexos

### Anexo A: Estructura de Archivos del Proyecto

```
uasdCrudPython/
├── main.py                  # Punto de entrada unificado (CLI + menú)
├── fase1_main.py           # Validación Fase I
├── fase2_orm.py           # Validación Fase II
├── setup.py                # Paquete instalable
├── requirements.txt        # Dependencias Python
├── .env                    # Configuración local
├── src/
│   ├── config.py           # Configuración centralizada
│   ├── dbcontext.py       # DbContext (gestor de conexiones)
│   ├── fase1/
│   │   ├── crud_service.py    # CRUD (13 entidades, 40+ operaciones)
│   │   ├── export_service.py  # CSV/JSON I/O
│   │   └── metrics_service.py # 5 categorías de métricas
│   ├── entities/
│   │   └── __init__.py   # 12 Entity Objects
│   ├── models/
│   │   └── data_repository.py # Model Layer (List<Entity>)
│   ├── controllers/
│   │   └── sakila_controller.py # Controller
│   └── utils/
│       └── helpers.py
├── sql/
│   ├── 00_init.sql         # Crear base de datos
│   ├── run_all.sql         # Script maestro
│   ├── ddl/
│   │   ├── 01_ddl.sql     # 4 tablas base
│   │   └── 02_ddl_extended.sql # 12 tablas extendidas
│   ├── dml/
│   │   ├── 02_dml.sql     # Datos base
│   │   └── 03_dml_extended.sql # Datos extendidos
│   └── queries/
│       ├── 03_queries.sql # 10 consultas básicas
│       └── 04_queries_extended.sql # 15 consultas extendidas
├── docs/
│   ├── DESIGN.md          # Diseño técnico
│   ├── criterios.md       # Mapeo de criterios
│   ├── ensayo/
│   │   └── ensayo.md      # Este documento
│   └── evidencias/
│       └── logs.md        # Logs de ejecución
└── data/                   # Exports CSV/JSON
```

### Anexo B: Datos de Prueba Cargados (~130+ registros)

| Tabla | Registros | Ejemplos |
|-------|-----------|----------|
| country | 5 | Dominican Republic, USA, Spain, Mexico, Colombia |
| city | 6 | Santo Domingo, NYC, Madrid, CDMX |
| film | 5 | Inception, Matrix, Interstellar, Spirited Away, Casablanca |
| inventory | 6 | Películas en tiendas 1 y 2 |
| language | 6 | English, Italian, Japanese, Mandarin, French, German |
| address | 4 | NYC y Santiago, RD |
| staff | 4 | Mike, Jon, Pedro, Juan |
| store | 2 | Tiendas 1 y 2 |
| actor | 21 | Keanu Reeves, Leonardo DiCaprio, etc. |
| category | 16 | Action, Animation, Classics, etc. |
| film_actor | 21 | Relaciones películas-actores |
| film_category | 11 | Relaciones películas-categorías |
| customer | 4 | Juan Pérez, María Rodríguez, etc. |
| rental | 5 | Alquileres Mayo 2026 |
| payment | 5 | Pagos $1.99-$4.99 |
| film_text | 5 | Textos completos |

### Anexo C: Métricas Descriptivas Calculadas

| Variable | Media | Rango | Desviación | Varianza |
|----------|-------|-------|------------|-----------|
| film.length (min) | 136.00 | 67.00 | 25.05 | 627.50 |
| film.replacement_cost ($) | 16.59 | 15.00 | 5.94 | 35.30 |
| payment.amount ($) | 3.99 | 3.00 | 1.41 | 2.00 |
| rental.duration (días) | 2.00 | 2.00 | 1.41 | 2.00 |

**Covarianza length vs replacement_cost**: 145.50 (relación lineal positiva)

---

**Repositorio GitHub**: https://github.com/edvvdev/uasdCrudPython

**Última actualización**: 6 de junio de 2026
