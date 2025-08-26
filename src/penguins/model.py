"""
Model training and evaluation logic
"""

import loguru
import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score


from penguins.registry import save_model, load_model
from penguins.params import MLFLOW_EXPERIMENT_NAME, MLFLOW_TRACKING_URI

logger = loguru.logger

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

def instantiate_model(fit=True):
    if fit:
        mlflow.log_params({"model_type": "LogisticRegression", "max_iter": 10_000})
        return LogisticRegression(max_iter=10_000)
    else:
        return load_model("logistic_regression")

def train_model(model, X_train:pd.DataFrame, y_train:pd.Series):
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X:pd.DataFrame, y:pd.Series) -> tuple[float]:
    y_pred = model.predict(X)
    score =  round(accuracy_score(y, y_pred), 2)
    recall = round(recall_score(y, y_pred, average="macro"), 2)
    precision = round(precision_score(y, y_pred, average="macro"), 2)
    f1 = round(f1_score(y, y_pred, average="macro"), 2)
    logger.info(f"✅ Model evaluation complete: {score}")
    signature = mlflow.models.infer_signature(X, model.predict(X))
    mlflow.sklearn.log_model(model
                            , name="logistic_regression"
                            , input_example=X.iloc[:5]
                            , signature=signature)
    mlflow.log_metric("test_accuracy", score)
    mlflow.log_metric("test_recall", recall)
    mlflow.log_metric("test_precision", precision)
    mlflow.log_metric("test_f1", f1)
    return score, recall, precision, f1
