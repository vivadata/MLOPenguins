from flask import Flask, render_template, request
import requests

BACKEND_URL= "https://penguins-api-861302064365.europe-west9.run.app/"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=["GET", "POST"])    
def pred():
    if request.method == "POST":
        # Handle form submission
        data = request.form
        print(data)
        # Process the data and make predictions
        params = {"bill_length_mm": data["bill_length_mm"],
                  "bill_depth_mm": data["bill_depth_mm"],
                  "flipper_length_mm": data["flipper_length_mm"],
                  "body_mass_g": data["body_mass_g"],
                  "sex": data["sex"]}

        response = requests.get(f"{BACKEND_URL}/predict", params=params)

        if response.status_code == 200:
            prediction = response.json()
            print(f"The predicted species is: {prediction}")
        return render_template('result.html', prediction=prediction)
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
