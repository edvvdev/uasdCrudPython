# SQL Scripts - Fase I

Carpeta que contiene los scripts SQL organizados por tipo de operación.

## Estructura

| Archivo | Descripción |
|---------|-------------|
| `00_init.sql` | DROP DATABASE y CREATE DATABASE sakila |
| `01_ddl.sql` | CREATE TABLE con constraints de integridad |
| `02_dml.sql` | INSERT para poblar datos de prueba |
| `03_queries.sql` | 10 consultas analíticas |
| `run_all.sql` | Script maestro que ejecuta todos en secuencia |

## Uso

```bash
# Ejecutar todos los scripts
mysql -u root < sql/run_all.sql

# O ejecutar individualmente
mysql -u root < sql/00_init.sql
mysql -u root < sql/01_ddl.sql
mysql -u root < sql/02_dml.sql

# Probar consultas
mysql -u root sakila < sql/03_queries.sql
```

## Constraints Implementados

| Tabla | Constraint | Propósito |
|-------|------------|-----------|
| country | unique_country | Nombre de país único |
| city | unique_city_country | Ciudad única por país (composite) |
| city | fk_city_country | FK con ON DELETE RESTRICT |
| film | unique_title_release | Título único por año |
| inventory | fk_inventory_film | FK con ON DELETE RESTRICT |