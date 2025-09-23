import sys 
import os 
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from src.CysProject.exception.exception import NetworkSecurityException
from src.CysProject.logging.logger import logging
from sklearn.pipeline import Pipeline
from src.CysProject.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from src.CysProject.constants.training_pipeline import TARGET_COLUMN
from src.CysProject.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from src.CysProject.entity.config_entity import DataTransformationConfig
import pickle 
from src.CysProject.utils.gen_functions import save_numpy_array_data,save_object


class DataTransformation:   
    def __init__(self, data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """Read CSV file into DataFrame"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        try:
            logging.info("Creating data transformer object.")
            imputer_params = DATA_TRANSFORMATION_IMPUTER_PARAMS
            imputer = KNNImputer(**imputer_params)
            
            pipeline = Pipeline(steps=[
                ('imputer', imputer)
            ])
            logging.info("Data transformer object created successfully.")
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation.")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Obtaining preprocessing object.")

            ## training dataframe 
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)


            ##testing dataframe 
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            logging.info("Obtaining preprocessing object.")
            preprocessing_object = self.get_data_transformer_object()
            preprocessor_object = preprocessing_object.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            ## preparing artifacts datatransformation_artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )   

            return data_transformation_artifact 

        except Exception as e:
            raise NetworkSecurityException(e, sys)