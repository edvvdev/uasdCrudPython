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
│   ├── fase1_main.py      # Fase I: CRUD + Import/Export + Métricas
│   └── fase2_orm.py       # Fase II: ORM (DbContext, Entity, Model, Controller)
├── sql/
│   ├── README.md          # Documentación SQL
│   ├── 00_init.sql        # CREATE DATABASE
│   ├── 01_ddl.sql         # CREATE TABLE + Constraints
│   ├── 02_dml.sql         # INSERT datos
│   ├── 03_queries.sql     # 10 consultas analíticas
│   └── run_all.sql        # Script maestro
├── docs/
│   ├── README.md          # Guía de uso
│   ├── DESIGN.md          # Diseño técnico
│   └── ensayo.md          # Ensayo académico
└── data/                  # Exports CSV/JSON
```

## Quick Start

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Importar base de datos (script maestro)
mysql -u root < sql/run_all.sql

# 3. Ejecutar Fase I
python src/fase1_main.py

# 4. Ejecutar Fase II
python src/fase2_orm.py
```

## Documentación

| Documento | Descripción |
|-----------|-------------|
| [docs/README.md](docs/README.md) | Guía de uso, API reference, configuración |
| [docs/DESIGN.md](docs/DESIGN.md) | Arquitectura, decisiones técnicas, limitaciones |
| [docs/ensayo.md](docs/ensayo.md) | Ensayo académico con todos los criterios de evaluación |
| [sql/README.md](sql/README.md) | Documentación de scripts SQL |

## Tecnologías

- **Python 3.8+** - Lenguaje principal
- **MariaDB** - Sistema de gestión de base de datos
- **mysql-connector-python** - Conector nativo MySQL
- **pandas/numpy** - Análisis de datos y métricas

## Repositorio

https://github.com/edvvdev/uasdCrudPython