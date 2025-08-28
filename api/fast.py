from  fastapi import FastAPI
import pandas as pd
import loguru
from pydantic import BaseModel
from enum import Enum

from penguins.data import preprocess_data
from penguins.model import instantiate_model

model = instantiate_model(fit=False)

my_api = FastAPI()

@my_api.get("/")
def read_root():
    return {"Hello": "World"}


@my_api.get("/predict")
def predict(bill_length_mm : float,
            bill_depth_mm  : float,
            flipper_length_mm : float,
            body_mass_g : float,
            sex : str) -> str:
    if sex not in ["Male", "Female"]:
        return {"error": "Invalid sex. Please provide 'male' or 'female'."}

    data = pd.DataFrame({
        "bill_length_mm": [bill_length_mm],
        "bill_depth_mm": [bill_depth_mm],
        "flipper_length_mm": [flipper_length_mm],
        "body_mass_g": [body_mass_g],
        "sex": [sex]
    })
    clean_data = preprocess_data(data)
    loguru.logger.info(f"Cleaned data ✅")
    prediction = model.predict(clean_data)
    loguru.logger.info(f"Prediction ✅")
    return prediction.item()

class Sex(str, Enum):
    Male = "Male"
    Female = "Female"

class PenguinFeatures(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    sex: Sex

@my_api.post("/predict")
def predict_post(features: PenguinFeatures) -> str:
    data = pd.DataFrame([features.model_dump()])
    clean_data = preprocess_data(data)
    loguru.logger.info(f"Cleaned data ✅")
    prediction = model.predict(clean_data)
    loguru.logger.info(f"Prediction ✅")
    return prediction.item()

# @my_api.post("/predict_batch")
# def predict_batch(features: list[PenguinFeatures]) -> list[str]:
#     data = pd.DataFrame([feature.model_dump() for feature in features])
#     clean_data = preprocess_data(data)
#     loguru.logger.info(f"Cleaned data ✅")
#     predictions = model.predict(clean_data)
#     loguru.logger.info(f"Predictions ✅")
#     return predictions.tolist()

from fastapi import File,UploadFile
from typing import Annotated
import csv

@my_api.post("/predict_batch")
def predict_batch(file: UploadFile = File(...)):
    csvReader = csv.DictReader(file.file.read().decode('utf-8').splitlines())
    data = pd.DataFrame(csvReader)
    clean_data = preprocess_data(data)
    loguru.logger.info(f"Cleaned data ✅")
    predictions = model.predict(clean_data)
    loguru.logger.info(f"Predictions ✅")
    return predictions.tolist()