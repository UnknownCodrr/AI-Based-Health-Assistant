import streamlit as st
import nltk
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from transformers import pipeline

# Download necessary NLTK data
nltk.download('punkt')

# Load a pre-trained transformer model for text generation
text_generator = pipeline("text-generation", model="distilgpt2")

# Streamlit App Interface with Enhanced UI
st.set_page_config(page_title="AI Healthcare Assistant", page_icon="🩺", layout="centered")
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .stTextInput>div>div>input {border-radius: 10px; padding: 10px;}
    .stButton>button {border-radius: 10px; background-color: #4CAF50; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("🩺 AI Healthcare Assistant")
st.write("#### Ask me anything about healthcare, symptoms, or medical conditions.")

# User input with placeholder
user_question = st.text_input("💬 Enter your health-related query:",
                              placeholder="e.g., What are the symptoms of diabetes?")

if user_question:
    with st.spinner("Analyzing your question..."):
        response = text_generator(user_question, max_length=100, num_return_sequences=1)
        generated_text = response[0]['generated_text']

    st.success("✅ Here is what I found:")
    st.write(f"📌 {generated_text}")

    # Additional AI-powered analysis with styled output
    st.subheader("🧐 Additional Analysis:")
    if "fever" in user_question.lower():
        st.info("Fever may indicate an infection. If it persists, consult a doctor.")
    elif "cough" in user_question.lower():
        st.info(
            "A persistent cough might be due to allergies, infections, or other conditions. Seek medical advice if severe.")
    else:
        st.warning("Please provide more details for a precise analysis.")

    # Additional Features
    st.subheader("📊 Health Statistics & Trends")
    health_data = pd.DataFrame({
        'Condition': ['Diabetes', 'Hypertension', 'Heart Disease', 'Asthma'],
        'Prevalence (%)': [10.5, 14.8, 8.2, 6.1]
    })
    st.bar_chart(health_data.set_index('Condition'))

    st.subheader("🛠️ Useful Health Tools")
    bmi_weight = st.number_input("Enter your weight (kg):", min_value=1.0, max_value=300.0, step=0.1)
    bmi_height = st.number_input("Enter your height (m):", min_value=0.5, max_value=2.5, step=0.01)
    if bmi_weight and bmi_height:
        bmi = bmi_weight / (bmi_height ** 2)
        st.write(f"Your BMI: {bmi:.2f}")
        if bmi < 18.5:
            st.warning("You are underweight. Consider consulting a nutritionist.")
        elif 18.5 <= bmi < 24.9:
            st.success("You have a healthy weight.")
        elif 25 <= bmi < 29.9:
            st.warning("You are overweight. Consider a balanced diet and exercise.")
        else:
            st.error("You are in the obese range. Consult a doctor for guidance.")
