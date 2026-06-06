# uasdCrudPython - Diseño Técnico

## Objetivos

- Implementar CRUD básico en Python para gestionar entities (Country, City, Film)
- Demonstrar arquitectura ORM nativa con DbContext, Entity, Model y Controller
- Validar integridad de datos con unique constraints y foreign keys
- Proporcionar import/export CSV y JSON para interoperabilidad
- Calcular métricas descriptivas (media, rango, desviación, varianza, covarianza)

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
├── setup.py                # Paquete instalable
├── requirements.txt       # Dependencias Python
├── .env                    # Configuración local
├── src/
│   ├── config.py           # Configuración centralizada
│   ├── main.py            # Orchestrator (ejecutado via main.py)
│   ├── dbcontext.py       # DbContext (gestor de conexiones)
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
│   └── evidencias/
└── data/
```

### Capas del Sistema

```
┌─────────────────────────────────────────────┐
│              main.py                        │
│      (Orchestrator + CLI + Menú)           │
├─────────────────────────────────────────────┤
│           SakilaWorkflowController          │
│      (Orquesta flujo de negocio)           │
├─────────────────────────────────────────────┤
│           DataRepository                    │
│    (List<Entity> - Abstracción de datos)    │
├─────────────────────────────────────────────┤
│             DbContext                       │
│    (Gestión de conexiones y transacciones)  │
├─────────────────────────────────────────────┤
│         MySQL Connector                     │
│        (Driver nativo Python)              │
├─────────────────────────────────────────────┤
│              MariaDB                        │
│              (Sakila)                       │
└─────────────────────────────────────────────┘
```

### Componentes Core

| Componente | Responsabilidad |
|------------|-----------------|
| `main.py` | Entry point unificado con CLI y menú interactivo |
| `config.py` | Configuración centralizada de BD (credenciales) |
| `DbContext` | Crear/destruir conexiones, ejecutar queries parametrizadas |
| `CrudService` | Operaciones CRUD para Country, City, Film |
| `ExportService` | Import/Export CSV y JSON |
| `MetricsService` | Cálculo de métricas descriptivas |
| `CountryEntity` | Mapeo tabla country |
| `CityEntity` | Mapeo tabla city |
| `FilmEntity` | Mapeo tabla film |
| `DataRepository` | Transformar filas SQL en List<Entity> |
| `SakilaWorkflowController` | Orquestar operaciones Fase II |

## Diseño de Datos

### Esquema de Tablas

```sql
country (country_id PK, country UNIQUE, last_update)
city (city_id PK, city, country_id FK, last_update, UNIQUE(city, country_id))
film (film_id PK, title, description, release_year, rental_duration, rental_rate, length, replacement_cost, rating, last_update, UNIQUE(title, release_year))
inventory (inventory_id PK, film_id FK, store_id, last_update)
```

### Integridad Referencial

- City.country_id → Country.country_id (ON DELETE RESTRICT)
- Inventory.film_id → Film.film_id (ON DELETE RESTRICT)
- Unique constraints evitan duplicados a nivel de BD

## Decisiones Técnicas

| Fecha | Decisión | Razón | Impacto |
|-------|-----------|-------|---------|
| 2026-06-05 | MySQL Connector nativo | Sin dependencias ORM externas, control total de SQL | Mayor curva de aprendizaje |
| 2026-06-05 | Unique constraints en BD | Integridad enforceada en origen | Errores controlados por arquitectura |
| 2026-06-05 | List<Entity> como modelo | Colecciones tipadas para interoperabilidad Python | Memoria adicional pero type-safe |
| 2026-06-06 | Config centralizada (.env) | Separar configuración de código | Facilita despliegue |
| 2026-06-06 | Paquete instalable (pip install -e .) | Facilita imports y distribución | Más profesional |

### Stack Tecnológico

- **Lenguaje**: Python 3.8+
- **Base de Datos**: MariaDB con Sakila
- **Driver**: mysql-connector-python (conector nativo)
- **Análisis**: pandas, numpy (métricas descriptivas)
- **Config**: python-dotenv (gestión de credenciales)
- **Estructuras**: typing.List para genericidad

## Limitaciones Conocidas

- Sin connection pooling
- Sin transacción distribuida
- Solo soporta un cliente a la vez

## Métricas Implementadas

| Métrica | Descripción |
|---------|-------------|
| Media | Promedio aritmético de length y replacement_cost |
| Rango | Diferencia entre max y min (np.ptp) |
| Desviación Estándar | Std con ddof=1 (muestral) |
| Varianza | Varianza muestral (ddof=1) |
| Covarianza | Matriz de covarianza entre length y replacement_cost |

## Ejecución

```bash
# Instalar como paquete
pip install -e .

# Menú interactivo
python src/main.py

# CLI flags
python src/main.py --fase1
python src/main.py --fase2
python src/main.py --queries
python src/main.py --all
```

## Historial de Cambios

### 2026-06-06 - v2.0

**Cambios**:
- Reestructuración modular (services por responsabilidad)
- Punto de entrada unificado (main.py con CLI)
- Configuración centralizada (config.py + .env)
- Paquete instalable (setup.py + pip install -e .)

**Razón**: Mejores prácticas de ingeniería de software
