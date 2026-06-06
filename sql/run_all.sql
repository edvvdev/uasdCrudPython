-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- FASE I: SCRIPT MAESTRO - EJECUTA TODOS LOS SCRIPTS EN ORDEN
-- =====================================================================

-- Ejecutar en orden:
-- 1.00_init.sql   (Crear base de datos)
-- 2. ddl/01_ddl.sql (Crear tablas)
-- 3. dml/02_dml.sql    (Insertar datos)
-- 4. queries/03_queries.sql (Consultas de prueba)

SOURCE sql/00_init.sql;
SOURCE sql/ddl/01_ddl.sql;
SOURCE sql/dml/02_dml.sql;
SOURCE sql/queries/03_queries.sql;