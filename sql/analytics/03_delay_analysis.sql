USE skyflow_db;

-- 1. Overall delay KPI
SELECT
    COUNT(*) AS total_flights,
    SUM(CASE WHEN delay_minutes > 0 THEN 1 ELSE 0 END)
        AS delayed_flights,
    ROUND(
        100.0 * SUM(CASE WHEN delay_minutes > 0 THEN 1 ELSE 0 END)
        / COUNT(*),
        2
    ) AS delay_rate_percent,
    ROUND(AVG(delay_minutes), 2) AS average_delay
FROM Flight;


-- 2. Delay by flight status
SELECT
    flight_status,
    COUNT(*) AS flights,
    ROUND(AVG(delay_minutes), 2) AS avg_delay,
    MAX(delay_minutes) AS max_delay
FROM Flight
GROUP BY flight_status
ORDER BY avg_delay DESC;


-- 3. Severe delays
SELECT
    flight_id,
    flight_number,
    delay_minutes,
    flight_status
FROM Flight
WHERE delay_minutes >= 60
ORDER BY delay_minutes DESC;


-- 4. Delay buckets
SELECT
    CASE
        WHEN delay_minutes = 0 THEN 'On Time'
        WHEN delay_minutes BETWEEN 1 AND 30 THEN '1-30 Minutes'
        WHEN delay_minutes BETWEEN 31 AND 60 THEN '31-60 Minutes'
        WHEN delay_minutes BETWEEN 61 AND 120 THEN '61-120 Minutes'
        ELSE '120+ Minutes'
    END AS delay_bucket,
    COUNT(*) AS flight_count
FROM Flight
GROUP BY delay_bucket
ORDER BY flight_count DESC;