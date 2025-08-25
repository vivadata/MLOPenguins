"""
Data Loading and Cleaning logic
"""

import os

import loguru
import pandas as pd
from seaborn import load_dataset
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

from registry import save_model, load_model

logger = loguru.logger

def load_data():
    """
    Load the penguins dataset.
    """
    if not os.path.exists("data"): 
        logger.info("Creating data directory")
        os.makedirs("data")
    if os.path.exists("data/penguins.csv"):
        logger.info("✅ Data Loaded from cache")
        return pd.read_csv("data/penguins.csv")
    data = load_dataset("penguins")
    data.to_csv("data/penguins.csv", index=False)
    return data

def clean_data(data:pd.DataFrame) -> pd.DataFrame:
    """
    Remove NaN and duplicate rows.
    """
    data = data.drop(columns=["island"])
    data = data.dropna().drop_duplicates()
    logger.info("✅ Data cleaned")    
    return data

def preprocess_data(data:pd.DataFrame, fit=False):
    pipe = instantiate_preprocessor(data,fit=fit)
    return pipe.transform(data)

def instantiate_preprocessor(data,fit=False) -> Pipeline:
    if fit :
        logger.info("Fitting preprocessor...")
        cat_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(sparse_output=False, drop="first")),
        ]).set_output(transform="pandas")
        num_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]).set_output(transform="pandas")
        
        preproc = ColumnTransformer([
            ("cat", cat_pipe, make_column_selector(dtype_include="object")),
            ("num", num_pipe, make_column_selector(dtype_include="number")),
        ]).set_output(transform="pandas")
        preproc.fit(data)
        save_model(preproc, "preprocessor")
        logger.info("✅ Preprocessor fitted")
    else :
        logger.info("Loading preprocessor...")
        preproc = load_model("preprocessor")
    return preproc
    

def get_X_y(data):
    """
    Split the data into features and target. 
    Return X_train, X_test, y_train, y_test
    """
    X = data.drop(columns=["species"])
    y = data["species"]
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

if __name__ == "__main__":
    data = load_data()
    cleaned_data = clean_data(data)
    X_train, X_test, y_train, y_test = get_X_y(cleaned_data)
    X_train_preproc = preprocess_data(X_train, fit=True)
    X_test_preproc = preprocess_data(X_test, fit=False)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)