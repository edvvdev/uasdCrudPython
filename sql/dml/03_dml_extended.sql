-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- FASE I: DML EXTENDIDO - DATOS DE PRUEBA PARA TABLAS SAKILA COMPLETAS
-- =====================================================================

-- Ingestión de Idiomas
INSERT INTO language (name) VALUES
('English'),
('Italian'),
('Japanese'),
('Mandarin'),
('French'),
('German');

-- Ingestión de Direcciones (Santiago, RD y NYC, USA)
INSERT INTO address (address, address2, district, city_id, postal_code, phone) VALUES
('100 Money Street', NULL, 'Manhattan', 2, '10001', '212-555-0100'),
('200 Broadway', NULL, 'Queens', 2, '10002', '212-555-0200'),
('Calle El Conde #50', NULL, 'Centro', 1, '10200', '809-555-0100'),
('Av. Abraham Lincoln #100', NULL, 'Ens. Julieta', 1, '10201', '809-555-0200');

-- Ingestión de Empleados (Staff)
INSERT INTO staff (first_name, last_name, address_id, email, store_id, active, username, password) VALUES
('Mike', 'Hauer', 1, 'mike.hauer@sakila.com', 1, 1, 'Mike', '5f4dcc3b5aa765d61d8327deb882cf99'),
('Jon', 'Sullivan', 2, 'jon.sullivan@sakila.com', 1, 1, 'Jon', '5f4dcc3b5aa765d61d8327deb882cf99'),
('Pedro', 'Martinez', 3, 'pedro.martinez@sakila.com', 2, 1, 'Pedro', '5f4dcc3b5aa765d61d8327deb882cf99'),
('Juan', 'Gomez', 4, 'juan.gomez@sakila.com', 2, 1, 'Juan', '5f4dcc3b5aa765d61d8327deb882cf99');

-- Ingestión de Tiendas (Store)
INSERT INTO store (manager_staff_id, address_id) VALUES
(1, 1),
(3, 3);

-- Actualizar store.manager_staff_id después de insertar staff
UPDATE store SET manager_staff_id = 1 WHERE store_id = 1;
UPDATE store SET manager_staff_id = 3 WHERE store_id = 2;

-- Ingestión de Actores
INSERT INTO actor (first_name, last_name) VALUES
('Keanu', 'Reeves'),
('Laurence', 'Fishburne'),
('Carrie-Anne', 'Moss'),
('Hugo', 'Weaving'),
('Christian', 'Bale'),
('Heath', 'Ledger'),
('Marion', 'Cotillard'),
('Joseph', 'Gordon-Levitt'),
('Ellen', 'Page'),
('Leonardo', 'DiCaprio'),
('Joseph', 'Gordon-Levitt'),
('Tom', 'Hardy'),
('Marion', 'Cotillard'),
('Matthew', 'McConaughey'),
('Anne', 'Hathaway'),
('Jessica', 'Chastain'),
('Hayao', 'Miyazaki'),
('Rumi', 'Hiiragi'),
('Catherine', 'Deneuve'),
('Humphrey', 'Bogart'),
('Ingrid', 'Bergman');

-- Ingestión de Categorías
INSERT INTO category (name) VALUES
('Action'),
('Animation'),
('Children'),
('Classics'),
('Comedy'),
('Documentary'),
('Drama'),
('Family'),
('Foreign'),
('Games'),
('Horror'),
('Music'),
('New'),
('Sci-Fi'),
('Sports'),
('Travel');

-- Ingestión de Film-Actor (relaciones)
INSERT INTO film_actor (actor_id, film_id) VALUES
(1, 2),  -- Keanu Reeves in The Matrix
(2, 2),  -- Laurence Fishburne in The Matrix
(3, 2),  -- Carrie-Anne Moss in The Matrix
(4, 2),  -- Hugo Weaving in The Matrix
(5, 1),  -- Christian Bale in Inception
(6, 1),  -- Heath Ledger in Inception
(7, 1),  -- Marion Cotillard in Inception
(8, 1),  -- Joseph Gordon-Levitt in Inception
(9, 1),  -- Ellen Page in Inception
(10, 3), -- Leonardo DiCaprio in Interstellar
(11, 3), -- Joseph Gordon-Levitt in Interstellar
(12, 3), -- Tom Hardy in Interstellar
(13, 3), -- Marion Cotillard in Interstellar
(14, 4), -- Matthew McConaughey in Spirited Away
(15, 4), -- Anne Hathaway in Spirited Away
(16, 4), -- Jessica Chastain in Spirited Away
(17, 4), -- Hayao Miyazaki in Spirited Away
(18, 4), -- Rumi Hiiragi in Spirited Away
(19, 5), -- Catherine Deneuve in Casablanca
(20, 5), -- Humphrey Bogart in Casablanca
(21, 5); -- Ingrid Bergman in Casablanca

-- Ingestión de Film-Category (relaciones)
INSERT INTO film_category (film_id, category_id) VALUES
(1, 1),  -- Inception: Action
(1, 10), -- Inception: Sci-Fi
(2, 1),  -- The Matrix: Action
(2, 14), -- The Matrix: Sci-Fi
(3, 1),  -- Interstellar: Action
(3, 14), -- Interstellar: Sci-Fi
(4, 2),  -- Spirited Away: Animation
(4, 6),  -- Spirited Away: Documentary
(4, 8),  -- Spirited Away: Family
(5, 4),  -- Casablanca: Classics
(5, 7);  -- Casablanca: Drama

-- Ingestión de Clientes (Customer)
INSERT INTO customer (store_id, first_name, last_name, email, address_id, create_date) VALUES
(1, 'Juan', 'Perez', 'juan.perez@email.com', 1, '2026-01-15 10:00:00'),
(1, 'Maria', 'Rodriguez', 'maria.rodriguez@email.com', 1, '2026-02-20 14:30:00'),
(2, 'Carlos', 'Santana', 'carlos.santana@email.com', 3, '2026-03-10 09:15:00'),
(2, 'Ana', 'Gomez', 'ana.gomez@email.com', 4, '2026-04-05 16:45:00');

-- Ingestión de Alquileres (Rental)
INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id) VALUES
('2026-05-01 09:00:00', 1, 1, '2026-05-03 09:00:00', 1),
('2026-05-02 10:30:00', 2, 1, '2026-05-04 10:30:00', 1),
('2026-05-03 14:00:00', 3, 2, '2026-05-05 14:00:00', 2),
('2026-05-04 11:15:00', 4, 3, NULL, 3),
('2026-05-05 16:00:00', 5, 4, '2026-05-07 16:00:00', 4);

-- Ingestión de Pagos (Payment)
INSERT INTO payment (customer_id, staff_id, rental_id, amount, payment_date) VALUES
(1, 1, 1, 4.99, '2026-05-01 09:00:00'),
(1, 1, 2, 3.99, '2026-05-02 10:30:00'),
(2, 2, 3, 2.99, '2026-05-03 14:00:00'),
(3, 3, 4, 4.99, '2026-05-04 11:15:00'),
(4, 4, 5, 1.99, '2026-05-05 16:00:00');

-- Ingestión de Film Text (búsqueda full-text)
INSERT INTO film_text (film_id, title, description) VALUES
(1, 'Inception', 'A thief who steals corporate secrets through use of dream-sharing.'),
(2, 'The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality.'),
(3, 'Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.'),
(4, 'Spirited Away', 'During her family move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods.'),
(5, 'Casablanca', 'A cynical expatriate American cafe owner struggles to decide whether or not to help his former lover.');
