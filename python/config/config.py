"""
SkyFlow Configuration File
"""

from pathlib import Path

# Project Root Folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data Folder
DATA_FOLDER = PROJECT_ROOT / "data"

# Data Layers
RAW_FOLDER = DATA_FOLDER / "raw"
BRONZE_FOLDER = DATA_FOLDER / "bronze"
SILVER_FOLDER = DATA_FOLDER / "silver"
GOLD_FOLDER = DATA_FOLDER / "gold"

# MySQL Configuration
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "kumkum@123*",
    "database": "skyflow_db"
}