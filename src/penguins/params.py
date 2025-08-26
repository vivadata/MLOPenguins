
import os

MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI")
MLFLOW_EXPERIMENT_NAME = os.environ.get("MLFLOW_EXPERIMENT_NAME", "default")

if __name__=="__main__":
    print(f"MLFLOW_TRACKING_URI = {MLFLOW_TRACKING_URI}")
    print(f"MLFLOW_EXPERIMENT_NAME = {MLFLOW_EXPERIMENT_NAME}")