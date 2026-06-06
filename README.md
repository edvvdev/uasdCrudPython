# uasdCrudPython

> Proyecto académico - Maestría en Ciencia de Datos e Inteligencia Artificial
> Implementación CRUD/ORM nativo en Python con MariaDB (Sakila Completo - 16 tablas)

## Estructura del Proyecto

```
uasdCrudPython/
├── main.py                  # Punto de entrada unificado (CLI + menú)
├── fase1_main.py           # Validación Fase I (CRUD + Export + Métricas)
├── fase2_orm.py            # Validación Fase II (Arquitectura ORM)
├── setup.py                # Paquete instalable
├── requirements.txt        # Dependencias Python
├── .env                    # Configuración local (no commitear)
├── .env.example            # Template de configuración
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuración centralizada
│   ├── dbcontext.py       # Gestor de conexiones (Capa Persistencia)
│   ├── fase1/
│   │   ├── __init__.py
│   │   ├── crud_service.py    # CRUD operations (13 entidades)
│   │   ├── export_service.py  # CSV/JSON I/O
│   │   └── metrics_service.py # Métricas descriptivas (film, payments, rentals)
│   ├── entities/
│   │   └── __init__.py # Entity Objects (12 entidades)
│   ├── models/
│   │   └── data_repository.py # Model Layer (List<Entity>)
│   ├── controllers/
│   │   └── sakila_controller.py # Controller (Flujo de negocio)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── sql/
│   ├── 00_init.sql         # Crear base de datos
│   ├── run_all.sql         # Script maestro
│   ├── ddl/
│   │   ├── 01_ddl.sql # DDL tablas base (country, city, film, inventory)
│   │   └── 02_ddl_extended.sql # DDL tablas extendidas (12 tablas más)
│   ├── dml/
│   │   ├── 02_dml.sql     # Datos base
│   │   └── 03_dml_extended.sql # Datos extendidos
│   └── queries/
│       ├── 03_queries.sql # 10 consultas básicas
│       └── 04_queries_extended.sql # 15 consultas extendidas
├── docs/
│   ├── README.md
│   ├── DESIGN.md
│   ├── criterios.md
│   ├── ensayo/
│   └── evidencias/
└── data/                   # Exports CSV/JSON
```

## Base de Datos Sakila Completo (16 tablas)

| Tabla | Descripción |
|-------|-------------|
| country | Países |
| city | Ciudades (FK: country) |
| address | Direcciones (FK: city) |
| store | Tiendas (FK: address, staff) |
| staff | Empleados (FK: address, store) |
| customer | Clientes (FK: address, store) |
| film | Películas |
| film_actor | Relación Film-Actor (PK compuesta) |
| film_category | Relación Film-Category (PK compuesta) |
| film_text | Búsqueda full-text (FK: film) |
| language | Idiomas |
| category | Categorías |
| inventory | Inventario (FK: film, store) |
| rental | Alquileres (FK: inventory, customer, staff) |
| payment | Pagos (FK: customer, staff, rental) |

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/edvvdev/uasdCrudPython.git
cd uasdCrudPython

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Instalar como paquete (desarrollo)
pip install -e .
```

## Uso

### Ejecución

```bash
# Menú interactivo
python main.py

# CLI flags
python main.py --fase1      # Ejecutar Fase I
python main.py --fase2      # Ejecutar Fase II
python main.py --queries    # Mostrar consultas SQL (25 queries)
python main.py --all        # Ejecutar todas las fases

# Scripts de validación independientes
python fase1_main.py        # Validación Fase I completa
python fase2_orm.py         # Validación Fase II ORM completa
```

### Menú Interactivo

```
$ python main.py

======================================================================
        MENÚ PRINCIPAL - uasdCrudPython
  Maestría en Ciencia de Datos e Inteligencia Artificial
