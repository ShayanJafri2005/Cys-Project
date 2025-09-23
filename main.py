from src.CysProject.components.data_ingestion import DataIngestion
from src.CysProject.components.data_validation import DataValidation
from src.CysProject.entity.config_entity import DataValidationConfig
from src.CysProject.entity.config_entity import DataIngestionConfig
from src.CysProject.entity.config_entity import TrainingPipelineConfig
from src.CysProject.exception.exception import NetworkSecurityException
from src.CysProject.logging.logger import logging
import sys


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate Data Ingestion Config")
        data_ingestion_artifact = dataingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        print("Data Initiation Completed")
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initiate Data Validation Config")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        print("Data Validation Completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)