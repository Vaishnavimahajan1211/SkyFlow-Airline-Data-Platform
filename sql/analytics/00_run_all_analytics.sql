USE skyflow_db;

SELECT 'SKYFLOW ANALYTICS STARTED' AS status;

SELECT
    COUNT(*) AS total_bookings,
    ROUND(SUM(final_amount), 2) AS total_revenue,
    ROUND(AVG(final_amount), 2) AS avg_booking_value
FROM Booking
WHERE booking_status <> 'CANCELLED';


SELECT
    COUNT(*) AS total_flights,
    SUM(flight_status = 'CANCELLED') AS cancelled_flights,
    SUM(delay_minutes > 0) AS delayed_flights,
    ROUND(AVG(delay_minutes), 2) AS avg_delay
FROM Flight;


SELECT
    COUNT(*) AS total_passengers
FROM Passenger;


SELECT
    COUNT(*) AS total_payments,
    ROUND(SUM(amount), 2) AS payment_value
FROM Payment;


SELECT
    r.route_type,
    COUNT(f.flight_id) AS flights,
    ROUND(AVG(f.delay_minutes), 2) AS avg_delay
FROM Route r
JOIN Flight f
    ON r.route_id = f.route_id
GROUP BY r.route_type;


SELECT
    seat_class,
    COUNT(*) AS bookings,
    ROUND(SUM(final_amount), 2) AS revenue
FROM Booking
WHERE booking_status <> 'CANCELLED'
GROUP BY seat_class
ORDER BY revenue DESC;

SELECT 'SKYFLOW ANALYTICS COMPLETED' AS status;