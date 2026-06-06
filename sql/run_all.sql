-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- FASE I: SCRIPT MAESTRO - EJECUTA TODOS LOS SCRIPTS EN ORDEN
-- =====================================================================

-- Ejecutar en orden:
-- 1. 00_init.sql   (Crear base de datos)
-- 2. 01_ddl.sql    (Crear tablas)
-- 3. 02_dml.sql    (Insertar datos)
-- 4. 03_queries.sql (Consultas de prueba)

-- Para ejecutar todos juntos desde consola:
-- mysql -u root < sql/run_all.sql

-- O individualmente:
-- mysql -u root < sql/00_init.sql
-- mysql -u root < sql/01_ddl.sql
-- mysql -u root < sql/02_dml.sql
-- mysql -u root < sql/03_queries.sql

SOURCE sql/00_init.sql;
SOURCE sql/01_ddl.sql;
SOURCE sql/02_dml.sql;
SOURCE sql/03_queries.sql;