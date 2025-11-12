#!/usr/bin/env python3
"""
Data processor to load and serve real CO2 data from CSV without external dependencies
"""
import csv
import json
import os

def load_co2_data():
    """Load CO2 data from CSV file using built-in csv module"""
    data_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'owid-co2-data.csv')
    
    if not os.path.exists(data_file):
        print(f"Data file not found: {data_file}")
        return None
    
    countries_data = {}
    
    try:
        with open(data_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                country = row.get('country', '')
                year = row.get('year', '')
                
                if not country or not year:
                    continue
                
                try:
                    year = int(year)
                except (ValueError, TypeError):
                    continue
                
                # Skip aggregated regions and focus on major countries
                if country in ['World', 'Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania']:
                    continue
                
                # Extract relevant data
                co2_emissions = row.get('co2', '')
                population = row.get('population', '')
                energy_consumption = row.get('primary_energy_consumption', '')
                
                # Convert to appropriate types
                try:
                    co2_emissions = float(co2_emissions) if co2_emissions else None
                    population = float(population) if population else None
                    energy_consumption = float(energy_consumption) if energy_consumption else None
                except (ValueError, TypeError):
                    continue
                
                # Only include rows with meaningful CO2 data
                if co2_emissions is None or co2_emissions <= 0:
                    continue
                
                if country not in countries_data:
                    countries_data[country] = {
                        "historical": []
                    }
                
                data_point = {
                    "year": year,
                    "co2": co2_emissions,
                    "population": population,
                    "energy": energy_consumption
                }
                
                countries_data[country]["historical"].append(data_point)
            
            # Sort data by year for each country
            for country in countries_data:
                countries_data[country]["historical"].sort(key=lambda x: x["year"])
            
            return countries_data
            
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_major_countries_data():
    """Get data for all countries with CO2 data"""
    all_data = load_co2_data()
    if not all_data:
        return None
    
    # Return all countries that have data
    available_countries = []
    filtered_data = {}
    
    # Include all countries with at least 5 years of data for better user experience
    for country, data in all_data.items():
        if len(data["historical"]) >= 5:  # Minimum 5 years of data
            available_countries.append(country)
            filtered_data[country] = data
    
    # Sort countries alphabetically for better UX
    available_countries.sort()
    
    # Get year range from all available data
    all_years = set()
    for country_data in filtered_data.values():
        for point in country_data["historical"]:
            all_years.add(point["year"])
    
    years = sorted(list(all_years))
    
    return {
        "countries": available_countries,
        "years": years,
        "data": filtered_data
    }

if __name__ == "__main__":
    # Test the data processor
    data = get_major_countries_data()
    if data:
        print(f"Loaded data for {len(data['countries'])} countries")
        print(f"Countries: {', '.join(data['countries'][:10])}...")
        print(f"Year range: {min(data['years'])} - {max(data['years'])}")
    else:
        print("Failed to load data")