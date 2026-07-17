-- =====================================================
-- TABLE: maintenance
-- =====================================================

CREATE TABLE maintenance (

    maintenance_id INT AUTO_INCREMENT PRIMARY KEY,

    aircraft_id INT NOT NULL,

    maintenance_type ENUM(
        'Routine',
        'Engine Check',
        'Repair',
        'Inspection'
    ),

    maintenance_date DATE,

    maintenance_cost DECIMAL(12,2),

    status ENUM(
        'Completed',
        'Scheduled',
        'In Progress'
    ) DEFAULT 'Scheduled',

    CONSTRAINT fk_maintenance_aircraft
        FOREIGN KEY (aircraft_id)
        REFERENCES aircraft(aircraft_id)

);

-- =====================================================
-- TABLE: fuel_consumption
-- =====================================================

CREATE TABLE fuel_consumption (

    fuel_id INT AUTO_INCREMENT PRIMARY KEY,

    flight_id INT NOT NULL,

    fuel_used_liters DECIMAL(10,2),

    fuel_cost DECIMAL(12,2),

    recorded_at DATETIME,

    CONSTRAINT fk_fuel_flight
        FOREIGN KEY (flight_id)
        REFERENCES flight(flight_id)

);

-- =====================================================
-- TABLE: customer_feedback
-- =====================================================

CREATE TABLE customer_feedback (

    feedback_id INT AUTO_INCREMENT PRIMARY KEY,

    booking_id INT NOT NULL,

    passenger_id INT NOT NULL,

    rating INT CHECK (rating BETWEEN 1 AND 5),

    comments VARCHAR(500),

    feedback_date DATE,

    CONSTRAINT fk_feedback_booking
        FOREIGN KEY (booking_id)
        REFERENCES booking(booking_id),

    CONSTRAINT fk_feedback_passenger
        FOREIGN KEY (passenger_id)
        REFERENCES passenger(passenger_id)

);

SHOW TABLES;
