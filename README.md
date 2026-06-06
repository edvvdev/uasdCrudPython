# uasdCrudPython

> Proyecto académico - Maestría en Ciencia de Datos e Inteligencia Artificial
> Implementación CRUD/ORM nativo en Python con MariaDB (Sakila)

## Estructura del Proyecto

```
uasdCrudPython/
├── requirements.txt       # Dependencias Python
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── dbcontext.py       # Gestor de conexiones y transacciones
│   ├── fase1_main.py      # Fase I: CRUD + Import/Export + Métricas
│   ├── fase2_orm.py       # Fase II: Punto de entrada ORM
│   ├── entities/
│   │   ├── __init__.py    # CountryEntity, CityEntity, FilmEntity, InventoryEntity
│   ├── models/
│   │   ├── __init__.py
│   │   └── data_repository.py  # List<Entity> y operaciones de negocio
│   └── controllers/
│       ├── __init__.py
│       └── sakila_controller.py  # Orquestador de flujo de negocio
├── sql/
│   ├── 00_init.sql        # CREATE DATABASE
│   ├── run_all.sql        # Script maestro
│   ├── ddl/
│   │   └── 01_ddl.sql     # CREATE TABLE + Constraints
│   ├── dml/
│   │   └── 02_dml.sql     # INSERT datos
│   └── queries/
│       └── 03_queries.sql # 10 consultas analíticas
├── docs/
│   ├── README.md          # Guía de uso
│   ├── DESIGN.md          # Diseño técnico
│   └── ensayo.md          # Ensayo académico
└── data/                  # Exports CSV/JSON
```

## Arquitectura ORM Modular

```
┌─────────────────────────────────────────────────────────────┐
│                    SakilaWorkflowController                │
│              (Orquesta flujo de negocio)                  │
├─────────────────────────────────────────────────────────────┤
│                     DataRepository                         │
│              (List<Entity> - Abstracción) │
├─────────────────────────────────────────────────────────────┤
│                      DbContext                             │
│         (Gestión de conexiones y transacciones)            │
├─────────────────────────────────────────────────────────────┤
│ mysql-connector-python                   │
│                    (Driver nativo) │
├─────────────────────────────────────────────────────────────┤
│ MariaDB                              │
│ (Sakila)                              │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Importar base de datos
mysql -u root < sql/run_all.sql

# 3. Ejecutar Fase I
python src/fase1_main.py

# 4. Ejecutar Fase II (ORM Modular)
python src/fase2_orm.py
```

## Componentes ORM

| Componente | Archivo | Descripción |
|------------|---------|-------------|
| **DbContext** | `src/dbcontext.py` | Gestiona ciclo de vida de conexiones y transacciones |
| **Entities** | `src/entities/__init__.py` | CountryEntity, CityEntity, FilmEntity, InventoryEntity |
| **Models** | `src/models/data_repository.py` | List<Entity> e hidratación de datos |
| **Controllers** | `src/controllers/sakila_controller.py` | Orquesta flujo de negocio |

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [docs/README.md](docs/README.md) | Guía de uso completa |
| [docs/DESIGN.md](docs/DESIGN.md) | Arquitectura y decisiones técnicas |
| [docs/ensayo.md](docs/ensayo.md) | Ensayo académico |
| [sql/README.md](sql/README.md) | Documentación SQL |

## Repositorio

https://github.com/edvvdev/uasdCrudPython