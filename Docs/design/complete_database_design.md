
# SkyFlow – Enterprise Airline Data Platform

# Complete Database Architecture & SQL Design

---

# Database Name

skyflow_db

---

# Database Modules

## Module 1 – Master Tables

1. Airport
2. Aircraft
3. Passenger
4. Crew
5. Route
6. Loyalty Program

---

## Module 2 – Operational Tables

7. Flight
8. Booking
9. Payment
10. Baggage
11. Weather
12. Flight Status

---

## Module 3 – Business Tables

13. Maintenance
14. Fuel Consumption
15. Customer Feedback

---

# Complete Database Architecture

```
                           AIRPORT
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
             WEATHER                   ROUTE
                                            │
                                            ▼
                                        FLIGHT
                          ┌─────────────┼──────────────┐
                          │             │              │
                          ▼             ▼              ▼
                     AIRCRAFT        CREW         FLIGHT_STATUS
                          │
                          ▼
                    MAINTENANCE

FLIGHT
   │
   ▼
BOOKING
   ├──────────────┐
   │              │
   ▼              ▼
PAYMENT        BAGGAGE
   │
   ▼
CUSTOMER_FEEDBACK

PASSENGER
   ├──────────────┐
   │              │
   ▼              ▼
BOOKING     LOYALTY_PROGRAM
       │
       ▼
CUSTOMER_FEEDBACK

FLIGHT
   │
   ▼
FUEL_CONSUMPTION
```

---

# Table Relationships

## AIRPORT

Referenced By

- Route
- Weather

---

## AIRCRAFT

Referenced By

- Flight
- Maintenance

---

## PASSENGER

Referenced By

- Booking
- Loyalty Program
- Customer Feedback

---

## CREW

Referenced By

- Flight

---

## ROUTE

Referenced By

- Flight

---

## LOYALTY PROGRAM

Belongs To

- Passenger

---

## FLIGHT

References

- Route
- Aircraft
- Crew

Referenced By

- Booking
- Flight Status
- Fuel Consumption

---

## BOOKING

References

- Passenger
- Flight

Referenced By

- Payment
- Baggage
- Customer Feedback

---

## PAYMENT

References

- Booking

---

## BAGGAGE

References

- Booking

---

## WEATHER

References

- Airport

---

## FLIGHT STATUS

References

- Flight

---

## MAINTENANCE

References

- Aircraft

---

## FUEL CONSUMPTION

References

- Flight

---

## CUSTOMER FEEDBACK

References

- Passenger
- Booking

---

# Foreign Key Mapping

```
Route
    ├── airport_id (Source)
    └── airport_id (Destination)

Weather
    └── airport_id

Flight
    ├── aircraft_id
    ├── route_id
    └── pilot_id

Booking
    ├── passenger_id
    └── flight_id

Payment
    └── booking_id

Baggage
    └── booking_id

Flight_Status
    └── flight_id

Maintenance
    └── aircraft_id

Fuel_Consumption
    └── flight_id

Customer_Feedback
    ├── booking_id
    └── passenger_id

Loyalty_Program
    └── passenger_id
```

---

# Database Flow

```
Passenger
      │
      ▼
Booking
      │
      ├────────► Payment
      │
      ├────────► Baggage
      │
      └────────► Customer Feedback


Airport
      │
      ▼
Route
      │
      ▼
Flight
      │
      ├────────► Flight Status
      │
      └────────► Fuel Consumption


Aircraft
      │
      ├────────► Flight
      │
      └────────► Maintenance


Crew
      │
      ▼
Flight


Passenger
      │
      ▼
Loyalty Program


Airport
      │
      ▼
Weather
```

---

# Total Database Summary

| Module | Tables |
|---------|--------|
| Master Tables | 6 |
| Operational Tables | 6 |
| Business Tables | 3 |

---

# Total Tables

15

---

# Database Technology

- MySQL
- SQL

---

# Database Purpose

- Airline Reservation Management
- Passenger Management
- Flight Management
- Airport Management
- Crew Management
- Revenue Tracking
- Payment Management
- Baggage Tracking
- Maintenance Management
- Weather Monitoring
- Fuel Analytics
- Customer Feedback Analysis

---

# Next Phase

Python Data Generator

↓

Pandas Validation

↓

Databricks + PySpark

↓

Parquet Files

↓

MySQL Analytics

↓

Power BI Dashboard