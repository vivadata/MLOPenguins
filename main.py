
# import loguru
# from penguins.data import load_data, preprocess_data, clean_data, get_X_y
# from penguins.model import instantiate_model,train_model, evaluate_model, save_model

# logger = loguru.logger 

# def train():
#     data = load_data()
#     cleaned_data = clean_data(data)
#     X_train, X_test, y_train, y_test = get_X_y(cleaned_data)
#     X_train_preproc = preprocess_data(X_train, fit=True)
#     X_test_preproc = preprocess_data(X_test, fit=False)
#     logger.info("✅ Data preprocessing complete")  
#     model = instantiate_model(fit=True)
#     model = train_model(model,X_train_preproc, y_train)
#     logger.info("✅ Model training complete")
#     score = evaluate_model(model, X_test_preproc, y_test)
#     logger.info(f"✅ Model evaluation complete: {score}")

if __name__ == "__main__":
    print(f"In main.py, __name__ = {__name__}")
    from penguins import registry