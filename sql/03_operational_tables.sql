USE skyflow_db;

-- =====================================================
-- TABLE: flight
-- =====================================================

CREATE TABLE flight (

    flight_id INT AUTO_INCREMENT PRIMARY KEY,

    flight_number VARCHAR(20) NOT NULL UNIQUE,

    aircraft_id INT NOT NULL,

    route_id INT NOT NULL,

    pilot_id INT NOT NULL,

    scheduled_departure DATETIME NOT NULL,

    actual_departure DATETIME,

    scheduled_arrival DATETIME NOT NULL,

    actual_arrival DATETIME,

    flight_status ENUM(
        'Scheduled',
        'Boarding',
        'Departed',
        'Delayed',
        'Cancelled',
        'Arrived'
    ) DEFAULT 'Scheduled',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_flight_aircraft
        FOREIGN KEY (aircraft_id)
        REFERENCES aircraft(aircraft_id),

    CONSTRAINT fk_flight_route
        FOREIGN KEY (route_id)
        REFERENCES route(route_id),

    CONSTRAINT fk_flight_pilot
        FOREIGN KEY (pilot_id)
        REFERENCES crew(crew_id)

);
DESCRIBE flight;

-- =====================================================
-- TABLE: booking
-- =====================================================

CREATE TABLE booking (

    booking_id INT AUTO_INCREMENT PRIMARY KEY,

    booking_reference VARCHAR(20) NOT NULL UNIQUE,

    passenger_id INT NOT NULL,

    flight_id INT NOT NULL,

    booking_date DATETIME NOT NULL,

    travel_class ENUM('Economy','Premium Economy','Business','First') NOT NULL,

    seat_number VARCHAR(10),

    ticket_price DECIMAL(10,2) NOT NULL,

    booking_status ENUM(
        'Confirmed',
        'Cancelled',
        'Pending'
    ) DEFAULT 'Confirmed',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_booking_passenger
        FOREIGN KEY (passenger_id)
        REFERENCES passenger(passenger_id),

    CONSTRAINT fk_booking_flight
        FOREIGN KEY (flight_id)
        REFERENCES flight(flight_id)

);
-- =====================================================
-- TABLE: payment
-- =====================================================

CREATE TABLE payment (

    payment_id INT AUTO_INCREMENT PRIMARY KEY,

    booking_id INT NOT NULL,

    payment_method ENUM(
        'Credit Card',
        'Debit Card',
        'UPI',
        'Net Banking',
        'Wallet'
    ),

    transaction_id VARCHAR(100) UNIQUE,

    amount DECIMAL(10,2) NOT NULL,

    payment_date DATETIME,

    payment_status ENUM(
        'Success',
        'Failed',
        'Refunded'
    ) DEFAULT 'Success',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payment_booking
        FOREIGN KEY (booking_id)
        REFERENCES booking(booking_id)

);
describe flight;

-- =====================================================
-- TABLE: baggage
-- =====================================================

CREATE TABLE baggage (

    baggage_id INT AUTO_INCREMENT PRIMARY KEY,

    booking_id INT NOT NULL,

    baggage_tag VARCHAR(30) UNIQUE,

    baggage_weight DECIMAL(5,2),

    baggage_type ENUM(
        'Cabin',
        'Check-in'
    ),

    baggage_status ENUM(
        'Checked-In',
        'Loaded',
        'In Transit',
        'Delivered',
        'Lost'
    ) DEFAULT 'Checked-In',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_baggage_booking
        FOREIGN KEY (booking_id)
        REFERENCES booking(booking_id)

);
show tables;

-- =====================================================
-- TABLE: weather
-- =====================================================

CREATE TABLE weather (

    weather_id INT AUTO_INCREMENT PRIMARY KEY,

    airport_id INT NOT NULL,

    observation_time DATETIME NOT NULL,

    temperature DECIMAL(5,2),

    humidity DECIMAL(5,2),

    wind_speed DECIMAL(5,2),

    weather_condition VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_weather_airport
        FOREIGN KEY (airport_id)
        REFERENCES airport(airport_id)

);

-- =====================================================
-- TABLE: flight_status
-- =====================================================

CREATE TABLE flight_status (

    status_id INT AUTO_INCREMENT PRIMARY KEY,

    flight_id INT NOT NULL,

    status ENUM(
        'Scheduled',
        'Boarding',
        'Departed',
        'Delayed',
        'Cancelled',
        'Arrived'
    ) NOT NULL,

    updated_at DATETIME NOT NULL,

    remarks VARCHAR(255),

    CONSTRAINT fk_status_flight
        FOREIGN KEY (flight_id)
        REFERENCES flight(flight_id)

);