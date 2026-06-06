-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- CASO PRÁCTICO 2: CRUD/ORM NATIVO Y ESTRUCTURAS DE DATOS
-- FASE I: ENTORNOS RELACIONALES, INTEGRIDAD Y CONSULTAS ANALÍTICAS
-- =====================================================================

-- ---------------------------------------------------------------------
-- PASO 1: REINICIO Y CREACIÓN DEL ENTORNO DE DATOS
-- ---------------------------------------------------------------------
DROP DATABASE IF EXISTS sakila;
CREATE DATABASE sakila;
USE sakila;

-- ---------------------------------------------------------------------
-- PASO 2: CREACIÓN DE ESTRUCTURAS (DDL) CON RESTRICCIONES DE INTEGRIDAD (Punto 5)
-- ---------------------------------------------------------------------

-- 1. Tabla de Países (Country)
CREATE TABLE country (
    country_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    country VARCHAR(50) NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (country_id),
    CONSTRAINT unique_country UNIQUE (country) -- Garantiza unicidad del nombre del país
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Tabla de Ciudades (City)
CREATE TABLE city (
    city_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    city VARCHAR(50) NOT NULL,
    country_id SMALLINT UNSIGNED NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (city_id),
    CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT unique_city_country UNIQUE (city, country_id) -- Impide duplicar una ciudad en el mismo país
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Tabla de Películas (Film)
CREATE TABLE film (
    film_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(128) NOT NULL,
    description TEXT DEFAULT NULL,
    release_year YEAR DEFAULT NULL,
    rental_duration TINYINT UNSIGNED NOT NULL DEFAULT 3,
    rental_rate DECIMAL(4,2) NOT NULL DEFAULT 4.99,
    length SMALLINT UNSIGNED DEFAULT NULL,
    replacement_cost DECIMAL(5,2) NOT NULL DEFAULT 19.99,
    rating ENUM('G','PG','PG-13','R','NC-17') DEFAULT 'G',
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (film_id),
    CONSTRAINT unique_title_release UNIQUE (title, release_year) -- Evita registrar la misma película el mismo año
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Tabla de Inventario (Inventory)
CREATE TABLE inventory (
    inventory_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    film_id SMALLINT UNSIGNED NOT NULL,
    store_id TINYINT UNSIGNED NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (inventory_id),
    CONSTRAINT fk_inventory_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------------------------------------
-- PASO 3: INGESTIÓN Y POBLACIÓN DE DATOS DE PRUEBA (DML)
-- ---------------------------------------------------------------------

-- Ingestión de Países
INSERT INTO country (country) VALUES 
('Dominican Republic'), ('United States'), ('Spain'), ('Mexico'), ('Colombia');

-- Ingestión de Ciudades
INSERT INTO city (city, country_id) VALUES 
('Santo Domingo', 1), ('Santiago', 1), ('New York', 2), 
('Madrid', 3), ('CDMX', 4), ('Bogota', 5);

-- Ingestión de Catálogo de Películas
INSERT INTO film (title, description, release_year, rental_duration, rental_rate, length, replacement_cost, rating) VALUES 
('Inception', 'A thief who steals corporate secrets through use of dream-sharing.', 2010, 5, 4.99, 148, 19.99, 'PG-13'),
('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality.', 1999, 7, 3.99, 136, 14.99, 'R'),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.', 2014, 6, 4.99, 169, 24.99, 'PG-13'),
('Spirited Away', 'During her family move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods.', 2001, 3, 2.99, 125, 12.99, 'PG'),
('Casablanca', 'A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover.', 1942, 4, 1.99, 102, 9.99, 'PG');

-- Ingestión de Inventario Físico de Tiendas
INSERT INTO inventory (film_id, store_id) VALUES 
(1, 1), (1, 2), (2, 1), (3, 1), (4, 2), (5, 1);


-- ---------------------------------------------------------------------
-- PASO 4: SET DE 10 CONSULTAS ANALÍTICAS EXIGIDAS POR LA ASIGNACIÓN
-- ---------------------------------------------------------------------

-- Consulta 1: Listar películas con costo de reemplazo crítico (mayor a $15.00)
SELECT title, release_year, replacement_cost, rating 
FROM film 
WHERE replacement_cost > 15.00;

-- Consulta 2: Join de variables geográficas (Ciudades con sus respectivos países)
SELECT ci.city_id, ci.city, co.country 
FROM city ci
INNER JOIN country co ON ci.country_id = co.country_id;

-- Consulta 3: Métrica agregada de densidad urbana (Ciudades por país ordenadas de mayor a menor)
SELECT co.country, COUNT(ci.city_id) AS total_ciudades
FROM country co
LEFT JOIN city ci ON co.country_id = ci.country_id
GROUP BY co.country_id
ORDER BY total_ciudades DESC;

-- Consulta 4: Análisis descriptivo relacional (Duración promedio por clasificación de edad)
SELECT rating, ROUND(AVG(length), 2) AS duracion_promedio
FROM film
GROUP BY rating;

-- Consulta 5: Búsqueda indexada por patrones de texto en títulos (Caso de contingencia)
SELECT film_id, title, rental_rate, rating 
FROM film 
WHERE title LIKE '%Matrix%' OR title LIKE '%Inception%';

-- Consulta 6: Auditoría de stock para el inventario activo de la Tienda ID 1
SELECT i.inventory_id, f.title, i.store_id 
FROM inventory i
JOIN film f ON i.film_id = f.film_id
WHERE i.store_id = 1;

-- Consulta 7: Filtro multidimensional (Películas con tarifa media-alta y larga duración)
SELECT title, rental_rate, length 
FROM film 
WHERE rental_rate BETWEEN 3.00 AND 6.00 AND length > 120;

-- Consulta 8: Control de volumen (Conteo total de existencias físicas por título de película)
SELECT f.title, COUNT(i.inventory_id) AS copias_disponibles
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
GROUP BY f.film_id;

-- Consulta 9: Integridad de datos residuales (Búsqueda de países huérfanos sin ciudades asociadas)
SELECT co.country 
FROM country co
LEFT JOIN city ci ON co.country_id = ci.country_id
WHERE ci.city_id IS NULL;

-- Consulta 10: Subconsulta avanzada (Identificación del registro con el máximo costo operativo)
SELECT title, replacement_cost 
FROM film 
WHERE replacement_cost = (SELECT MAX(replacement_cost) FROM film);

-- Instalacion de python
pip install mysql-connector-python pandas numpy
