# SkyFlow Enterprise Airline Data Platform

## Master Tables

### 1. airport
- airport_id (PK)
- airport_code
- airport_name
- city
- state
- country
- timezone
- latitude
- longitude
- created_at

### 2. aircraft
- aircraft_id (PK)
- aircraft_code
- manufacturer
- model
- capacity
- manufacturing_year
- airline_name
- status
- created_at

### 3. passenger
- passenger_id (PK)
- passenger_code
- first_name
- last_name
- gender
- date_of_birth
- email
- phone_number
- passport_number
- nationality
- created_at

### 4. crew
- crew_id (PK)
- crew_code
- first_name
- last_name
- role
- experience_years
- nationality
- status

### 5. loyalty_program
- loyalty_id (PK)
- passenger_id (FK)
- membership_level
- total_points

### 6. route
- route_id (PK)
- route_code
- source_airport_id (FK)
- destination_airport_id (FK)
- distance_km
- estimated_duration_minutes

---

## Operational Tables

### 7. flight
- flight_id (PK)
- flight_code
- aircraft_id (FK)
- route_id (FK)
- departure_time
- arrival_time
- flight_status

### 8. booking
- booking_id (PK)
- booking_code
- passenger_id (FK)
- flight_id (FK)
- booking_date
- booking_status

### 9. payment
- payment_id (PK)
- booking_id (FK)
- amount
- payment_method
- payment_status

### 10. baggage
- baggage_id (PK)
- booking_id (FK)
- baggage_weight
- baggage_type

### 11. weather
- weather_id (PK)
- airport_id (FK)
- temperature
- weather_condition
- wind_speed

### 12. flight_status
- status_id (PK)
- flight_id (FK)
- status
- delay_minutes

---

## Business Tables

### 13. maintenance
- maintenance_id (PK)
- aircraft_id (FK)
- maintenance_date
- maintenance_type
- engineer_name

### 14. fuel_consumption
- fuel_id (PK)
- flight_id (FK)
- fuel_used_liters
- fuel_cost

### 15. customer_feedback
- feedback_id (PK)
- booking_id (FK)
- rating
- comments