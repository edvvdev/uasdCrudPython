# uasdCrudPython

> Proyecto académico para la Maestría en Ciencia de Datos e Inteligencia Artificial. Implementación de CRUD/ORM nativo en Python con MariaDB (Sakila).

## Visión General

Este proyecto demuestra una implementación de arquitectura ORM nativa en Python, conectando con la base de datos Sakila de MariaDB. Cubre dos fases: operaciones CRUD básicas con métricas descriptivas, y una arquitectura ORM completa con DbContext, Entities, Models y Controller.

## Estructura del Proyecto

```
uasdCrudPython/
├── requirements.txt       # Dependencias Python
├── README.md
├── src/
│   ├── fase1_main.py      # CRUD + Import/Export + Métricas (Fase I)
│   └── fase2_orm.py       # ORM POO (Fase II)
├── sql/
│   ├── 00_init.sql        # CREATE DATABASE
│   ├── 01_ddl.sql         # CREATE TABLE + Constraints
│   ├── 02_dml.sql         # INSERT datos
│   ├── 03_queries.sql     # 10 consultas analíticas
│   └── run_all.sql         # Script maestro
├── docs/
│   ├── README.md           # Este documento
│   ├── DESIGN.md           # Diseño técnico
│   └── ensayo.md           # Ensayo académico
└── data/                   # Exports CSV/JSON
```

## Características Implementadas

### Fase I: Operaciones Básicas (CRUD + Import/Export + Métricas)

| Componente | Descripción | Función/Archivo |
|------------|-------------|-----------------|
| **CRUD Countries** | Create, Read, Update, Delete para países | `crud_crear_pais()`, `crud_leer_paises()` |
| **CRUD Cities** | Create, Read para ciudades vinculadas | `crud_crear_ciudad()`, `crud_eliminar_ciudad()` |
| **CRUD Films** | Update para tarifas de películas | `crud_actualizar_tarifa_pelicula()` |
| **Import/Export CSV** | Exporta tablas a archivos CSV | `exportar_a_csv(tabla, ruta)` |
| **Import/Export JSON** | Exporta tablas a archivos JSON | `exportar_a_json(tabla, ruta)` |
| **Métricas Descriptivas** | Media, Rango, Desviación, Varianza, Covarianza | `calcular_metricas_descriptivas()` |

### Fase II: Arquitectura ORM

| Componente | Descripción |
|------------|-------------|
| **DbContext** | Gestor de conexiones y transacciones con MySQL |
| **Entity Objects** | CountryEntity, CityEntity, FilmEntity (mapeo 1:1 con tablas) |
| **Model Layer** | DataRepository con List<Entity> para hidratación de datos |
| **Controller** | SakilaWorkflowController para orquestar el flujo de negocio |

## Requisitos

- Python 3.8+
- MariaDB/MySQL
- Dependencias:
  ```bash
  pip install -r requirements.txt
  ```

## Uso

### 1. Importar Base de Datos

```bash
mysql -u root < sql/run_all.sql
```

O individualmente:
```bash
mysql -u root < sql/00_init.sql
mysql -u root < sql/01_ddl.sql
mysql -u root < sql/02_dml.sql
```

### 2. Ejecutar Fase I

```bash
python src/fase1_main.py
```

**Operaciones ejecutadas:**
1. Crear país (con validación de duplicados via Unique Constraint)
2. Crear ciudad vinculada a país
3. Actualizar tarifa de película
4. Leer últimos países
5. Eliminar ciudad (validando FK)
6. Exportar tabla Film a CSV
7. Exportar tabla City a JSON
8. Calcular métricas descriptivas (media, rango, desviación, varianza, covarianza)

### 3. Ejecutar Fase II

```bash
python src/fase2_orm.py
```

**Flujo ORM:**
1. Crear entidad Country en memoria
2. Persistir entidad via DbContext
3. Forzar duplicado para auditar Unique Constraint
4. Hidratar List<CountryEntity> desde repositorio
5. Crear entidad City vinculada a Country
6. Modificar estado de FilmEntity y sincronizar con BD
7. Eliminar entidad via capa intermedia

