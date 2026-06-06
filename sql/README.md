# SQL Scripts - Fase I

Carpeta que contiene los scripts SQL organizados por tipo de operación.

## Estructura

```
sql/
├── 00_init.sql              # DROP DATABASE y CREATE DATABASE sakila
├── run_all.sql              # Script maestro (ejecuta todos en secuencia)
├── ddl/
│   └── 01_ddl.sql           # CREATE TABLE con constraints de integridad
├── dml/
│   └── 02_dml.sql           # INSERT para poblar datos de prueba
└── queries/
    └── 03_queries.sql       # 10 consultas analíticas
```

## Uso

```bash
# Ejecutar todos los scripts
mysql -u root < sql/run_all.sql

# O individualmente
mysql -u root < sql/00_init.sql
mysql -u root < sql/ddl/01_ddl.sql
mysql -u root < sql/dml/02_dml.sql
mysql -u root < sql/queries/03_queries.sql
```

## Constraints Implementados (ddl/01_ddl.sql)

| Tabla | Constraint | Propósito |
|-------|------------|-----------|
| country | unique_country | Nombre de país único |
| city | unique_city_country | Ciudad única por país (composite) |
| city | fk_city_country | FK con ON DELETE RESTRICT |
| film | unique_title_release | Título único por año |
| inventory | fk_inventory_film | FK con ON DELETE RESTRICT |

## Datos de Prueba (dml/02_dml.sql)

- **Países**: Dominican Republic, United States, Spain, Mexico, Colombia
- **Ciudades**: Santo Domingo, Santiago, New York, Madrid, CDMX, Bogota
- **Películas**: Inception, The Matrix, Interstellar, Spirited Away, Casablanca
- **Inventario**: 6 registros de películas en tiendas

## Consultas Analíticas (queries/03_queries.sql)

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