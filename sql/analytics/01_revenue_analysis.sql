USE skyflow_db;

-- =========================================================
-- SKYFLOW - REVENUE ANALYSIS
-- =========================================================

-- 1. Total booking revenue
SELECT
    COUNT(*) AS total_bookings,
    ROUND(SUM(final_amount), 2) AS total_revenue,
    ROUND(AVG(final_amount), 2) AS average_booking_value
FROM Booking
WHERE booking_status <> 'CANCELLED';


-- 2. Revenue by seat class
SELECT
    seat_class,
    COUNT(*) AS total_bookings,
    ROUND(SUM(final_amount), 2) AS total_revenue,
    ROUND(AVG(final_amount), 2) AS average_booking_value
FROM Booking
WHERE booking_status <> 'CANCELLED'
GROUP BY seat_class
ORDER BY total_revenue DESC;


-- 3. Revenue by booking status
SELECT
    booking_status,
    COUNT(*) AS booking_count,
    ROUND(SUM(final_amount), 2) AS total_revenue
FROM Booking
GROUP BY booking_status
ORDER BY total_revenue DESC;


-- 4. Revenue by payment status
SELECT
    payment_status,
    COUNT(*) AS booking_count,
    ROUND(SUM(final_amount), 2) AS total_amount
FROM Booking
GROUP BY payment_status
ORDER BY total_amount DESC;


-- 5. Monthly revenue
SELECT
    DATE_FORMAT(booking_date, '%Y-%m') AS booking_month,
    COUNT(*) AS total_bookings,
    ROUND(SUM(final_amount), 2) AS monthly_revenue
FROM Booking
WHERE booking_status <> 'CANCELLED'
GROUP BY DATE_FORMAT(booking_date, '%Y-%m')
ORDER BY booking_month;


-- 6. Discount impact
SELECT
    ROUND(SUM(ticket_price), 2) AS gross_ticket_value,
    ROUND(SUM(discount), 2) AS total_discount,
    ROUND(SUM(tax), 2) AS total_tax,
    ROUND(SUM(final_amount), 2) AS final_revenue
FROM Booking
WHERE booking_status <> 'CANCELLED';


-- 7. Top 10 highest-value bookings
SELECT
    booking_id,
    passenger_id,
    flight_id,
    seat_class,
    booking_status,
    final_amount
FROM Booking
WHERE booking_status <> 'CANCELLED'
ORDER BY final_amount DESC
LIMIT 10;