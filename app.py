# app.py
import streamlit as st
import pandas as pd
import random
import query

st.title("Content Rating")

# Define the options for the categories and severities
category_options = [
    "Sex & Nudity",
    "Violence & Gore",
    "Profanity",
    "Alcohol, Drugs & Smoking",
    "Frightening & Intense Scenes",
]
severity_options = ["Severe", "Moderate", "Mild"]

# Create dropdowns for category and severity for each criteria
criteria_1_category = st.selectbox("Select Category 1:", category_options)
criteria_1_severity = st.selectbox("Select Severity 1:", severity_options)

criteria_2_category = st.selectbox("Select Category 2:", category_options)
criteria_2_severity = st.selectbox("Select Severity 2:", severity_options)


# This part will be done by the back-end:

# criteria_list = ['Sex & Nudity','Severe','Profanity','Moderate']
criteria_list = [
    criteria_1_category,
    criteria_1_severity,
    criteria_2_category,
    criteria_2_severity,
]
st.write("Recommended Show:", query.query_series(criteria_list=criteria_list))

