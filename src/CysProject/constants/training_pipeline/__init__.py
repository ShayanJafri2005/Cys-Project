# GENERAL TRAINING PIPELINE CONSTANTS

# Target column (label)
TARGET_COLUMN: str = "Result"

# ML pipeline name
PIPELINE_NAME: str = "NetworkSecurity"

# Directory for storing pipeline artifacts
ARTIFACT_DIR: str = "Artifacts"

# Raw data file name (after ingestion/export from DB)
FILE_NAME: str = "phisingData.csv"

# Train/Test split file names
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH: str = "schema.yaml"


"""
Data Ingestion related constants.
All constants start with DATA_INGESTION_ prefix.
"""

# SQLite database file (instead of server DB)
DATA_INGESTION_DATABASE_NAME: str = "network_data.db"

# Table name inside SQLite
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"

# Directory structure for ingestion pipeline
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"

# Train-test split ratio
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2 


"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

