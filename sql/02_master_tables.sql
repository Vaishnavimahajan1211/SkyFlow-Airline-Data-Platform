USE skyflow_db;

-- =====================================================
-- AIRPORT
-- =====================================================


CREATE TABLE airport (

    airport_code VARCHAR(10) PRIMARY KEY,

    airport_name VARCHAR(150) NOT NULL,

    city VARCHAR(100) NOT NULL,

    country VARCHAR(100) NOT NULL,

    timezone VARCHAR(100) NOT NULL

);

-- =====================================================
-- AIRCRAFT
-- =====================================================

CREATE TABLE aircraft (

    aircraft_id VARCHAR(10) PRIMARY KEY,

    aircraft_code VARCHAR(20) UNIQUE NOT NULL,

    manufacturer VARCHAR(100) NOT NULL,

    model VARCHAR(100) NOT NULL,

    capacity INT NOT NULL,

    manufacturing_year INT,

    status VARCHAR(30)

);

-- =====================================================
-- PASSENGER
-- =====================================================

CREATE TABLE passenger (

    passenger_id VARCHAR(10) PRIMARY KEY,

    first_name VARCHAR(50),

    last_name VARCHAR(50),

    gender VARCHAR(20),

    date_of_birth DATE,

    email VARCHAR(100),

    phone BIGINT,

    passport_number VARCHAR(30),

    nationality VARCHAR(50)

);

-- =====================================================
-- ROUTE
-- =====================================================

CREATE TABLE route (

    route_id VARCHAR(10) PRIMARY KEY,

    source_airport VARCHAR(10) NOT NULL,

    destination_airport VARCHAR(10) NOT NULL,

    route_type VARCHAR(30),

    distance_km INT,

    duration_minutes INT,

    fuel_estimate_liters DECIMAL(10,2),

    CONSTRAINT fk_route_source
        FOREIGN KEY (source_airport)
        REFERENCES airport(airport_code),

    CONSTRAINT fk_route_destination
        FOREIGN KEY (destination_airport)
        REFERENCES airport(airport_code)

);

SHOW TABLES;