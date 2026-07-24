# SkyFlow - Python Architecture

## Overview

The Python layer is responsible for generating realistic airline data, validating datasets, orchestrating the complete data pipeline, and loading processed data into MySQL.

---

# Python Data Pipeline

Python Data Generator
        │
        ▼
Generate CSV Files
        │
        ▼
Pandas Validation
        │
        ▼
Databricks + PySpark
        │
        ▼
Parquet Files
        │
        ▼
MySQL
        │
        ▼
Power BI Dashboard

---

# Python Folder Structure

```
python/
│
├── config/
│      config.py
│
├── generators/
│      airport_generator.py
│      aircraft_generator.py
│      passenger_generator.py
│      crew_generator.py
│      route_generator.py
│      flight_generator.py
│      booking_generator.py
│      payment_generator.py
│      baggage_generator.py
│      weather_generator.py
│      maintenance_generator.py
│      fuel_generator.py
│      feedback_generator.py
│
├── validators/
│      validate_airport.py
│      validate_passenger.py
│      validate_booking.py
│
├── loaders/
│      mysql_loader.py
│
├── pipeline/
│      run_pipeline.py
│
├── utils/
│      helpers.py
│      logger.py
│
└── tests/
```

---

# Folder Responsibilities

## config/

Stores project configuration.

Example:

- Database Configuration
- File Paths
- Global Variables

---

## generators/

Generate realistic airline datasets.

Files:

- airport_generator.py
- aircraft_generator.py
- passenger_generator.py
- crew_generator.py
- route_generator.py
- flight_generator.py
- booking_generator.py
- payment_generator.py
- baggage_generator.py
- weather_generator.py
- maintenance_generator.py
- fuel_generator.py
- feedback_generator.py

---

## validators/

Validate generated datasets.

Responsibilities:

- Check NULL values
- Remove duplicates
- Validate Email
- Validate Phone Number
- Validate Passport Number
- Validate Foreign Keys

---

## loaders/

Load processed CSV files into MySQL.

Responsibilities:

- Read CSV Files
- Batch Insert
- Error Logging

---

## pipeline/

Controls the complete project workflow.

Main File:

run_pipeline.py

Pipeline Flow:

Generate Data

↓

Validate Data

↓

Load into MySQL

↓

Pipeline Completed

---

## utils/

Contains reusable helper functions.

Examples:

- Logger
- Date Functions
- Random Utilities
- Common Functions

---

## tests/

Used for testing Python modules.

---

# Python Libraries

- pandas
- faker
- random
- uuid
- datetime
- csv
- mysql-connector-python
- pathlib
- logging
- os

---

# Generated Files

- airport.csv
- aircraft.csv
- passenger.csv
- crew.csv
- route.csv
- flight.csv
- booking.csv
- payment.csv
- baggage.csv
- weather.csv
- maintenance.csv
- fuel_consumption.csv
- customer_feedback.csv

---

# Responsibilities of Python Layer

- Generate realistic airline datasets.
- Maintain relationships between tables.
- Validate generated data.
- Export CSV files.
- Load data into MySQL.
- Prepare datasets for Databricks.
- Execute the complete data pipeline.

---

# Future Enhancement (cloud version)

- Azure Data Lake Storage
- Azure Data Factory
- Azure Databricks
- Azure SQL Database