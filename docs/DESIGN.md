# uasdCrudPython - Diseño Técnico

## Objetivos

- Implementar CRUD completo en Python para las 16 tablas de Sakila
- Demostrar arquitectura ORM nativa con DbContext, Entity, Model y Controller
- Validar integridad de datos con unique constraints y foreign keys
- Proporcionar import/export CSV y JSON para interoperabilidad
- Calcular métricas descriptivas multivariable (media, rango, desviación, varianza, covarianza)
- Ejecutar 25 consultas analíticas SQL (básicas y extendidas)

## No Objetivos

- No es un ORM completo tipo Django o SQLAlchemy
- No incluye migraciones de base de datos
- No implementa autenticación o autorización
- No proporciona API REST (solo ejecución local)

## Arquitectura

### Estructura del Proyecto

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
│   │   ├── crud_service.py    # CRUD operations (13 entidades)
│   │   ├── export_service.py  # CSV/JSON I/O
│   │   └── metrics_service.py # Métricas descriptivas (5 categorías)
│   ├── entities/
│   │   └── __init__.py   # 12 Entity Objects
│   ├── models/
│   │   └── data_repository.py # Model Layer (List<Entity>)
│   ├── controllers/
│   │   └── sakila_controller.py # Controller (Flujo de negocio)
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
│   ├── DESIGN.md
│   ├── criterios.md
│   ├── ensayo/
│   └── evidencias/
└── data/                   # Exports CSV/JSON
```

### Capas del Sistema

```
┌─────────────────────────────────────────────┐
│           main.py / fase1_main.py           │
│      (Orchestrator + CLI + Menú)           │
├─────────────────────────────────────────────┤
│           SakilaWorkflowController           │
│      (Orquesta flujo de negocio)            │
├─────────────────────────────────────────────┤
│           DataRepository                     │
│    (List<Entity> - Abstracción de datos)   │
├─────────────────────────────────────────────┤
│             DbContext                       │
│    (Gestión de conexiones y transacciones) │
├─────────────────────────────────────────────┤
│    mysql-connector-python / SQLAlchemy      │
│        (Driver + Pandas adapter)            │
├─────────────────────────────────────────────┤
│              MariaDB                         │
│           (Sakila - 16 tablas)              │
└─────────────────────────────────────────────┘
```

### Componentes Core

| Componente | Responsabilidad |
|------------|-----------------|
| `main.py` | Entry point con CLI y menú interactivo |
| `fase1_main.py` | Validación completa Fase I |
| `fase2_orm.py` | Validación completa Fase II ORM |
| `config.py` | Configuración centralizada de BD |
| `DbContext` | Crear/destruir conexiones, queries parametrizadas |
| `CrudService` | CRUD para 13 entidades (40+ operaciones) |
| `ExportService` | Import/Export CSV y JSON |
| `MetricsService` | 5 categorías de métricas descriptivas |
| `DataRepository` | Transformar filas SQL en List<Entity> |
| `SakilaWorkflowController` | Orquestar operaciones de negocio |

## Diseño de Datos - Sakila Completo (16 tablas)

### Esquema de Tablas

```sql
-- TABLAS BASE (DDL original)
country (country_id PK, country UNIQUE, last_update)
city (city_id PK, city, country_id FK→country, last_update, UNIQUE(city, country_id))
film (film_id PK, title, description, release_year, rental_duration, rental_rate, length, replacement_cost, rating, last_update, UNIQUE(title, release_year))
inventory (inventory_id PK, film_id FK→film, store_id, last_update)

