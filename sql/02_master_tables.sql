

USE skyflow_db;

CREATE TABLE airport (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    airport_code CHAR(3) NOT NULL UNIQUE,
    airport_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    timezone VARCHAR(50),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select* from Airport; 


CREATE TABLE aircraft (
    aircraft_id INT AUTO_INCREMENT PRIMARY KEY,
    aircraft_code VARCHAR(20) NOT NULL UNIQUE,
    manufacturer VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    manufacturing_year YEAR,
    airline_name VARCHAR(100),
    status ENUM('Active','Maintenance','Retired') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE passenger (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_code VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender ENUM('Male','Female','Other'),
    date_of_birth DATE,
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    passport_number VARCHAR(30) UNIQUE,
    nationality VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