======================================================================

 1. FASE I: CRUD + Import/Export + Métricas
 2. FASE II: Arquitectura ORM (con submenús)
 3. CONSULTAS SQL (25 queries)
 4. DOCUMENTACIÓN
 0. Salir

Seleccione una opción:
```

## Arquitectura ORM (Fase II)

| Componente | Descripción |
|------------|-------------|
| **DbContext** | Gestor de conexiones y transacciones |
| **Entity Objects** | CountryEntity, CityEntity, FilmEntity, ActorEntity, CategoryEntity, StaffEntity, CustomerEntity, RentalEntity, PaymentEntity, InventoryEntity, LanguageEntity, AddressEntity, StoreEntity |
| **Model Layer** | DataRepository con List<Entity> |
| **Controller** | SakilaWorkflowController |

## Métricas Descriptivas Implementadas

| Variable | Métricas |
|----------|----------|
| film.length | Media, Rango, Desviación, Varianza, Covarianza |
| film.replacement_cost | Media, Rango, Desviación, Varianza |
| payment.amount | Total, Media, Rango, Desviación, Varianza |
| rental.duration | Media, Rango, Desviación, Varianza |
| inventory.by_store | Conteo por tienda |
| customer.activity | Alquileres y gastos por cliente |

## Consultas SQL (25 total)

### Básicas (1-10)
1. Películas con costo > $15.00
2. Ciudades con países (JOIN)
3. Ciudades por país (conteo)
4. Duración promedio por clasificación
5. Búsqueda por título (Matrix/Inception)
6. Inventario activo Tienda 1
7. Películas tarifa 3-6 y duración > 120
8. Conteo de copias por título
9. Países sin ciudades
10. Máximo costo de reemplazo

### Extendidas (11-25)
11. Actores por película
12. Categorías por película
13. Películas por actor
14. Staff activo por tienda
15. Direcciones completas
16. Clientes por tienda
17. Alquileres activos
18. Historial de pagos
19. Ingresos por tienda
20. Empleado con más alquileres
21. Cliente que más gasta
22. Películas más alquiladas
23. Top 3 categorías
24. Duración promedio por categoría
25. Rental completo con detalles

## Criterios de Evaluación

| # | Criterio | Puntos | Estado |
|---|----------|--------|--------|
| 1 | FASE I: Queries SQL + Python | 8 | ✅ |
| 2 | DbContext + ORM framework | 3 | ✅ |
| 3 | Entity | 3 | ✅ |
| 4 | Model (list<entity>) | 3 | ✅ |
| 5 | Controller | 3 | ✅ |
| 6 | Sakila Completo (16 tablas) | + | ✅ |
| 7 | Video explicativo (opcional) | 3 | ❌ |

## Base de Datos

```bash
# Importar estructura y datos completos
mysql -u root < sql/run_all.sql

# O ejecutar scripts individualmente
mysql -u root < sql/00_init.sql
mysql -u root < sql/ddl/01_ddl.sql
mysql -u root < sql/ddl/02_ddl_extended.sql
mysql -u root < sql/dml/02_dml.sql
mysql -u root < sql/dml/03_dml_extended.sql
```

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [docs/README.md](docs/README.md) | Guía de uso completa |
| [docs/DESIGN.md](docs/DESIGN.md) | Arquitectura y decisiones técnicas |
| [docs/criterios.md](docs/criterios.md) | Mapeo de criterios de evaluación |
| [docs/ensayo/ensayo.md](docs/ensayo/ensayo.md) | Ensayo académico |
| [docs/evidencias/logs.md](docs/evidencias/logs.md) | Logs de ejecución |

## Repositorio

https://github.com/edvvdev/uasdCrudPython

## Autores

- Framiel Trinidad
- Edwing Perez
- Jharol Duran

**Universidad**: Universidad Autónoma de Santo Domingo (UASD)
**Curso**: INF-8237-C2: Ciencias de Datos 1
**Profesora**: Silveria del Orbe Abad
