# app.py
import streamlit as st
import pandas as pd
import random

# Load the data from the CSV file
data = pd.read_csv("data/parental-guides.csv")

st.title('Content Rating')

# Define the options for the categories and severities
category_options = ["Sex & Nudity", "Violence & Gore", "Profanity", "Alcohol, Drugs & Smoking", "Frightening & Intense Scenes"]
severity_options = ["Severe", "Moderate", "Mild"]

# Create dropdowns for category and severity for each criteria
criteria_1_category = st.selectbox('Select Category 1:', category_options)
criteria_1_severity = st.selectbox('Select Severity 1:', severity_options)

criteria_2_category = st.selectbox('Select Category 2:', category_options)
criteria_2_severity = st.selectbox('Select Severity 2:', severity_options)


# This part will be done by the back-end:

# Filter the data based on user selections for both criteria
filtered_data_1 = data[(data['cat'] == criteria_1_category) & (data['level'] == criteria_1_severity)]
filtered_data_2 = data[(data['cat'] == criteria_2_category) & (data['level'] == criteria_2_severity)]

# Group the filtered data by series title and aggregate the severity levels
grouped_data_1 = filtered_data_1.groupby('t')['level'].agg(','.join)
grouped_data_2 = filtered_data_2.groupby('t')['level'].agg(','.join)

# Find the intersection of the series titles that meet both criteria
intersected_series_titles = grouped_data_1.index.intersection(grouped_data_2.index)

# Randomly select one series from the intersected series titles
if len(intersected_series_titles) > 0:
    recommended_show = random.choice(intersected_series_titles)
    st.write('Recommended Show:', recommended_show)
else:
    st.write('No series found.')
