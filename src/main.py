import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Construct the absolute path to the data file
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, '..', 'data', 'owid-co2-data.csv')

# Load the dataset
df = pd.read_csv(data_path)

# --- Data Cleaning and Preprocessing ---

# 1. Select relevant columns
df = df[['country', 'year', 'co2', 'gdp', 'population', 'primary_energy_consumption', 'energy_per_capita']]

# 2. Rename columns for clarity
df.rename(columns={
    'country': 'Country',
    'year': 'Year',
    'co2': 'CO2_Emissions',
    'gdp': 'GDP',
    'population': 'Population',
    'primary_energy_consumption': 'Energy_Use',
    'energy_per_capita': 'Energy_Per_Capita'
}, inplace=True)

# 3. Handle missing values (e.g., fill with the mean of the column)
for col in ['GDP', 'Population', 'Energy_Use', 'Energy_Per_Capita', 'CO2_Emissions']:
    df[col].fillna(df[col].mean(), inplace=True)

# --- Feature Engineering ---
# For simplicity, we will use the existing features. More complex features could be engineered.

# --- Model Training ---

# 1. Define features (X) and target (y)
features = ['Year', 'GDP', 'Population', 'Energy_Use', 'Energy_Per_Capita']
target = 'CO2_Emissions'

X = df[features]
y = df[target]

# 2. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Initialize and train the models
# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# --- Model Evaluation ---

# Make predictions
lr_preds = lr_model.predict(X_test)
rf_preds = rf_model.predict(X_test)

# Evaluate models
print("Linear Regression:")
print(f"MAE: {mean_absolute_error(y_test, lr_preds)}")
print(f"R² Score: {r2_score(y_test, lr_preds)}")

print("\nRandom Forest Regressor:")
print(f"MAE: {mean_absolute_error(y_test, rf_preds)}")
print(f"R² Score: {r2_score(y_test, rf_preds)}")


# --- Forecasting Future Emissions ---

def forecast_emissions(country_name, model, start_year, end_year):
    country_df = df[df['Country'] == country_name].copy()
    
    # Use the latest available data for forecasting
    latest_data = country_df.iloc[-1]
    
    forecast_data = []
    for year in range(start_year, end_year + 1):
        # Simple assumption: GDP, Population, etc., grow at a fixed rate (e.g., 2% per year)
        gdp = latest_data['GDP'] * (1.02 ** (year - latest_data['Year']))
        population = latest_data['Population'] * (1.01 ** (year - latest_data['Year']))
        energy_use = latest_data['Energy_Use'] * (1.02 ** (year - latest_data['Year']))
        energy_per_capita = latest_data['Energy_Per_Capita'] * (1.05 ** (year - latest_data['Year']))
        
        prediction = model.predict([[year, gdp, population, energy_use, energy_per_capita]])
        forecast_data.append({'Year': year, 'Predicted_CO2_Emissions': prediction[0]})
        
        # Update latest_data for the next iteration
        latest_data = {
            'Year': year,
            'GDP': gdp,
            'Population': population,
            'Energy_Use': energy_use,
            'Energy_Per_Capita': energy_per_capita
        }
        
    return pd.DataFrame(forecast_data)

# Forecast for specific countries up to 2030
countries_to_forecast = ['Kenya', 'China', 'United States']
forecast_results = {}

for country in countries_to_forecast:
    forecast_results[country] = forecast_emissions(country, rf_model, df['Year'].max() + 1, 2030)
    print(f'\nForecast for {country}:')
    print(forecast_results[country])

# --- Visualization ---

plt.figure(figsize=(12, 8))

for country, forecast_df in forecast_results.items():
    historical_df = df[df['Country'] == country]
    plt.plot(historical_df['Year'], historical_df['CO2_Emissions'], label=f'Historical CO2 Emissions - {country}')
    plt.plot(forecast_df['Year'], forecast_df['Predicted_CO2_Emissions'], linestyle='--', label=f'Forecasted CO2 Emissions - {country}')

plt.title('CO2 Emissions Forecast up to 2030')
plt.xlabel('Year')
plt.ylabel('CO2 Emissions (in million tonnes)')
plt.legend()
plt.grid(True)
plt.savefig('co2_emissions_forecast.png')

# --- Ethical Reflection ---
# This section would be added as comments in the final script.
# 1. Data Bias: Data from developing countries might be less accurate or available,
#    leading to models that are less reliable for these regions. This can result in
#    unfair policy recommendations.
# 2. Policy Implications: Emission forecasts can help governments set realistic targets
#    and design data-driven climate policies. By identifying the main drivers of emissions,
#    they can create targeted interventions (e.g., promoting renewable energy).