# uasdCrudPython

> Proyecto académico para la Maestría en Ciencia de Datos e Inteligencia Artificial. Implementación de CRUD/ORM nativo en Python con MariaDB (Sakila).

## Visión General

Este proyecto demuestra una implementación de arquitectura ORM nativa en Python, conectando con la base de datos Sakila de MariaDB. Cubre dos fases: operaciones CRUD básicas con métricas descriptivas, y una arquitectura ORM completa con DbContext, Entities, Models y Controller.

## Arquitectura del Proyecto

```
uasdCrudPython/
├── Fase1.sql              # DDL, DML y 10 consultas SQL
├── requirements.txt       # Dependencias Python
├── src/
│   ├── fase1_main.py      # CRUD + Import/Export + Métricas (Fase I)
│   └── fase2_orm.py       # ORM POO con DbContext, Entity, Model, Controller (Fase II)
├── docs/
│   ├── README.md           # Este documento
│   ├── DESIGN.md           # Diseño técnico
│   └── ensayo.md           # Ensayo académico completo
└── data/                   # Carpeta para exports CSV/JSON
```

## Características

### Fase I: Operaciones Básicas

- **CRUD Query-Level**: Create, Read, Update, Delete para Country, City y Film
- **Import/Export CSV**: Exportación de tablas a archivos CSV
- **Import/Export JSON**: Exportación de tablas a archivos JSON
- **Métricas Descriptivas**: Media, Rango, Desviación Estándar, Varianza, Covarianza

### Fase II: Arquitectura ORM

- **DbContext**: Gestor de conexiones y transacciones con MySQL
- **Entities**: CountryEntity, CityEntity, FilmEntity (mapeo 1:1 con tablas)
- **Models**: DataRepository con List<Entity> para hidratación de datos
- **Controller**: SakilaWorkflowController para orquestar el flujo de negocio

## Requisitos

- Python 3.8+
- MariaDB/MySQL con base de datos Sakila
- Dependencias:
  ```bash
  pip install mysql-connector-python pandas numpy
  ```

## Configuración

### Base de Datos

```sql
# Importar estructura y datos
mysql -u root < Fase1.sql
```

### Conexión en Código

Los archivos vienen configurados con:
- Host: `localhost`
- Puerto: `3306`
- Usuario: `root`
- Contraseña: `0000` (vacía para MariaDB local)
- Base de datos: `sakila`

## Uso

### Fase I: Ejecución de CRUD Básico

```bash
python src/fase1_main.py
```

Operaciones realizadas:
1. Crear país (con validación de duplicados via Unique Constraint)
2. Crear ciudad vinculada a país
3. Actualizar tarifa de película
4. Leer últimos países
5. Eliminar ciudad (validando FK)
6. Exportar tabla Film a CSV
7. Exportar tabla City a JSON
8. Calcular métricas descriptivas

### Fase II: ORM Nativo

```bash
python src/fase2_orm.py
```

Flujo:
1. Crear entidad Country en memoria
2. Persistir entidad via DbContext
3. Forzar duplicado para auditar Unique Constraint
4. Hidratar List<CountryEntity> desde repositorio
5. Crear entidad City vinculada a Country
6. Modificar estado de FilmEntity y sincronizar con BD
7. Eliminar entidad via capa intermedia

## API Reference

### Clases - Fase II (ORM)

| Clase | Descripción |
|-------|-------------|
| `DbContext` | Gestiona ciclo de vida de conexiones y transacciones |
| `CountryEntity` | Mapeo de tabla country (country_id, country, last_update) |
| `CityEntity` | Mapeo de tabla city (city_id, city, country_id, last_update) |
| `FilmEntity` | Mapeo de tabla film (film_id, title, rental_rate, length, etc.) |
| `DataRepository` | Abstrae DbContext, convierte filas en List<Entity> |
| `SakilaWorkflowController` | Orquesta flujo de negocio y comunicación con cliente |

### Funciones - Fase I

| Función | Descripción |
|---------|-------------|
| `obtener_conexion()` | Establece conexión segura con MySQL |
| `crud_crear_pais(nombre)` | Inserta país nuevo |
| `crud_leer_paises(limite)` | Lee últimos N países |
| `crud_crear_ciudad(nombre, pais_id)` | Inserta ciudad vinculada |
| `crud_actualizar_tarifa_pelicula(id, tarifa)` | Actualiza rental_rate |
| `crud_eliminar_ciudad(id)` | Elimina ciudad por ID |
| `exportar_a_csv(tabla, ruta)` | Exporta tabla a CSV |
| `exportar_a_json(tabla, ruta)` | Exporta tabla a JSON |
| `calcular_metricas_descriptivas()` | Calcula stats de film (length, replacement_cost) |

## Integridad de Datos

### Constraints Definidos

- `unique_country`: Nombre de país único
- `unique_city_country`: Ciudad única por país (composite)
- `unique_title_release`: Título único por año de lanzamiento
- `fk_city_country`: Foreign key con ON DELETE RESTRICT
- `fk_inventory_film`: Foreign key con ON DELETE RESTRICT

## Consultas SQL Incluidas

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

Equipo Colaborativo - Maestría en Ciencia de Datos e Inteligencia Artificial

## Licencia

Academic Use / Uso Académico