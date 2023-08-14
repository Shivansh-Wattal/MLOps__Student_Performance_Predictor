import sys
from dataclasses import dataclass
import os

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl") 


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_obj(self):
        
        # function used for data transformation

        try:
            numerical_columns = ['reading score','writing score']
            categorical_columns = [
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course"
                ]
            
            # Data transformation pipeline for numerical columns.
            num_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='median')), # Fill null values.
                    ('scaler',StandardScaler()) # Standardization
                ]

            )
            # Data transformation pipeline for categorical columns.
            cat_pipeline = Pipeline(
                steps = [
                    ('imputer',SimpleImputer(strategy='most_frequent')), # Fill null values.
                    ('one_hot_encoder',OneHotEncoder()), #One Hot encoding.
                    ('scaler',StandardScaler(with_mean=False)) # Standardization.

                ]
                
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combined pipeline for all the columns.
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,categorical_columns)
                ]

            )

            return preprocessor

        except Exception as e:
            raise CustomException(e,sys) 
    
    def initiate_data_trransformation(self,train_path,test_path):
        try:
            # Reading data.
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("read train and test data.")

            logging.info("obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_obj()

            target_column_name = "math score"
            #numerical_columns = ['reading score','writing score']

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("applying preprocessing object to training and testing dataframe")

            # Transforming data using the preprocessing_obj file.
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Concatination.
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]

            logging.info("saved preprocessing object.")

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)