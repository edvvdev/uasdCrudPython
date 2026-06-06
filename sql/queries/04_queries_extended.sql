-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- CONSULTAS EXTENDIDAS - SAKILA COMPLETO
-- =====================================================================

-- =============================================================================
-- CONSULTAS EXISTENTES (ORIGINALES)
-- =============================================================================

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

-- =============================================================================
-- CONSULTAS NUEVAS (TABLAS EXTENDIDAS)
-- =============================================================================

-- Consulta 11: Actores por película (JOIN film_actor + actor)
SELECT f.title, a.first_name, a.last_name
FROM film f
INNER JOIN film_actor fa ON f.film_id = fa.film_id
INNER JOIN actor a ON fa.actor_id = a.actor_id
ORDER BY f.title;

-- Consulta 12: Categorías por película (JOIN film_category + category)
SELECT f.title, c.name AS category
FROM film f
INNER JOIN film_category fc ON f.film_id = fc.film_id
INNER JOIN category c ON fc.category_id = c.category_id
ORDER BY f.title;

-- Consulta 13: Películas por actor (búsqueda por actor)
SELECT a.first_name, a.last_name, f.title
FROM actor a
INNER JOIN film_actor fa ON a.actor_id = fa.actor_id
INNER JOIN film f ON fa.film_id = f.film_id
WHERE a.last_name LIKE '%Reeves%';

-- Consulta 14: Staff activo por tienda
SELECT s.username, s.first_name, s.last_name, st.store_id
FROM staff s
INNER JOIN store st ON s.store_id = st.store_id
WHERE s.active = 1;

-- Consulta 15: Direcciones completas con ciudad y país
SELECT a.address, a.district, a.phone, c.city, co.country
FROM address a
INNER JOIN city c ON a.city_id = c.city_id
INNER JOIN country co ON c.country_id = co.country_id;

-- Consulta 16: Clientes por tienda
SELECT c.first_name, c.last_name, c.email, st.store_id
FROM customer c
INNER JOIN store st ON c.store_id = st.store_id
ORDER BY st.store_id;

-- Consulta 17: Alquileres activos (sin devolver)
SELECT r.rental_id, r.rental_date, f.title, c.first_name, c.last_name
FROM rental r
INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
INNER JOIN customer c ON r.customer_id = c.customer_id
WHERE r.return_date IS NULL;

-- Consulta 18: Historial de pagos por cliente
SELECT c.first_name, c.last_name, p.amount, p.payment_date
FROM payment p
INNER JOIN customer c ON p.customer_id = c.customer_id
ORDER BY c.customer_id, p.payment_date;

-- Consulta 19: Total de ingresos por tienda
SELECT st.store_id, SUM(p.amount) AS total_ingresos
FROM payment p
INNER JOIN staff s ON p.staff_id = s.staff_id
INNER JOIN store st ON s.store_id = st.store_id
GROUP BY st.store_id;

-- Consulta 20: Empleado que más alquila (staff con más rentals)
SELECT s.first_name, s.last_name, COUNT(r.rental_id) AS total_alquileres
FROM staff s
INNER JOIN rental r ON s.staff_id = r.staff_id
GROUP BY s.staff_id
ORDER BY total_alquileres DESC;

-- Consulta 21: Cliente que más gasta
SELECT c.first_name, c.last_name, SUM(p.amount) AS total_gastado
FROM customer c
INNER JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY total_gastado DESC;

-- Consulta 22: Películas más alquiladas
SELECT f.title, COUNT(r.rental_id) AS veces_alquilada
FROM film f
INNER JOIN inventory i ON f.film_id = i.film_id
INNER JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id
ORDER BY veces_alquilada DESC;

-- Consulta 23: Top 3 categorías más populares
SELECT c.name, COUNT(r.rental_id) AS alquileres
FROM category c
INNER JOIN film_category fc ON c.category_id = fc.category_id
INNER JOIN film f ON fc.film_id = f.film_id
INNER JOIN inventory i ON f.film_id = i.film_id
INNER JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY c.category_id
ORDER BY alquileres DESC
LIMIT 3;

-- Consulta 24: Duración promedio de películas por categoría
SELECT c.name, ROUND(AVG(f.length), 2) AS duracion_promedio
FROM category c
INNER JOIN film_category fc ON c.category_id = fc.category_id
INNER JOIN film f ON fc.film_id = f.film_id
GROUP BY c.category_id;

-- Consulta 25: Información completa de rental con detalles
SELECT
    r.rental_id,
    r.rental_date,
    r.return_date,
    f.title,
    c.first_name AS cliente_nombre,
    c.last_name AS cliente_apellido,
    s.username AS atendido_por
FROM rental r
INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
INNER JOIN customer c ON r.customer_id = c.customer_id
INNER JOIN staff s ON r.staff_id = s.staff_id
ORDER BY r.rental_date DESC;
