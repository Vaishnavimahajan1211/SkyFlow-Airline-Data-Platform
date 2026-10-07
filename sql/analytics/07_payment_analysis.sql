USE skyflow_db;

-- 1. Payment status
SELECT
    payment_status,
    COUNT(*) AS payment_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM Payment
GROUP BY payment_status
ORDER BY total_amount DESC;


-- 2. Payment method performance
SELECT
    payment_method,
    COUNT(*) AS transactions,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS average_transaction
FROM Payment
GROUP BY payment_method
ORDER BY total_amount DESC;


-- 3. Successful payment revenue
SELECT
    COUNT(*) AS successful_transactions,
    ROUND(SUM(amount), 2) AS successful_revenue
FROM Payment
WHERE payment_status = 'SUCCESS';


-- 4. Failed payments
SELECT
    COUNT(*) AS failed_transactions,
    ROUND(SUM(amount), 2) AS failed_amount
FROM Payment
WHERE payment_status = 'FAILED';


-- 5. Payment vs booking revenue
SELECT
    COUNT(DISTINCT b.booking_id) AS bookings,
    ROUND(SUM(b.final_amount), 2) AS booking_revenue,
    ROUND(SUM(p.amount), 2) AS payment_amount
FROM Booking b
JOIN Payment p
    ON b.booking_id = p.booking_id;