import streamlit as st 
import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

import os, time

BACKEND_URL = os.getenv("BACKEND_URL")

@st.cache_data
def load_data():
    with st.spinner('Loading data...'):
        df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv")
        time.sleep(3)
    return df

df = load_data()
st.dataframe(df.head())

st.button("Hello")

fig, ax = plt.subplots()
sns.histplot(data=df, x="body_mass_g", hue="species", kde=True, ax=ax)
ax.set_title("Body Mass Distribution by Species")
st.pyplot(fig)

st.header("My Penguin App")
st.write(""" Welcome, Penguin Enthusiasts!""")

bill_length = st.number_input('Bill Length (mm)', value=7.0)
bill_depth = st.number_input('Bill Depth (mm)', value=5.0)
flipper_length = st.number_input('Flipper Length (mm)', value=200.0)
body_mass = st.number_input('Body Mass (g)', value=4000.0)
sex = st.selectbox('Sex', options=['Male', 'Female'])

if st.button("Predict Species"):
    with st.spinner('Predicting species...'):
        time.sleep(3)
        params = {"bill_length_mm": bill_length,
                  "bill_depth_mm": bill_depth,
                  "flipper_length_mm": flipper_length,
              "body_mass_g": body_mass,
              "sex": sex}

        response = requests.get(f"{BACKEND_URL}/predict", params=params)

    if response.status_code == 200:
        st.snow()
        prediction = response.json()
        st.success(f"The predicted species is: {prediction}")
    else:
        st.error("Error occurred while predicting species.")
