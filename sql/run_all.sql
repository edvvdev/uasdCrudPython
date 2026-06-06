-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- SCRIPT MAESTRO - EJECUTA TODOS LOS SCRIPTS EN ORDEN
-- =====================================================================

-- ORDEN DE EJECUCIÓN:
-- 1.00_init.sql                    (Crear base de datos)
-- 2. ddl/01_ddl.sql (Tablas base: country, city, film, inventory)
-- 3. ddl/02_ddl_extended.sql        (Tablas extendidas Sakila completo)
-- 4. dml/02_dml.sql                (Datos base)
-- 5. dml/03_dml_extended.sql       (Datos extendidos)
-- 6. queries/03_queries.sql        (Consultas básicas1-10)
-- 7. queries/04_queries_extended.sql (Consultas extendidas 11-25)

SOURCE sql/00_init.sql;
SOURCE sql/ddl/01_ddl.sql;
SOURCE sql/ddl/02_ddl_extended.sql;
SOURCE sql/dml/02_dml.sql;
SOURCE sql/dml/03_dml_extended.sql;
SOURCE sql/queries/03_queries.sql;
SOURCE sql/queries/04_queries_extended.sql;
