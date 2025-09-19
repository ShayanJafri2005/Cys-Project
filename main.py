from src.CysProject.components.data_ingestion import DataIngestion
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
    except Exception as e:
        raise NetworkSecurityException(e,sys)