'''To provide a user-friendly interface for predicting a person’s insurance premium category based on their health, income, and lifestyle data by communicating with a machine learning model served via FastAPI.'''

import streamlit as st
import requests

API_URL = "http://52.66.135.111:8000/predict"

st.title("Insurance Premium Category Predictor")

st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=22)
weight = st.number_input("Weight (kg)", min_value=1.0, value=60.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.65)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=5.0)
smoker = st.selectbox("Are you a smoker?", options=[False,True])
city = st.text_input("City", value="New Delhi")
occupation = st.selectbox(
    "Occupation",
    ['private_job', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'retired']
)

if st.button("Predict Premium Category"):
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "response" in result:
            prediction = result["response"]
            st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
            st.write("🔍 Confidence:", prediction["confidence"])
            st.write("📊 Class Probabilities:")
            st.json(prediction["class_probabilities"])

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")