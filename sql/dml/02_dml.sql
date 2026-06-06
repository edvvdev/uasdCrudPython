-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- FASE I: DML - DATA MANIPULATION LANGUAGE
-- INGESTIÓN Y POBLACIÓN DE DATOS DE PRUEBA
-- =====================================================================

-- Ingestión de Países
INSERT INTO country (country) VALUES
('Dominican Republic'),
('United States'),
('Spain'),
('Mexico'),
('Colombia');

-- Ingestión de Ciudades
INSERT INTO city (city, country_id) VALUES
('Santo Domingo', 1),
('Santiago', 1),
('New York', 2),
('Madrid', 3),
('CDMX', 4),
('Bogota', 5);

-- Ingestión de Catálogo de Películas
INSERT INTO film (title, description, release_year, rental_duration, rental_rate, length, replacement_cost, rating) VALUES
('Inception', 'A thief who steals corporate secrets through use of dream-sharing.', 2010, 5, 4.99, 148, 19.99, 'PG-13'),
('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality.', 1999, 7, 3.99, 136, 14.99, 'R'),
('Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.', 2014, 6, 4.99, 169, 24.99, 'PG-13'),
('Spirited Away', 'During her family move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods.', 2001, 3, 2.99, 125, 12.99, 'PG'),
('Casablanca', 'A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover.', 1942, 4, 1.99, 102, 9.99, 'PG');

-- Ingestión de Inventario Físico de Tiendas
INSERT INTO inventory (film_id, store_id) VALUES
(1, 1), (1, 2),
(2, 1),
(3, 1),
(4, 2),
(5, 1);