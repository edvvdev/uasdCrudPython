# uasdCrudPython

> Proyecto académico - Maestría en Ciencia de Datos e Inteligencia Artificial
> Implementación CRUD/ORM nativo en Python con MariaDB (Sakila)

## Cumplimiento de Criterios de Evaluación

| # | Criterio | Puntos | Estado |
|---|----------|--------|--------|
| 1 | FASE I: Queries SQL + Python |8 | ✅ |
| 2 | DbContext + ORM framework | 3 | ✅ |
| 3 | Entity |3 | ✅ |
| 4 | Model (list<entity>) | 3 | ✅ |
| 5 | Controller | 3 | ✅ |
| 6 | Video explicativo (opcional) | 3 | ❌ |

Ver [docs/criterios.md](docs/criterios.md) para mapeo completo.

## Estructura del Proyecto

```
uasdCrudPython/
├── requirements.txt       # Dependencias Python
├── README.md
├── src/
│   ├── dbcontext.py       # DbContext (gestor de conexiones)
│   ├── fase1_main.py      # Fase I: CRUD + Import/Export + Métricas
│   ├── fase2_orm.py       # Fase II: Punto de entrada ORM
│   ├── entities/
│   │   └── __init__.py    # CountryEntity, CityEntity, FilmEntity
│   ├── models/
│   │   └── data_repository.py  # List<Entity>
│   └── controllers/
│       └── sakila_controller.py # SakilaWorkflowController
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
│   ├── README.md          # Este documento
│   ├── DESIGN.md          # Diseño técnico
│   ├── criterios.md       # Mapeo de criterios de evaluación
│   ├── ensayo/
│   │   └── ensayo.md # Ensayo académico
│   └── evidencias/       # Screenshots de corrida
└── data/                  # Exports CSV/JSON
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

## Arquitectura ORM Modular

```
┌─────────────────────────────────────────────────────────────┐
│                    SakilaWorkflowController                │
│              (Orquesta flujo de negocio) [2 pts]         │
├─────────────────────────────────────────────────────────────┤
│                     DataRepository                         │
│              (List<Entity> - Abstracción)  [1 pt]         │
├─────────────────────────────────────────────────────────────┤
│                      DbContext                             │
│         (Gestión de conexiones y transacciones)  [1 pt]   │
├─────────────────────────────────────────────────────────────┤
│               mysql-connector-python                       │
│                    (Driver nativo)                        │
├─────────────────────────────────────────────────────────────┤
│                      MariaDB                               │
│                      (Sakila)                              │
└─────────────────────────────────────────────────────────────┘
```

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [docs/README.md](docs/README.md) | Guía de uso completa |
| [docs/DESIGN.md](docs/DESIGN.md) | Arquitectura y decisiones técnicas |
| [docs/criterios.md](docs/criterios.md) | Mapeo de criterios de evaluación |
| [docs/ensayo/ensayo.md](docs/ensayo/ensayo.md) | Ensayo académico |
| [sql/README.md](sql/README.md) | Documentación SQL |

## Repositorio

https://github.com/edvvdev/uasdCrudPython