USE skyflow_db;

SELECT
    -- Booking KPIs
    (
        SELECT COUNT(*)
        FROM Booking
    ) AS total_bookings,

    (
        SELECT COUNT(*)
        FROM Booking
        WHERE booking_status <> 'CANCELLED'
    ) AS active_bookings,

    (
        SELECT ROUND(SUM(final_amount), 2)
        FROM Booking
        WHERE booking_status <> 'CANCELLED'
    ) AS total_revenue,

    (
        SELECT ROUND(AVG(final_amount), 2)
        FROM Booking
        WHERE booking_status <> 'CANCELLED'
    ) AS average_booking_value,

    -- Flight KPIs
    (
        SELECT COUNT(*)
        FROM Flight
    ) AS total_flights,

    (
        SELECT COUNT(*)
        FROM Flight
        WHERE flight_status = 'CANCELLED'
    ) AS cancelled_flights,

    (
        SELECT ROUND(AVG(delay_minutes), 2)
        FROM Flight
    ) AS average_delay_minutes,

    (
        SELECT COUNT(*)
        FROM Flight
        WHERE delay_minutes > 0
    ) AS delayed_flights,

    -- Passenger KPI
    (
        SELECT COUNT(*)
        FROM Passenger
    ) AS total_passengers,

    -- Payment KPI
    (
        SELECT ROUND(SUM(amount), 2)
        FROM Payment
        WHERE payment_status = 'SUCCESS'
    ) AS successful_payment_value;