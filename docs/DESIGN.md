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
├── requirements.txt       # Dependencias Python
├── src/
│   ├── fase1_main.py      # CRUD + Import/Export + Métricas
│   └── fase2_orm.py       # ORM POO (DbContext, Entity, Model, Controller)
├── sql/
│   ├── 00_init.sql        # CREATE DATABASE
│   ├── 01_ddl.sql         # CREATE TABLE + Constraints
│   ├── 02_dml.sql         # INSERT datos
│   ├── 03_queries.sql     # 10 consultas analíticas
│   └── run_all.sql        # Script maestro
├── docs/
│   ├── README.md
│   ├── DESIGN.md
│   └── ensayo.md
└── data/                   # Exports CSV/JSON
```

### Capas del Sistema

```
┌─────────────────────────────────────────────┐
│         SakilaWorkflowController            │
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
| `DbContext` | Crear/destruir conexiones, ejecutar queries parametrizadas, manejar errores |
| `CountryEntity` | Representar tabla country con country_id, country, last_update |
| `CityEntity` | Representar tabla city con city_id, city, country_id, last_update |
| `FilmEntity` | Representar tabla film con film_id, title, rental_rate, length, replacement_cost, release_year |
| `DataRepository` | Transformar filas SQL en List<Entity>, coordinar con DbContext |
| `SakilaWorkflowController` | Orquestar operaciones, sincronizar estado objeto-BD |

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

### Stack Tecnológico

- **Lenguaje**: Python 3.8+
- **Base de Datos**: MariaDB con Sakila
- **Driver**: mysql-connector-python (conector nativo)
- **Análisis**: pandas, numpy (métricas descriptivas)
- **Estructuras**: typing.List para genericidad

## Limitaciones Conocidas

- Credenciales hardcodeadas en archivos (no producción)
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
# Fase I
python fase1_main.py

# Fase II
python fase2_orm.py
```

## Historial de Cambios

### 2026-06-05 - v1.0

**Cambios**: Versión inicial con Fase I y Fase II completas

**Razón**: Entrega de proyecto académico