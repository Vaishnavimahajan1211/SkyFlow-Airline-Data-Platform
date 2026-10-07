USE skyflow_db;

-- 1. Cancellation KPI
SELECT
    COUNT(*) AS total_flights,
    SUM(CASE WHEN flight_status = 'CANCELLED' THEN 1 ELSE 0 END)
        AS cancelled_flights,
    ROUND(
        100.0 * SUM(CASE WHEN flight_status = 'CANCELLED' THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS cancellation_rate_percent
FROM Flight;


-- 2. Cancelled flights
SELECT
    flight_id,
    flight_number,
    route_id,
    aircraft_id,
    departure_datetime
FROM Flight
WHERE flight_status = 'CANCELLED'
ORDER BY departure_datetime;


-- 3. Booking cancellations
SELECT
    COUNT(*) AS cancelled_bookings,
    ROUND(SUM(final_amount), 2) AS cancelled_booking_value
FROM Booking
WHERE booking_status = 'CANCELLED';


-- 4. Booking status distribution
SELECT
    booking_status,
    COUNT(*) AS booking_count,
    ROUND(SUM(final_amount), 2) AS booking_value
FROM Booking
GROUP BY booking_status
ORDER BY booking_count DESC;