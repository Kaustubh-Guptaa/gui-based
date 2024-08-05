CREATE DATABASE prog1_db;

USE prog1_db;

CREATE TABLE celestial_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50),
    distance DOUBLE,
    magnitude DOUBLE
);

INSERT INTO celestial_data (name, type, distance, magnitude) 
VALUES ('Sun', 'Star', 0.0, -26.74),
('Sirius', 'Star', 8.6, -1.46),
('Alpha Centauri', 'Star System', 4.37, -0.27),
('Betelgeuse', 'Red Supergiant Star', 642.5, 0.42),
('Vega', 'Star', 25.0, 0.03);

delete from celestial_data where id = 7;