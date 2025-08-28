from prefect import get_run_logger
from prefect import flow,task
import loguru
from penguins.data import load_data, preprocess_data, clean_data, get_X_y
from penguins.model import instantiate_model,train_model, evaluate_model, save_model

logger = loguru.logger 

@task
def load_data_task():
    return load_data()
    
@task
def clean_data_task(*args,**kwargs):
    return clean_data(*args,**kwargs)

@task
def preprocess_data_task(*args,**kwargs):
    return preprocess_data(*args,**kwargs)

@task
def get_X_y_task(*args,**kwargs):
    return get_X_y(*args,**kwargs)

@task
def instantiate_model_task(*args,**kwargs):
    return instantiate_model(*args,**kwargs)

@task
def train_model_task(model, X, y):
    return train_model(model, X, y)

@task
def evaluate_model_task(model, X, y):
    return evaluate_model(model, X, y)

@flow
def train_flow():
    logger = get_run_logger()
    data = load_data_task()
    cleaned_data = clean_data_task(data)
    X_train, X_test, y_train, y_test = get_X_y_task(cleaned_data)
    X_train_preproc = preprocess_data_task(X_train, fit=True)
    X_test_preproc = preprocess_data_task(X_test, fit=False)
    logger.info("✅ Data preprocessing complete")  
    model = instantiate_model_task(fit=True)
    model = train_model_task(model,X_train_preproc, y_train)
    logger.info("✅ Model training complete")
    evaluate_model_task(model, X_test_preproc, y_test)


def train():
    data = load_data()
    cleaned_data = clean_data(data)
    X_train, X_test, y_train, y_test = get_X_y(cleaned_data)
    X_train_preproc = preprocess_data(X_train, fit=True)
    X_test_preproc = preprocess_data(X_test, fit=False)
    logger.info("✅ Data preprocessing complete")  
    model = instantiate_model(fit=True)
    model = train_model(model,X_train_preproc, y_train)
    logger.info("✅ Model training complete")
    evaluate_model(model, X_test_preproc, y_test)


if __name__ == "__main__":
    train()