## API Reference

### Funciones - Fase I

| Función | Descripción |
|---------|-------------|
| `obtener_conexion()` | Establece conexión segura con MySQL |
| `crud_crear_pais(nombre_pais)` | Inserta país nuevo |
| `crud_leer_paises(limite)` | Lee últimos N países |
| `crud_crear_ciudad(nombre_ciudad, id_pais)` | Inserta ciudad vinculada |
| `crud_actualizar_tarifa_pelicula(id_pelicula, nueva_tarifa)` | Actualiza rental_rate |
| `crud_eliminar_ciudad(id_ciudad)` | Elimina ciudad por ID |
| `exportar_a_csv(nombre_tabla, ruta_destino)` | Exporta tabla a CSV |
| `exportar_a_json(nombre_tabla, ruta_destino)` | Exporta tabla a JSON |
| `calcular_metricas_descriptivas()` | Calcula media, rango, desviación, varianza, covarianza |

### Clases - Fase II (ORM)

| Clase | Descripción |
|-------|-------------|
| `DbContext` | Gestiona ciclo de vida de conexiones y transacciones |
| `CountryEntity` | Mapeo de tabla country |
| `CityEntity` | Mapeo de tabla city |
| `FilmEntity` | Mapeo de tabla film |
| `DataRepository` | Abstrae DbContext, convierte filas en List<Entity> |
| `SakilaWorkflowController` | Orquesta flujo de negocio |

## Integridad de Datos (Unique Constraints)

### Constraints Implementados en SQL (`sql/01_ddl.sql`)

| Tabla | Constraint | Columnas | Propósito |
|-------|------------|----------|-----------|
| country | unique_country | country | Evitar países duplicados por nombre |
| city | unique_city_country | city, country_id | Evitar ciudad duplicada en mismo país |
| film | unique_title_release | title, release_year | Evitar título duplicado en mismo año |

### Foreign Keys con Comportamiento Restrictivo

| Tabla | Foreign Key | Referencias | Comportamiento |
|-------|-------------|-------------|----------------|
| city | fk_city_country | country(country_id) | ON DELETE RESTRICT, ON UPDATE CASCADE |
| inventory | fk_inventory_film | film(film_id) | ON DELETE RESTRICT, ON UPDATE CASCADE |

## Consultas SQL Analíticas (`sql/03_queries.sql`)

1. **Películas con costo de reemplazo > $15.00**
2. **Join ciudades con países** (INNER JOIN)
3. **Conteo de ciudades por país** (GROUP BY con LEFT JOIN)
4. **Duración promedio por clasificación** (AVG, GROUP BY)
5. **Búsqueda por patrón en títulos** (LIKE '%...%')
6. **Inventario activo por tienda** (JOIN con фильтро по store_id)
7. **Películas con tarifa 3-6 y duración > 120** (BETWEEN, AND)
8. **Conteo de copias por título** (COUNT, LEFT JOIN)
9. **Países sin ciudades asociadas** (LEFT JOIN WHERE NULL)
10. **Película con máximo costo operativo** (Subconsulta MAX)

## Métricas Descriptivas Implementadas

| Métrica | Descripción | Función |
|---------|-------------|---------|
| **Media** | Promedio aritmético de length y replacement_cost | `np.mean()` |
| **Rango** | Diferencia entre max y min | `np.ptp()` |
| **Desviación Estándar** | Std muestral (ddof=1) | `np.std(ddof=1)` |
| **Varianza** | Varianza muestral (ddof=1) | `np.var(ddof=1)` |
| **Covarianza** | Matriz de covarianza bivariada | `np.cov(ddof=1)` |

## Autores

- Framiel Trinidad
- Edwing Perez
- Jharol Duran

**Universidad**: Universidad Autónoma de Santo Domingo (UASD)  
**Curso**: INF-8237-C2: Ciencias de Datos 1  
**Profesora**: Silveria del Orbe Abad

## Repositorio

https://github.com/edvvdev/uasdCrudPython