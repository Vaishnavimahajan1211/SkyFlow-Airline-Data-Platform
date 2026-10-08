# ✈️ SkyFlow — Enterprise Airline Data Platform

An end-to-end data engineering project that simulates an airline's data ecosystem, from relational source data and ETL processing to analytics-ready datasets and business intelligence metrics.

## Project Overview

SkyFlow processes airline data related to passengers, bookings, flights, airports, aircraft, routes, and payments. It transforms source data into structured Bronze, Silver, and Gold layers and uses Databricks and PySpark to generate reusable business analytics.

## Architecture

**MySQL → Python ETL → Bronze → Silver → Gold → Databricks → Delta Analytics Tables**

## Technology Stack

* **Database:** MySQL
* **Programming:** Python, Pandas
* **Big Data Processing:** Apache Spark, PySpark
* **Analytics Platform:** Databricks
* **Storage and Analytics:** CSV datasets, Delta tables, SQL
* **Version Control:** Git and GitHub

## Implemented Features

### Data Engineering Pipeline

* Relational airline database with passenger, booking, flight, airport, aircraft, route, and payment data.
* Python-based data generation and processing.
* Bronze, Silver, and Gold data layers.
* PySpark transformations for Gold dimension and fact datasets.

### Gold Data Layer

| Dataset         |    Records |
| --------------- | ---------: |
| `dim_passenger` |      1,000 |
| `dim_airport`   |         50 |
| `dim_aircraft`  |         50 |
| `dim_route`     |        100 |
| `fact_booking`  |      5,000 |
| `fact_flight`   |        200 |
| `fact_payment`  |      5,000 |
| **Total**       | **11,400** |

### Data Quality

* 52 validation checks passed.
* Primary-key null and duplicate checks.
* Foreign-key integrity checks.
* Booking amount and flight-delay business rules.

### Databricks Business Analytics

The Gold datasets are loaded into Databricks and used to generate five persisted Delta analytics tables:

* `workspace.default.skyflow_booking_kpis`
* `workspace.default.skyflow_flight_kpis`
* `workspace.default.skyflow_payment_kpis`
* `workspace.default.skyflow_route_revenue`
* `workspace.default.skyflow_flight_performance`

These tables support analysis of booking status, confirmed booking revenue, payment amounts, route revenue, and flight delays.

## Repository Structure

```text
SkyFlow-Airline-Data-Platform/
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docs/
│   ├── design/
│   └── screenshots/
├── python/
│   ├── config/
│   ├── generators/
│   ├── loaders/
│   ├── pipeline/
│   ├── quality/
│   ├── spark/
│   └── utils/
└── sql/
    └── analytics/
```

## Project Status

**Current status: Core batch pipeline and Databricks analytics implemented.**

Future enhancements may include automated orchestration, streaming ingestion, and dashboard integration.

## Business Value

SkyFlow demonstrates how an airline can organize operational data, validate data quality, and derive metrics that support revenue analysis and flight-performance monitoring.
