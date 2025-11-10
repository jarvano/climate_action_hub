#!/usr/bin/env python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="CO2 Emissions Forecast",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading and Caching ---
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'data', 'owid-co2-data.csv')
    df = pd.read_csv(data_path)
    return df

df = load_data()

# --- Sidebar ---
st.sidebar.title("Configuration")

# Country selection
countries = sorted(df['country'].unique())
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=['Kenya', 'China', 'United States'])

# Year selection
min_year, max_year = int(df['year'].min()), int(df['year'].max())
start_year = st.sidebar.slider("Start Year", min_year, max_year, min_year)
end_year = st.sidebar.slider("End Year", min_year, max_year, max_year)

# Forecast horizon
forecast_horizon = st.sidebar.slider("Forecast Horizon (Years)", 1, 20, 8)

# --- Main Content ---
st.title("CO2 Emissions Forecast")
st.write("This application forecasts CO2 emissions for selected countries using a Random Forest Regressor model.")

# Filter data based on selection
filtered_df = df[(df['country'].isin(selected_countries)) & (df['year'] >= start_year) & (df['year'] <= end_year)]

# --- Model Training and Forecasting ---

# Prepare data for the model
model_df = filtered_df.copy()
features = ['year', 'gdp', 'population', 'primary_energy_consumption', 'energy_per_capita']
target = 'co2'

# Handle missing values
for col in features + [target]:
    model_df[col].fillna(model_df.groupby('country')[col].transform('mean'), inplace=True)
    model_df[col].fillna(model_df[col].mean(), inplace=True) # Fill remaining NaNs

X = model_df[features]
y = model_df[target]

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# --- Forecasting ---
forecast_results = {}
for country in selected_countries:
    country_df = model_df[model_df['country'] == country]
    if not country_df.empty:
        latest_data = country_df.iloc[-1]
        forecast_data = []
        for year in range(end_year + 1, end_year + forecast_horizon + 1):
            gdp = latest_data['gdp'] * (1.02 ** (year - latest_data['year']))
            population = latest_data['population'] * (1.01 ** (year - latest_data['year']))
            energy_use = latest_data['primary_energy_consumption'] * (1.02 ** (year - latest_data['year']))
            energy_per_capita = latest_data['energy_per_capita'] * (1.05 ** (year - latest_data['year']))
            
            prediction = model.predict([[year, gdp, population, energy_use, energy_per_capita]])
            forecast_data.append({'year': year, 'predicted_co2': prediction[0]})
            
            latest_data = {
                'year': year,
                'gdp': gdp,
                'population': population,
                'primary_energy_consumption': energy_use,
                'energy_per_capita': energy_per_capita
            }
        forecast_results[country] = pd.DataFrame(forecast_data)

# --- Visualization ---
st.subheader("Historical and Forecasted CO2 Emissions")

fig, ax = plt.subplots(figsize=(12, 8))

for country in selected_countries:
    # Plot historical data
    hist_df = filtered_df[filtered_df['country'] == country]
    ax.plot(hist_df['year'], hist_df['co2'], label=f"Historical CO2 Emissions - {country}")
    
    # Plot forecasted data
    if country in forecast_results:
        forecast_df = forecast_results[country]
        ax.plot(forecast_df['year'], forecast_df['predicted_co2'], linestyle='--', label=f"Forecasted CO2 Emissions - {country}")

ax.set_title("CO2 Emissions Forecast")
ax.set_xlabel("Year")
ax.set_ylabel("CO2 Emissions (in million tonnes)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# --- Display Data ---
st.subheader("Raw and Forecasted Data")
st.write(filtered_df)

if forecast_results:
    st.subheader("Forecasted Data")
    for country, forecast_df in forecast_results.items():
        st.write(f"**{country}**")
        st.write(forecast_df)