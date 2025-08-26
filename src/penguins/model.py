"""
Model training and evaluation logic
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from penguins.registry import save_model, load_model

def instantiate_model(fit=True):
    if fit:
        return LogisticRegression()
    else:
        return load_model("logistic_regression")

def train_model(model, X_train:pd.DataFrame, y_train:pd.Series):
    model.fit(X_train, y_train)
    save_model(model, "logistic_regression")
    return model

def evaluate_model(model, X:pd.DataFrame, y:pd.Series):
    y_pred = model.predict(X)
    return round(accuracy_score(y, y_pred), 2)
