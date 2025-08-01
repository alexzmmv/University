-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create cities table
CREATE TABLE cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100) NOT NULL
);

-- Create city connections table (bidirectional)
CREATE TABLE city_connections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_city_id INT NOT NULL,
    to_city_id INT NOT NULL,
    distance INT DEFAULT 0,
    FOREIGN KEY (from_city_id) REFERENCES cities(id),
    FOREIGN KEY (to_city_id) REFERENCES cities(id),
    UNIQUE(from_city_id, to_city_id)
);


-- Insert sample cities
INSERT INTO cities (name, country) VALUES 
('Cluj-Napoca', 'Romania'),
('Bucharest', 'Romania'),
('Budapest', 'Hungary'),
('Vienna', 'Austria'),
('Prague', 'Czech Republic'),
('Warsaw', 'Poland'),
('Berlin', 'Germany'),
('Munich', 'Germany'),
('Zurich', 'Switzerland'),
('Milan', 'Italy'),
('Paris', 'France'),
('Amsterdam', 'Netherlands');

INSERT INTO city_connections (from_city_id, to_city_id, distance) VALUES 
-- Cluj-Napoca connections
(1, 2, 450), -- Cluj to Bucharest
(1, 3, 350), -- Cluj to Budapest
(1, 6, 600), -- Cluj to Warsaw

-- Bucharest connections
(2, 1, 450), -- Bucharest to Cluj
(2, 3, 525), -- Bucharest to Budapest
(2, 6, 650), -- Bucharest to Warsaw

-- Budapest connections  
(3, 1, 350), -- Budapest to Cluj
(3, 2, 525), -- Budapest to Bucharest
(3, 4, 243), -- Budapest to Vienna
(3, 5, 525), -- Budapest to Prague
(3, 6, 545), -- Budapest to Warsaw

-- Vienna connections
(4, 3, 243), -- Vienna to Budapest
(4, 5, 300), -- Vienna to Prague
(4, 8, 357), -- Vienna to Munich
(4, 9, 601), -- Vienna to Zurich

-- Prague connections
(5, 3, 525), -- Prague to Budapest
(5, 4, 300), -- Prague to Vienna
(5, 6, 680), -- Prague to Warsaw
(5, 7, 350), -- Prague to Berlin

-- Warsaw connections
(6, 1, 600), -- Warsaw to Cluj
(6, 2, 650), -- Warsaw to Bucharest
(6, 3, 545), -- Warsaw to Budapest
(6, 5, 680), -- Warsaw to Prague
(6, 7, 570), -- Warsaw to Berlin

-- Berlin connections
(7, 5, 350), -- Berlin to Prague
(7, 6, 570), -- Berlin to Warsaw
(7, 8, 585), -- Berlin to Munich
(7, 12, 580), -- Berlin to Amsterdam
(7, 11, 1050), -- Berlin to Paris

-- Munich connections
(8, 4, 357), -- Munich to Vienna
(8, 7, 585), -- Munich to Berlin
(8, 9, 354), -- Munich to Zurich
(8, 10, 572), -- Munich to Milan

-- Zurich connections
(9, 4, 601), -- Zurich to Vienna
(9, 8, 354), -- Zurich to Munich
(9, 10, 279), -- Zurich to Milan
(9, 11, 490), -- Zurich to Paris

-- Milan connections
(10, 8, 572), -- Milan to Munich
(10, 9, 279), -- Milan to Zurich
(10, 11, 851), -- Milan to Paris

-- Paris connections
(11, 7, 1050), -- Paris to Berlin
(11, 9, 490), -- Paris to Zurich
(11, 10, 851), -- Paris to Milan
(11, 12, 430), -- Paris to Amsterdam

-- Amsterdam connections
(12, 7, 580), -- Amsterdam to Berlin
(12, 11, 430); -- Amsterdam to Paris
