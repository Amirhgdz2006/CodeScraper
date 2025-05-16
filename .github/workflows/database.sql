CREATE DATABASE codescraper;

USE codescraper;

CREATE TABLE melkradar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    area INT,
    built_year INT,
    room INT,
    floor INT,
    max_floor INT,
    sale BOOLEAN,
    rent BOOLEAN,
    elevator BOOLEAN,
    parking BOOLEAN,
    storage_room BOOLEAN,
    image_link TEXT,
    location TEXT,
    rent_price BIGINT,
    deposit_price BIGINT,
    UNIQUE KEY unique_property (title, area, location(255)),
    INDEX idx_area (area),
    INDEX idx_location (location(255))
);

CREATE TABLE divar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    area INT,
    built_year INT,
    room INT,
    floor INT,
    max_floor INT,
    sale BOOLEAN,
    rent BOOLEAN,
    elevator BOOLEAN,
    parking BOOLEAN,
    storage_room BOOLEAN,
    image_link TEXT,
    location TEXT,
    rent_price BIGINT,
    deposit_price BIGINT,
    UNIQUE KEY unique_property (title, area, location(255)),
    INDEX idx_area (area),
    INDEX idx_location (location(255))
);

ALTER TABLE melkradar
ADD sale_price BIGINT,
ADD price_per_m2 BIGINT;

ALTER TABLE divar
ADD sale_price BIGINT,
ADD price_per_m2 BIGINT;
