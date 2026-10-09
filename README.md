# SkyFlow — Enterprise Airline Data Platform

An end-to-end data engineering project that transforms airline operational data into analytics-ready datasets using MySQL, Python, Pandas, PySpark, and Databricks.

## Overview

SkyFlow simulates an airline data platform that processes passengers, bookings, flights, airports, aircraft, routes, and payments. It follows a layered data architecture and produces analytical datasets for business reporting and operational insights.

## Architecture

**MySQL → Python ETL → Bronze → Silver → Gold → Databricks → Delta Analytics Tables**

## Technology Stack

* **Database:** MySQL
* **Programming:** Python, SQL
* **Data Processing:** Pandas, Apache Spark, PySpark
* **Analytics Platform:** Databricks
* **Storage Formats:** CSV, Delta tables
* **Version Control:** Git, GitHub

## Key Features

### 1. Data Engineering Pipeline

* Airline-related relational data and Python-based data generation.
* Bronze, Silver, and Gold data-processing layers.
* PySpark transformations for dimension and fact datasets.
* Analytics-ready outputs for downstream business analysis.

### 2. Gold Data Layer

The pipeline generates seven dimension and fact datasets.

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

### 3. Data Quality Validation

* 52 validation checks passed in the tested run.
* Primary-key null and duplicate checks.
* Foreign-key integrity checks.
* Booking amount and flight-delay business-rule checks.

### 4. Databricks Analytics

Five persisted Delta analytics tables have been created and verified:

* `workspace.default.skyflow_booking_kpis`
* `workspace.default.skyflow_flight_kpis`
* `workspace.default.skyflow_payment_kpis`
* `workspace.default.skyflow_route_revenue`
* `workspace.default.skyflow_flight_performance`

These tables support analysis of booking status, confirmed-booking revenue, payment amounts, route revenue, and flight performance.

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
├── sql/
│   └── analytics/
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

* Python
* MySQL and MySQL Workbench
* Git
* A Databricks workspace for the analytics stage

### 1. Clone the Repository

```bash
git clone https://github.com/Vaishnavimahajan1211/SkyFlow-Airline-Data-Platform.git
cd SkyFlow-Airline-Data-Platform
```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure MySQL

* Create or configure the project database using the SQL scripts in the `sql/` directory.
* Configure your local database connection settings.
* Keep passwords and other credentials out of GitHub.

### 4. Run the Pipeline

After configuring the required database connection and project dependencies, run:

```bash
python -m python.pipeline.master_pipeline
```

The pipeline generates the project's data-layer outputs. Generated Gold datasets are intentionally excluded from Git tracking and may need to be regenerated locally.

### 5. Run Databricks Analytics

Upload the generated Gold datasets to your Databricks workspace, then run the analytics notebook or SQL workflow used to create the five Delta tables listed above.

## Project Status

**Implemented:** Core batch pipeline, Gold dimension and fact datasets, data-quality validations, and Databricks Delta analytics.

**Potential future enhancements:** Automated orchestration, streaming ingestion, and dashboard integration.

## Business Value

SkyFlow demonstrates how airline operational data can be transformed into structured, validated datasets for revenue analysis, booking insights, payment analysis, and flight-performance monitoring.
