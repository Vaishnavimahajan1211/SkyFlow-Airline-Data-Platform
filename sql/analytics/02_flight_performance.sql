USE skyflow_db;

-- 1. Flight status summary
SELECT
    flight_status,
    COUNT(*) AS flight_count
FROM Flight
GROUP BY flight_status
ORDER BY flight_count DESC;


-- 2. Average delay by status
SELECT
    flight_status,
    COUNT(*) AS flights,
    ROUND(AVG(delay_minutes), 2) AS avg_delay_minutes,
    MAX(delay_minutes) AS max_delay_minutes
FROM Flight
GROUP BY flight_status
ORDER BY avg_delay_minutes DESC;


-- 3. Completed flights
SELECT
    COUNT(*) AS completed_flights
FROM Flight
WHERE flight_status IN ('LANDED', 'DEPARTED');


-- 4. Flights with delay
SELECT
    COUNT(*) AS delayed_flights,
    ROUND(AVG(delay_minutes), 2) AS avg_delay,
    MAX(delay_minutes) AS maximum_delay
FROM Flight
WHERE delay_minutes > 0;


-- 5. Top 10 delayed flights
SELECT
    flight_id,
    flight_number,
    route_id,
    aircraft_id,
    flight_status,
    delay_minutes
FROM Flight
ORDER BY delay_minutes DESC
LIMIT 10;