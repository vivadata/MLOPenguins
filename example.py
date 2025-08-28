from prefect import flow, task
from prefect.logging import loggers
import time
import prefect

logger = prefect.logging.get_logger()

@task(log_prints=True)
def load_data() :
    logger = loggers.get_run_logger()
    logger.info("✅ Data Loaded")
    time.sleep(2)
    return 1

@task 
def preproc(X):
    logger.info("✅ Data preprocessed")
    time.sleep(2)
    return 1

@task 
def get_X_y(data):
    return "X_train","y_train","X_test","y_test"

@task 
def train(X_train,y_train):
    time.sleep(3)
    return
    
@task 
def evaluate(model,X_test,y_test):
    time.sleep(3)
    return 1
    
@task()
def notify(trained,score):
    logger = loggers.get_run_logger()
    logger.info("✅ Model Trained")
    
@flow
def main(): 
    data = load_data()
    X_train,y_train,X_test,y_test = get_X_y(data)
    X_train_preproc = preproc(X_train)
    X_test_preproc = preproc(X_test)
    model = train(X_train,y_train)
    score = evaluate(model,X_test,y_test)
    notify(model,score)

from datetime import timedelta, datetime
from prefect.schedules import Interval
if __name__ == "__main__" : 
    main(
        # name = "my-little-deployment",
        # cron =  "*/5 * * * *",
        # schedule= Interval(timedelta(minutes=5)
        #                    , anchor_date=datetime(2025,8,27,13,0,0)
        #                    , timezone="Europe/Paris")
    )