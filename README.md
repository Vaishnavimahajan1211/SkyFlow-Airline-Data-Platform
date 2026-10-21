# SkyFlow — Enterprise Airline Data Platform

An end-to-end data engineering project that transforms airline operational data into analytics-ready datasets using MySQL, Python, Pandas, PySpark, and Databricks.

## Overview

SkyFlow simulates a modern airline data platform that processes passenger, booking, flight, airport, aircraft, route, and payment data. It uses a layered data architecture to transform operational data into structured datasets for business analysis and operational reporting.

## Architecture

**MySQL → Python ETL → Bronze → Silver → Gold → Databricks → Delta Analytics Tables**

![SkyFlow Architecture](docs/screenshots/skyflow_architecture.png)

## Technology Stack

| Category | Technologies |
|---|---|
| Database | MySQL |
| Programming | Python, SQL |
| Data Processing | Pandas, Apache Spark, PySpark |
| Analytics Platform | Databricks |
| Storage Formats | CSV, Delta Tables |
| Version Control | Git, GitHub |

## Key Features

### 1. End-to-End Data Pipeline

- Airline-related relational data and Python-based data generation.
- Bronze, Silver, and Gold data-processing layers.
- PySpark transformations for dimension and fact datasets.
- Analytics-ready datasets for downstream business analysis.

![Pipeline Execution](docs/screenshots/skyflow_pipeline.png)

### 2. Gold Data Layer

The pipeline generates seven dimension and fact datasets containing **11,400 records**.

| Dataset | Records |
|---|---:|
| `dim_passenger` | 1,000 |
| `dim_airport` | 50 |
| `dim_aircraft` | 50 |
| `dim_route` | 100 |
| `fact_booking` | 5,000 |
| `fact_flight` | 200 |
| `fact_payment` | 5,000 |
| **Total** | **11,400** |

### 3. Data Quality

The tested pipeline run completed **52 out of 52 data-quality checks successfully**.

Validation includes:
- Primary-key null and duplicate checks.
- Foreign-key integrity checks.
- Booking amount and flight-delay business-rule checks.
- CSV-based data-quality reporting.

![Data Quality Report](docs/screenshots/skyflow_data_quality_report.png)

### 4. Databricks Analytics

Five persisted Delta analytics tables have been created and verified:

- `workspace.default.skyflow_booking_kpis`
- `workspace.default.skyflow_flight_kpis`
- `workspace.default.skyflow_payment_kpis`
- `workspace.default.skyflow_route_revenue`
- `workspace.default.skyflow_flight_performance`

These tables support analysis of booking status, confirmed-booking revenue, payment amounts, route revenue, and flight performance.

![Databricks Analytics](docs/screenshots/databricks_analytics.png)

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

- Python
- MySQL and MySQL Workbench
- Git
- A Databricks workspace for the analytics stage

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

- Create and configure the project database using the SQL scripts in the `sql/` directory.
- Set up the local database connection using the project's configuration.
- Keep credentials in a local `.env` file and never commit passwords or secrets.

### 4. Run the Pipeline

After configuring MySQL and the required dependencies, run:

```bash
python -m python.pipeline.master_pipeline
```

The pipeline generates the project's data-layer outputs. Generated data may need to be recreated locally because some generated files are excluded from Git tracking.

### 5. Run Databricks Analytics

Upload the generated Gold datasets to your Databricks workspace and run the project's analytics notebook or SQL workflow to create and verify the five Delta tables listed above.

## Validation Results

Latest recorded validation results:

- Pipeline steps completed: **8/8**
- Data-quality checks passed: **52/52**
- Automated unit tests passed: **17/17**
- Gold datasets: **7**
- Gold records: **11,400**
- Verified Databricks Delta analytics tables: **5**

These results describe the tested project run. A fresh setup should rerun the pipeline and tests to verify its own environment.

## Project Status

**Implemented:** Core batch pipeline, Gold dimension and fact datasets, data-quality validations, automated tests, and Databricks Delta analytics.

**Potential future enhancements:**
- Automated workflow orchestration.
- Streaming data ingestion.
- Business intelligence dashboard integration.

## Business Value

SkyFlow demonstrates how airline operational data can be transformed into structured, validated datasets for booking analysis, revenue insights, payment monitoring, route performance, and flight-performance analysis.

## Author

**Vaishnavi Mahajan**

- [GitHub](https://github.com/Vaishnavimahajan1211)
- [LinkedIn](https://www.linkedin.com/in/vaishnavi-mahajan-4549203a2)
