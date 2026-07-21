USE skyflow_db;

-- =====================================================
-- FLIGHT
-- =====================================================

CREATE TABLE flight (

    flight_id VARCHAR(10) PRIMARY KEY,

    flight_number VARCHAR(20) UNIQUE NOT NULL,

    route_id VARCHAR(10) NOT NULL,

    aircraft_id VARCHAR(10) NOT NULL,

    departure_datetime DATETIME NOT NULL,

    arrival_datetime DATETIME NOT NULL,

    flight_status VARCHAR(30),

    terminal VARCHAR(10),

    gate_number VARCHAR(10),

    delay_minutes INT,

    CONSTRAINT fk_flight_route
        FOREIGN KEY (route_id)
        REFERENCES route(route_id),

    CONSTRAINT fk_flight_aircraft
        FOREIGN KEY (aircraft_id)
        REFERENCES aircraft(aircraft_id)

);

-- =====================================================
-- BOOKING
-- =====================================================

CREATE TABLE booking (

    booking_id VARCHAR(10) PRIMARY KEY,

    passenger_id VARCHAR(10) NOT NULL,

    flight_id VARCHAR(10) NOT NULL,

    booking_date DATETIME,

    seat_class VARCHAR(30),

    booking_status VARCHAR(30),

    ticket_price DECIMAL(10,2),

    tax DECIMAL(10,2),

    discount DECIMAL(10,2),

    final_amount DECIMAL(10,2),

    payment_status VARCHAR(30),

    CONSTRAINT fk_booking_passenger
        FOREIGN KEY (passenger_id)
        REFERENCES passenger(passenger_id),

    CONSTRAINT fk_booking_flight
        FOREIGN KEY (flight_id)
        REFERENCES flight(flight_id)

);

USE skyflow_db;

CREATE TABLE payment (

    payment_id VARCHAR(10) PRIMARY KEY,

    booking_id VARCHAR(10) NOT NULL,

    payment_date DATETIME,

    payment_method VARCHAR(30),

    payment_status VARCHAR(20),

    amount DECIMAL(10,2),

    transaction_id VARCHAR(50),

    FOREIGN KEY (booking_id)
        REFERENCES booking(booking_id)

);

ALTER TABLE payment
DROP COLUMN transaction_id;

show tables;
