# uasdCrudPython

> Proyecto académico - Maestría en Ciencia de Datos e Inteligencia Artificial
> Implementación CRUD/ORM nativo en Python con MariaDB (Sakila)

## Estructura del Proyecto

```
uasdCrudPython/
├── Fase1.sql           # DDL, DML, Constraints y 10 Consultas SQL
├── requirements.txt    # Dependencias Python
├── .gitignore
├── src/
│   ├── fase1_main.py   # Fase I: CRUD + Import/Export + Métricas
│   └── fase2_orm.py    # Fase II: ORM (DbContext, Entity, Model, Controller)
├── docs/
│   ├── README.md       # Documentación de uso
│   ├── DESIGN.md       # Diseño técnico
│   └── ensayo.md        # Ensayo académico completo
└── data/               # Carpeta para exports CSV/JSON
```

## Quick Start

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Importar base de datos
mysql -u root < Fase1.sql

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

## Tecnologías

- **Python 3.8+** - Lenguaje principal
- **MariaDB** - Sistema de gestión de base de datos
- **mysql-connector-python** - Conector nativo MySQL
- **pandas/numpy** - Análisis de datos y métricas

## Repositorio

https://github.com/edvvdev/uasdCrudPython