USE skyflow_db;

-- 1. Passenger booking activity
SELECT
    p.passenger_id,
    CONCAT(p.first_name, ' ', p.last_name) AS passenger_name,
    p.nationality,
    COUNT(b.booking_id) AS total_bookings,
    ROUND(SUM(b.final_amount), 2) AS total_spend
FROM Passenger p
JOIN Booking b
    ON p.passenger_id = b.passenger_id
WHERE b.booking_status <> 'CANCELLED'
GROUP BY
    p.passenger_id,
    p.first_name,
    p.last_name,
    p.nationality
ORDER BY total_spend DESC
LIMIT 20;


-- 2. Revenue by nationality
SELECT
    p.nationality,
    COUNT(DISTINCT p.passenger_id) AS passengers,
    COUNT(b.booking_id) AS bookings,
    ROUND(SUM(b.final_amount), 2) AS revenue
FROM Passenger p
JOIN Booking b
    ON p.passenger_id = b.passenger_id
WHERE b.booking_status <> 'CANCELLED'
GROUP BY p.nationality
ORDER BY revenue DESC;


-- 3. Repeat passengers
SELECT
    p.passenger_id,
    CONCAT(p.first_name, ' ', p.last_name) AS passenger_name,
    COUNT(b.booking_id) AS booking_count
FROM Passenger p
JOIN Booking b
    ON p.passenger_id = b.passenger_id
WHERE b.booking_status <> 'CANCELLED'
GROUP BY
    p.passenger_id,
    p.first_name,
    p.last_name
HAVING COUNT(b.booking_id) > 1
ORDER BY booking_count DESC;


-- 4. Passenger segment
SELECT
    CASE
        WHEN booking_count = 1 THEN 'One-Time'
        WHEN booking_count BETWEEN 2 AND 4 THEN 'Regular'
        ELSE 'Frequent'
    END AS passenger_segment,
    COUNT(*) AS passenger_count
FROM (
    SELECT
        passenger_id,
        COUNT(*) AS booking_count
    FROM Booking
    WHERE booking_status <> 'CANCELLED'
    GROUP BY passenger_id
) x
GROUP BY passenger_segment;