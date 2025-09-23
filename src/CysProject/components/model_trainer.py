import os
import sys 
from src.CysProject.exception.exception import NetworkSecurityException
from src.CysProject.logging.logger import logging

from src.CysProject.entity.config_entity import ModelTrainerConfig
from src.CysProject.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact

from src.CysProject.utils.gen_functions import load_object,save_object
from src.CysProject.utils.gen_functions import load_numpy_array_data,evaluate_models
from src.CysProject.utils.ml_utils.metric.classification_metric import get_classification_score
from src.CysProject.utils.ml_utils.model.estimator import NetworkModel 

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier as KNNClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
    ExtraTreesClassifier
) 
from sklearn.svm import SVC



class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact): 
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models = {
                "LogisticRegression": LogisticRegression(verbose=1),
                "KNeighborsClassifier": KNNClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "RandomForestClassifier": RandomForestClassifier(verbose=1),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
                "ExtraTreesClassifier": ExtraTreesClassifier(verbose=1),
                "SVC": SVC(verbose=1)
            }

            params = {
                "LogisticRegression": {
                    "C": [0.1, 1, 10],
                    "penalty": ["l1", "l2"],
                    "solver": ["liblinear", "saga"]
                },
                "KNeighborsClassifier": {
                    "n_neighbors": [3,4 ],
                    "weights": ["uniform", "distance"],
                   # "algorithm": ["auto", "ball_tree", "kd_tree", "brute"]
                },
                "DecisionTreeClassifier": {
                   # "criterion": ["gini", "entropy"],
                   # "splitter": ["best", "random"],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf":  [1, 2, 4]
                },
                "RandomForestClassifier": {
                    "n_estimators": [50, 100, 200],
                    "criterion": ["gini", "entropy"],
                    "max_depth": [None, 10, 20, 30],
                 #   "min_samples_split": [2, 5, 10  ],
                   # "min_samples_leaf": [1, 2,],
                  #  "max_features": ["auto", "sqrt", "log2"]
                },
                "AdaBoostClassifier": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1.0]
                },
                "GradientBoostingClassifier": {
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1.0],
                    "max_depth": [3, 4, 5]
                },
                "ExtraTreesClassifier": {
                    "n_estimators": [50, 100, 20],
                   # "criterion": ["gini", "entropy"],
                    "max_depth": [None, 10, 20, 30],
                   # "min_samples_split": [2, 5, 10],
                  #  "min_samples_leaf": [1, 2, 4]
                },
                "SVC": {
                    "C": [0.1, 1, 10],
                    "kernel": ["linear", "rbf"],
                    "gamma": ["scale", "auto"]
                }
            }
            
            model_report:dict = evaluate_models(X_train=x_train,y_train=y_train,
                                                X_test=x_test,y_test=y_test,
                                                models=models,param=params)
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            y_train_pred = best_model.predict(x_train)
            classification_train_metric =get_classification_score(y_train,y_train_pred)

             ##  We will write a function to track in mlflow next commit

            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_test,y_test_pred)

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            network_model = NetworkModel(preprocessor=preprocessor,model=best_model)
            logging.info(f"Best found model on both training and testing dataset.")
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=network_model)

            ## Model Trainer Artifact 
            ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                 train_metric_artifact=classification_train_metric,
                                 test_metric_artifact=classification_test_metric)
            logging.info(f"Model trainer artifact: {ModelTrainerArtifact} created")
            return network_model

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info("Loading transformed training dataset")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            ##loading training and testing array 
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            logging.info("Splitting input and target feature from both train and test arr")

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model= self.train_model(x_train,y_train,x_test,y_test)




        except Exception as e:
            raise NetworkSecurityException(e,sys)