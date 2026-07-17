-- =====================================================
-- TABLE: airport
-- =====================================================
CREATE TABLE airport (

    airport_id INT AUTO_INCREMENT PRIMARY KEY,

    airport_code CHAR(3) NOT NULL UNIQUE,
    airport_name VARCHAR(100) NOT NULL,

    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,

    timezone VARCHAR(50),

    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),

    airport_type ENUM('Domestic','International') DEFAULT 'International',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
DESCRIBE airport;
select* from airport;

-- =====================================================
-- TABLE: aircraft
-- =====================================================

CREATE TABLE aircraft (

    aircraft_id INT AUTO_INCREMENT PRIMARY KEY,

    aircraft_code VARCHAR(20) NOT NULL UNIQUE,

    manufacturer VARCHAR(50) NOT NULL,

    model VARCHAR(50) NOT NULL,

    aircraft_type ENUM('Passenger','Cargo') DEFAULT 'Passenger',

    seating_capacity INT NOT NULL,

    manufacturing_year YEAR,

    current_airport_id INT,

    status ENUM('Active','Maintenance','Retired') DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_aircraft_airport
        FOREIGN KEY (current_airport_id)
        REFERENCES airport(airport_id)

);
DESCRIBE aircraft;
select* from aircraft;

-- =====================================================
-- TABLE: passenger
-- =====================================================

CREATE TABLE passenger (

    passenger_id INT AUTO_INCREMENT PRIMARY KEY,

    passenger_code VARCHAR(20) NOT NULL UNIQUE,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    gender ENUM('Male','Female','Other'),

    date_of_birth DATE,

    nationality VARCHAR(50),

    passport_number VARCHAR(20) UNIQUE,

    passport_expiry DATE,

    email VARCHAR(100) UNIQUE,

    phone_number VARCHAR(20),

    address VARCHAR(255),

    city VARCHAR(100),

    country VARCHAR(100),

    emergency_contact_name VARCHAR(100),

    emergency_contact_phone VARCHAR(20),

    meal_preference ENUM('Veg','Non-Veg','Vegan','Jain'),

    account_status ENUM('Active','Inactive') DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

DESCRIBE passenger;
select * from passenger;

-- =====================================================
-- TABLE: crew
-- =====================================================

CREATE TABLE crew (

    crew_id INT AUTO_INCREMENT PRIMARY KEY,

    crew_code VARCHAR(20) NOT NULL UNIQUE,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    role ENUM('Pilot','Co-Pilot','Cabin Crew','Engineer') NOT NULL,

    license_number VARCHAR(50) UNIQUE,

    experience_years INT,

    nationality VARCHAR(50),

    joining_date DATE,

    status ENUM('Active','On Leave','Retired') DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
-- =====================================================
-- TABLE: route
-- =====================================================

CREATE TABLE route (

    route_id INT AUTO_INCREMENT PRIMARY KEY,

    route_code VARCHAR(20) NOT NULL UNIQUE,

    source_airport_id INT NOT NULL,

    destination_airport_id INT NOT NULL,

    distance_km DECIMAL(8,2),

    estimated_duration_minutes INT,

    route_status ENUM('Active','Inactive') DEFAULT 'Active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_route_source
        FOREIGN KEY (source_airport_id)
        REFERENCES airport(airport_id),

    CONSTRAINT fk_route_destination
        FOREIGN KEY (destination_airport_id)
        REFERENCES airport(airport_id)

);

-- =====================================================
-- TABLE: loyalty_program
-- =====================================================

CREATE TABLE loyalty_program (

    loyalty_id INT AUTO_INCREMENT PRIMARY KEY,

    passenger_id INT NOT NULL,

    membership_number VARCHAR(30) UNIQUE,

    membership_level ENUM('Silver','Gold','Platinum') DEFAULT 'Silver',

    total_points INT DEFAULT 0,

    joining_date DATE,

    expiry_date DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_loyalty_passenger
        FOREIGN KEY (passenger_id)
        REFERENCES passenger(passenger_id)

);
