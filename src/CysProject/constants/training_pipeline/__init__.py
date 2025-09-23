import numpy as np
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


"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}