-- TABLAS EXTENDIDAS (DDL nuevo)
language (language_id PK, name, last_update)
address (address_id PK, address, address2, district, city_id FK→city, postal_code, phone, last_update)
store (store_id PK, manager_staff_id FK→staff, address_id FK→address, last_update)
actor (actor_id PK, first_name, last_name, last_update, KEY idx_actor_name)
category (category_id PK, name UNIQUE, last_update)
film_actor (actor_id FK→actor, film_id FK→film, last_update, PK(actor_id, film_id))
film_category (film_id FK→film, category_id FK→category, last_update, PK(film_id, category_id))
staff (staff_id PK, first_name, last_name, address_id FK→address, email, store_id FK→store, active, username UNIQUE, password, last_update)
customer (customer_id PK, store_id FK→store, first_name, last_name, email, address_id FK→address, create_date, last_update)
rental (rental_id PK, rental_date, inventory_id FK→inventory, customer_id FK→customer, return_date, staff_id FK→staff, last_update, KEY idx_rental_date, KEY idx_rental_inventory_customer)
payment (payment_id PK, customer_id FK→customer, staff_id FK→staff, rental_id FK→rental, amount, payment_date, last_update)
film_text (film_id PK FK→film, title, description)
```

### Integridad Referencial

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

### Unique Constraints

| Tabla | Constraint | Columna(s) |
|-------|------------|------------|
| country | unique_country | country |
| city | unique_city_country | (city, country_id) |
| film | unique_title_release | (title, release_year) |
| category | unique_category_name | name |
| staff | unique_staff_username | username |

## Entity Objects (12 entidades)

| Entity | Tabla | Atributos Principales |
|--------|-------|---------------------|
| CountryEntity | country | country_id, country |
| CityEntity | city | city_id, city, country_id |
| FilmEntity | film | film_id, title, rental_rate, length, replacement_cost, rating |
| InventoryEntity | inventory | inventory_id, film_id, store_id |
| LanguageEntity | language | language_id, name |
| AddressEntity | address | address_id, address, district, city_id, phone |
| StoreEntity | store | store_id, manager_staff_id, address_id |
| ActorEntity | actor | actor_id, first_name, last_name |
| CategoryEntity | category | category_id, name |
| StaffEntity | staff | staff_id, first_name, last_name, username, store_id |
| CustomerEntity | customer | customer_id, first_name, last_name, store_id |
| RentalEntity | rental | rental_id, rental_date, inventory_id, customer_id, return_date |
| PaymentEntity | payment | payment_id, customer_id, amount, payment_date |

## Decisiones Técnicas

| Fecha | Decisión | Razón | Impacto |
|-------|-----------|-------|---------|
| 2026-06-05 | MySQL Connector nativo | Sin dependencias ORM externas, control total de SQL | Mayor curva de aprendizaje |
| 2026-06-05 | Unique constraints en BD | Integridad enforceada en origen | Errores controlados por arquitectura |
| 2026-06-05 | List<Entity> como modelo | Colecciones tipadas para interoperabilidad Python | Memoria adicional pero type-safe |
| 2026-06-06 | Config centralizada (.env) | Separar configuración de código | Facilita despliegue |
| 2026-06-06 | Paquete instalable (pip install -e .) | Facilita imports y distribución | Más profesional |
| 2026-06-06 | SQLAlchemy para Pandas | Elimina warnings de deprecated connection | Compatibilidad pandas |
| 2026-06-06 | Sakila Completo (16 tablas) | Demostrar ciclo transaccional completo | Scope académico expandido |

### Stack Tecnológico

- **Lenguaje**: Python 3.8+
- **Base de Datos**: MariaDB con Sakila (16 tablas)
- **Driver**: mysql-connector-python (conector nativo)
- **Pandas Adapter**: SQLAlchemy (para read_sql sin warnings)
- **Análisis**: pandas, numpy (métricas descriptivas)
- **Config**: python-dotenv (gestión de credenciales)
- **Estructuras**: typing.List para genericidad

## Métricas Descriptivas Implementadas

| Variable | Descripción | Métricas |
|----------|-------------|----------|
| film.length | Duración películas (minutos) | Media, Rango, Std, Varianza |
| film.replacement_cost | Costo reemplazo ($) | Media, Rango, Std, Varianza |
| film.length vs replacement_cost | Covarianza | Matriz covarianza (ddof=1) |
| payment.amount | Monto pagos ($) | Total, Media, Rango, Std, Varianza |
| rental.duration | Días de alquiler | Media, Rango, Std, Varianza |
| inventory.by_store | Unidades por tienda | Conteo |
| customer.activity | Alquileres y gastos | Totales y medias |

## Consultas SQL (25 total)

### Básicas (1-10)
1. Películas con costo > $15.00
2. Ciudades con países (JOIN)
3. Ciudades por país (GROUP BY)
4. Duración promedio por clasificación
5. Búsqueda por título (LIKE)
6. Inventario activo por tienda
7. Películas con tarifa 3-6 y duración > 120
8. Conteo de copias por título
9. Países sin ciudades
10. Máximo costo de reemplazo (subconsulta)

### Extendidas (11-25)
11. Actores por película (JOIN múltiple)
12. Categorías por película
13. Películas por actor
14. Staff activo por tienda
15. Direcciones completas (JOIN 3 tablas)
16. Clientes por tienda
17. Alquileres activos (WHERE NULL)
18. Historial de pagos por cliente
19. Ingresos por tienda (GROUP BY + SUM)
20. Empleado con más alquileres
21. Cliente que más gasta
22. Películas más alquiladas
23. Top 3 categorías populares
24. Duración promedio por categoría
25. Rental completo con detalles (JOIN 5 tablas)

## Limitaciones Conocidas

- Sin connection pooling
- Sin transacción distribuida
- Solo soporta un cliente a la vez
- Film text sin CRUD en Python (solo DDL/DML)

## Ejecución

```bash
# Instalar como paquete
pip install -e .

# Menú interactivo
python main.py

# CLI flags
python main.py --fase1
python main.py --fase2
python main.py --queries
python main.py --all

# Scripts de validación
python fase1_main.py    # Fase I completa
python fase2_orm.py     # Fase II ORM completa

# Base de datos
mysql -u root < sql/run_all.sql
```

## Historial de Cambios

### 2026-06-06 - v3.0 (Sakila Completo)

**Cambios**:
- Expansión a16 tablas Sakila completo
- 12 Entity Objects (CountryEntity hasta PaymentEntity)
- CRUD completo en CrudService (40+ operaciones)
- Controller expandido con 8 nuevas entidades
- Métricas extendidas (payments, rentals, inventory, customer)
- 25 consultas SQL (10 básicas + 15 extendidas)
- Submenús interactivos para Actor, Category, Staff, Customer, Rental, Payment
- Evidencias actualizadas con logs completos

**Razón**: Demostrar ciclo transaccional y analítico completo en un DBMS relacional

### 2026-06-06 - v2.0

**Cambios**:
- Reestructuración modular (services por responsabilidad)
- Punto de entrada unificado (main.py con CLI)
- Configuración centralizada (config.py + .env)
- Paquete instalable (setup.py + pip install -e .)

**Razón**: Mejores prácticas de ingeniería de software
