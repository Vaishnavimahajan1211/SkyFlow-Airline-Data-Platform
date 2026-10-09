
"""
SkyFlow Configuration File
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Project Root Folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load environment variables from the project root .env file
load_dotenv(PROJECT_ROOT / ".env")

# Data Folder
DATA_FOLDER = PROJECT_ROOT / "data"

# Data Layers
RAW_FOLDER = DATA_FOLDER / "raw"
BRONZE_FOLDER = DATA_FOLDER / "bronze"
SILVER_FOLDER = DATA_FOLDER / "silver"
GOLD_FOLDER = DATA_FOLDER / "gold"

# MySQL Configuration
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE", "skyflow_db")
}