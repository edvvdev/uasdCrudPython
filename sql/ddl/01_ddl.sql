-- =====================================================================
-- MAESTRÍA EN CIENCIA DE DATOS E INTELIGENCIA ARTIFICIAL
-- FASE I: DDL - DATA DEFINITION LANGUAGE
-- CREACIÓN DE ESTRUCTURAS CON RESTRICCIONES DE INTEGRIDAD
-- =====================================================================

-- Tabla de Países (Country)
CREATE TABLE country (
    country_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    country VARCHAR(50) NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (country_id),
    CONSTRAINT unique_country UNIQUE (country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de Ciudades (City)
CREATE TABLE city (
    city_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    city VARCHAR(50) NOT NULL,
    country_id SMALLINT UNSIGNED NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (city_id),
    CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT unique_city_country UNIQUE (city, country_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de Películas (Film)
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
    CONSTRAINT unique_title_release UNIQUE (title, release_year)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla de Inventario (Inventory)
CREATE TABLE inventory (
    inventory_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
    film_id SMALLINT UNSIGNED NOT NULL,
    store_id TINYINT UNSIGNED NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (inventory_id),
    CONSTRAINT fk_inventory_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;