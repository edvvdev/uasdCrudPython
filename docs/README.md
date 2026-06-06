# uasdCrudPython - Documentación de Uso

> Proyecto académico para la Maestría en Ciencia de Datos e Inteligencia Artificial. Implementación de CRUD/ORM nativo en Python con MariaDB (Sakila).

## Visión General

Este proyecto demuestra una implementación de arquitectura ORM nativa en Python, conectando con la base de datos Sakila de MariaDB. Cubre dos fases: operaciones CRUD básicas con métricas descriptivas, y una arquitectura ORM completa con DbContext, Entities, Models y Controller.

## Estructura del Proyecto

```
uasdCrudPython/
├── main.py                  # Punto de entrada unificado (CLI + menú)
├── setup.py                # Paquete instalable
├── requirements.txt       # Dependencias Python
├── .env                    # Configuración local
├── src/
│   ├── config.py           # Configuración centralizada
│   ├── main.py            # Orchestrator + CLI
│   ├── dbcontext.py       # Gestor de conexiones
│   ├── fase1/
│   │   ├── crud_service.py    # CRUD operations
│   │   ├── export_service.py  # CSV/JSON I/O
│   │   └── metrics_service.py # Métricas descriptivas
│   ├── fase2/
│   │   ├── entities/
│   │   ├── models/
│   │   └── controllers/
│   └── utils/
│       └── helpers.py
├── sql/
│   ├── ddl/
│   ├── dml/
│   └── queries/
├── docs/
│   ├── README.md           # Este documento
│   ├── DESIGN.md          # Diseño técnico
│   ├── criterios.md       # Mapeo de criterios de evaluación
│   ├── ensayo/
│   │   └── ensayo.md      # Ensayo académico
│   └── evidencias/
└── data/                   # Exports CSV/JSON
```

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/edvvdev/uasdCrudPython.git
cd uasdCrudPython

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar como paquete (desarrollo)
pip install -e .
```

## Uso

### Punto de Entrada Unificado

```bash
# Menú interactivo
python src/main.py

# CLI flags
python src/main.py --fase1      # Ejecutar Fase I
python src/main.py --fase2      # Ejecutar Fase II
python src/main.py --queries    # Mostrar consultas SQL
python src/main.py --all        # Ejecutar todo
```

### Ejecución Individual por Servicio

```python
from src.fase1 import CrudService, ExportService, MetricsService

# CRUD
crud = CrudService()
crud.crear_pais("Brasil")
paises = crud.leer_paises(5)

# Export
export = ExportService()
export.exportar_a_csv("film", "data/peliculas.csv")

# Métricas
metrics = MetricsService()
metrics.calcular_metricas_descriptivas()
```

## Características Implementadas

### Fase I: Operaciones Básicas

| Componente | Descripción | Servicio |
|------------|-------------|----------|
| **CRUD Countries** | Create, Read para países | `CrudService` |
| **CRUD Cities** | Create, Read, Delete para ciudades | `CrudService` |
| **CRUD Films** | Read, Update para películas | `CrudService` |
| **Import/Export CSV** | Exportar/importar tablas a CSV | `ExportService` |
| **Import/Export JSON** | Exportar/importar tablas a JSON | `ExportService` |
| **Métricas Descriptivas** | Media, Rango, Desviación, Varianza, Covarianza | `MetricsService` |

### Fase II: Arquitectura ORM

| Componente | Descripción |
|------------|-------------|
| **DbContext** | Gestor de conexiones y transacciones con MySQL |
| **Entity Objects** | CountryEntity, CityEntity, FilmEntity, InventoryEntity |
| **Model Layer** | DataRepository con List<Entity> para hidratación de datos |
| **Controller** | SakilaWorkflowController para orquestar el flujo de negocio |

## API Reference

### Servicios - Fase I

| Servicio | Descripción |
|----------|-------------|
| `CrudService` | Operaciones CRUD para Country, City, Film |
| `ExportService` | Import/Export CSV y JSON |
| `MetricsService` | Métricas descriptivas (media, rango, desviación, varianza, covarianza) |

### Clases - Fase II (ORM)

| Clase | Descripción |
|-------|-------------|
| `DbContext` | Gestiona ciclo de vida de conexiones y transacciones |
| `CountryEntity` | Mapeo de tabla country |
| `CityEntity` | Mapeo de tabla city |
| `FilmEntity` | Mapeo de tabla film |
| `InventoryEntity` | Mapeo de tabla inventory |
| `DataRepository` | Abstrae DbContext, convierte filas en List<Entity> |
| `SakilaWorkflowController` | Orquesta flujo de negocio |

## Integridad de Datos

### Constraints Implementados

| Tabla | Constraint | Propósito |
|-------|------------|-----------|
| country | unique_country | Nombre de país único |
| city | unique_city_country | Ciudad única por país (composite) |
| film | unique_title_release | Título único por año de lanzamiento |

### Foreign Keys con Comportamiento Restrictivo

| Tabla | Foreign Key | Comportamiento |
|-------|-------------|----------------|
| city | fk_city_country | ON DELETE RESTRICT |
| inventory | fk_inventory_film | ON DELETE RESTRICT |

## Consultas SQL Analíticas

10 consultas implementadas en `sql/queries/03_queries.sql`:
1. Películas con costo de reemplazo > $15.00
2. Join ciudades con países
3. Conteo de ciudades por país
4. Duración promedio por clasificación
5. Búsqueda por patrón en títulos
6. Inventario activo por tienda
7. Películas con tarifa 3-6 y duración > 120
8. Conteo de copias por título
9. Países sin ciudades asociadas
10. Película con máximo costo operativo

## Autores

- Framiel Trinidad
- Edwing Perez
- Jharol Duran

**Universidad**: Universidad Autónoma de Santo Domingo (UASD)
**Curso**: INF-8237-C2: Ciencias de Datos 1
**Profesora**: Silveria del Orbe Abad

## Repositorio

https://github.com/edvvdev/uasdCrudPython
