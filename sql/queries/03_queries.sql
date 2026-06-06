-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- FASE I: CONSULTAS ANALÍTICAS (10 QUERIES)
-- =====================================================================

-- Consulta 1: Películas con costo de reemplazo crítico (mayor a $15.00)
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