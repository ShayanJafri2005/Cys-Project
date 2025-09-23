from src.CysProject.exception.exception import NetworkSecurityException
from src.CysProject.logging.logger import logging
from src.CysProject.entity.config_entity import DataValidationConfig
from src.CysProject.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.CysProject.constants.training_pipeline import SCHEMA_FILE_PATH
from src.CysProject.utils.gen_functions import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """Read CSV file into DataFrame"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_columns(self, dataframe: pd.DataFrame) -> bool:
        """Validate number of columns against schema"""
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {list(dataframe.columns)}")
            return len(dataframe.columns) == number_of_columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool:
        """Check if required numerical columns exist"""
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns

            missing_numerical_columns = [
                col for col in numerical_columns if col not in dataframe_columns
            ]

            if missing_numerical_columns:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
                return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """Detect data drift between train and test datasets"""
        try:
            status = True
            report = {}

            for column in base_df.columns:
                if column not in current_df.columns:
                    continue
                d1 = base_df[column]
                d2 = current_df[column]
                test_result = ks_2samp(d1, d2)

                if threshold <= float(test_result.pvalue):
                    is_found = False
                else:
                    is_found = True
                    status = False

                report[column] = {
                    "p_value": float(test_result.pvalue),
                    "drift_status": is_found
                }

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = ""

            # Get train and test file paths from DataIngestionArtifact
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Reading data
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # Validate number of columns
            if not self.validate_number_columns(train_dataframe):
                error_message += "Train dataframe does not contain all columns.\n"
            if not self.validate_number_columns(test_dataframe):
                error_message += "Test dataframe does not contain all columns.\n"

            # Check numerical columns
            if not self.is_numerical_column_exist(train_dataframe):
                error_message += "Train dataframe does not contain all numerical columns.\n"
            if not self.is_numerical_column_exist(test_dataframe):
                error_message += "Test dataframe does not contain all numerical columns.\n"

            if error_message:
                logging.info(error_message)

            # Data drift detection
            status = self.detect_dataset_drift(train_dataframe, test_dataframe)

            # Save validated datasets
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            # Build artifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
