USE skyflow_db;

-- 1. Route flight volume
SELECT
    r.route_id,
    r.source_airport,
    r.destination_airport,
    COUNT(f.flight_id) AS total_flights
FROM Route r
LEFT JOIN Flight f
    ON r.route_id = f.route_id
GROUP BY
    r.route_id,
    r.source_airport,
    r.destination_airport
ORDER BY total_flights DESC;


-- 2. Route delay performance
SELECT
    r.route_id,
    r.source_airport,
    r.destination_airport,
    COUNT(f.flight_id) AS total_flights,
    ROUND(AVG(f.delay_minutes), 2) AS avg_delay,
    MAX(f.delay_minutes) AS max_delay
FROM Route r
JOIN Flight f
    ON r.route_id = f.route_id
GROUP BY
    r.route_id,
    r.source_airport,
    r.destination_airport
ORDER BY avg_delay DESC;


-- 3. International vs domestic
SELECT
    r.route_type,
    COUNT(f.flight_id) AS total_flights,
    ROUND(AVG(f.delay_minutes), 2) AS avg_delay
FROM Route r
JOIN Flight f
    ON r.route_id = f.route_id
GROUP BY r.route_type;


-- 4. Top revenue routes
SELECT
    r.route_id,
    r.source_airport,
    r.destination_airport,
    COUNT(b.booking_id) AS bookings,
    ROUND(SUM(b.final_amount), 2) AS revenue
FROM Route r
JOIN Flight f
    ON r.route_id = f.route_id
JOIN Booking b
    ON f.flight_id = b.flight_id
WHERE b.booking_status <> 'CANCELLED'
GROUP BY
    r.route_id,
    r.source_airport,
    r.destination_airport
ORDER BY revenue DESC
LIMIT 10;