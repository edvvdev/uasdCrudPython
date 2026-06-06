# uasdCrudPython

> Proyecto académico - Maestría en Ciencia de Datos e Inteligencia Artificial
> Implementación CRUD/ORM nativo en Python con MariaDB (Sakila)

## Estructura del Proyecto

```
uasdCrudPython/
├── main.py                  # Punto de entrada unificado (CLI + menú)
├── setup.py                # Paquete instalable
├── requirements.txt        # Dependencias Python
├── .env                    # Configuración local (no commitear)
├── .env.example            # Template de configuración
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuración centralizada
│   ├── dbcontext.py       # Gestor de conexiones
│   ├── fase1/
│   │   ├── __init__.py
│   │   ├── crud_service.py    # CRUD operations
│   │   ├── export_service.py  # CSV/JSON I/O
│   │   └── metrics_service.py # Métricas descriptivas
│   ├── fase2/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   ├── models/
│   │   └── controllers/
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── sql/
│   ├── 00_init.sql
│   ├── run_all.sql
│   ├── ddl/
│   ├── dml/
│   └── queries/
├── docs/
│   ├── README.md
│   ├── DESIGN.md
│   ├── criterios.md
│   ├── ensayo/
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
python main.py --queries    # Mostrar consultas SQL
python main.py --all        # Ejecutar todas las fases
```

### Menú Interactivo

```
$ python main.py

============================================
        MENÚ PRINCIPAL - uasdCrudPython
  Maestría en Ciencia de Datos
============================================

  1. FASE I: CRUD + Import/Export + Métricas
  2. FASE II: Arquitectura ORM
  3. CONSULTAS SQL (10 queries)
  4. DOCUMENTACIÓN
  0. Salir

Seleccione una opción:
```

## Criterios de Evaluación

| # | Criterio | Puntos | Estado |
|---|----------|--------|--------|
| 1 | FASE I: Queries SQL + Python | 8 | ✅ |
| 2 | DbContext + ORM framework | 3 | ✅ |
| 3 | Entity | 3 | ✅ |
| 4 | Model (list<entity>) | 3 | ✅ |
| 5 | Controller | 3 | ✅ |
| 6 | Video explicativo (opcional) | 3 | ❌ |

Ver [docs/criterios.md](docs/criterios.md) para mapeo completo.

## Base de Datos

```bash
# Importar estructura y datos
mysql -u root < sql/run_all.sql

# O ejecutar scripts individualmente
mysql -u root < sql/00_init.sql
mysql -u root < sql/ddl/01_ddl.sql
mysql -u root < sql/dml/02_dml.sql
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

## Autores

- Framiel Trinidad
- Edwing Perez
- Jharol Duran

**Universidad**: Universidad Autónoma de Santo Domingo (UASD)
**Curso**: INF-8237-C2: Ciencias de Datos 1
**Profesora**: Silveria del Orbe Abad
