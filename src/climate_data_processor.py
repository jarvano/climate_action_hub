#!/usr/bin/env python3
"""
Enhanced Data Processor for Climate Action Hub
Processes CO2 emissions, temperature, and sea level data
"""

import csv
import json
import os
import numpy as np
from datetime import datetime

class ClimateDataProcessor:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, 'data')
        
    def load_co2_data(self):
        """Load CO2 emissions data from CSV file"""
        data_file = os.path.join(self.data_path, 'owid-co2-data.csv')
        
        if not os.path.exists(data_file):
            print(f"CO2 data file not found: {data_file}")
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
                    co2_per_capita = row.get('co2_per_capita', '')
                    co2_per_gdp = row.get('co2_per_gdp', '')
                    
                    # Convert to appropriate types
                    try:
                        co2_emissions = float(co2_emissions) if co2_emissions else None
                        population = float(population) if population else None
                        energy_consumption = float(energy_consumption) if energy_consumption else None
                        co2_per_capita = float(co2_per_capita) if co2_per_capita else None
                        co2_per_gdp = float(co2_per_gdp) if co2_per_gdp else None
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
                        "energy": energy_consumption,
                        "co2_per_capita": co2_per_capita,
                        "co2_per_gdp": co2_per_gdp
                    }
                    
                    countries_data[country]["historical"].append(data_point)
                
                # Sort data by year for each country
                for country in countries_data:
                    countries_data[country]["historical"].sort(key=lambda x: x["year"])
                
                return countries_data
                
        except Exception as e:
            print(f"Error loading CO2 data: {e}")
            return None
    
    def generate_temperature_data(self):
        """Generate synthetic temperature anomaly data"""
        years = list(range(1990, 2024))  # 1990 to 2023
        base_temp = 0.0
        
        temperature_data = []
        for i, year in enumerate(years):
            # Simulate accelerating warming trend
            trend = 0.02 * i  # 0.02°C per year trend
            noise = random.uniform(-0.1, 0.1)
            
            # Add some realistic variations (El Niño, etc.)
            if year in [1998, 2010, 2016, 2020]:
                trend += 0.15  # Strong El Niño years
            
            temperature = base_temp + trend + noise
            temperature_data.append({
                'year': year,
                'value': round(temperature, 2),
                'type': 'global'
            })
        
        return temperature_data
    
    def load_sea_level_data(self):
        """Load sea level rise data"""
        # This would typically load from satellite altimetry data
        # For now, we'll create synthetic sea level data
        print("Loading sea level data...")
        
        # Simulated global mean sea level rise (relative to 1993 baseline)
        # Based on satellite observations and tide gauge data trends
        base_sea_level_rise = {
            1993: 0.0, 1994: 2.1, 1995: 4.3, 1996: 6.8, 1997: 9.2,
            1998: 11.5, 1999: 14.1, 2000: 16.8, 2001: 19.5, 2002: 22.3,
            2003: 25.1, 2004: 28.0, 2005: 31.2, 2006: 34.5, 2007: 37.8,
            2008: 41.2, 2009: 44.6, 2010: 48.1, 2011: 51.5, 2012: 54.8,
            2013: 58.2, 2014: 61.8, 2015: 65.5, 2016: 69.1, 2017: 72.8,
            2018: 76.5, 2019: 80.2, 2020: 83.8, 2021: 87.5, 2022: 91.2,
            2023: 94.9
        }
        
        return {
            "global_mean_sea_level_rise": base_sea_level_rise,
            "baseline_year": 1993,
            "unit": "mm",
            "rate_of_rise": "3.4 mm/year (average since 1993)"
        }
    
    def generate_regional_temperature_data(self, co2_data):
        """Generate regional temperature data based on CO2 emissions patterns"""
        regional_temp_data = {}
        
        # Temperature anomaly multipliers for different regions
        regional_multipliers = {
            "Arctic": 2.0,      # Arctic amplification effect
            "North America": 1.1,
            "Europe": 1.2,
            "Asia": 1.0,
            "Africa": 0.9,
            "South America": 0.8,
            "Oceania": 1.0,
            "Antarctica": 1.5
        }
        
        # Assign regions to countries (simplified mapping)
        country_to_region = {
            "United States": "North America", "Canada": "North America", "Mexico": "North America",
            "China": "Asia", "India": "Asia", "Japan": "Asia", "South Korea": "Asia",
            "Russia": "Arctic", "Norway": "Arctic", "Sweden": "Arctic", "Finland": "Arctic",
            "Germany": "Europe", "United Kingdom": "Europe", "France": "Europe", "Italy": "Europe",
            "Brazil": "South America", "Argentina": "South America",
            "Australia": "Oceania", "New Zealand": "Oceania",
            "South Africa": "Africa", "Nigeria": "Africa", "Kenya": "Africa",
            "Saudi Arabia": "Asia", "Iran": "Asia", "Turkey": "Asia"
        }
        
        global_temp = self.load_temperature_data()
        
        for country, data in co2_data.items():
            if country in country_to_region:
                region = country_to_region[country]
                multiplier = regional_multipliers.get(region, 1.0)
                
                country_temp_data = []
                for point in data["historical"]:
                    year = point["year"]
                    if year in global_temp["global_temperature_anomaly"]:
                        base_anomaly = global_temp["global_temperature_anomaly"][year]
                        regional_anomaly = base_anomaly * multiplier
                        
                        country_temp_data.append({
                            "year": year,
                            "temperature_anomaly": round(regional_anomaly, 2),
                            "region": region
                        })
                
                if country_temp_data:
                    regional_temp_data[country] = {
                        "historical": country_temp_data,
                        "region": region,
                        "average_multiplier": multiplier
                    }
        
        return regional_temp_data
    
    def generate_regional_sea_level_data(self, co2_data):
        """Generate regional sea level data based on geographic factors"""
        regional_sea_data = {}
        
        # Sea level rise varies by region due to ocean currents, glacial rebound, etc.
        regional_sea_multipliers = {
            "Pacific Islands": 1.5,    # Higher vulnerability
            "Indian Ocean": 1.3,
            "Atlantic": 1.1,
            "Mediterranean": 1.2,
            "Caribbean": 1.4,
            "Arctic": 0.8,             # Less rise due to land rebound
            "Antarctic": 0.9
        }
        
        # Assign coastal regions to countries
        country_to_coastal_region = {
            "United States": "Atlantic", "Canada": "Atlantic", "Mexico": "Caribbean",
            "Japan": "Pacific Islands", "Australia": "Pacific Islands", "Indonesia": "Pacific Islands",
            "India": "Indian Ocean", "South Africa": "Indian Ocean",
            "United Kingdom": "Atlantic", "France": "Atlantic", "Italy": "Mediterranean",
            "Brazil": "Atlantic", "Argentina": "Atlantic",
            "China": "Pacific Islands", "South Korea": "Pacific Islands"
        }
        
        global_sea = self.load_sea_level_data()
        
        for country, data in co2_data.items():
            if country in country_to_coastal_region:
                coastal_region = country_to_coastal_region[country]
                multiplier = regional_sea_multipliers.get(coastal_region, 1.0)
                
                country_sea_data = []
                for point in data["historical"]:
                    year = point["year"]
                    if year in global_sea["global_mean_sea_level_rise"]:
                        base_rise = global_sea["global_mean_sea_level_rise"][year]
                        regional_rise = base_rise * multiplier
                        
                        country_sea_data.append({
                            "year": year,
                            "sea_level_rise": round(regional_rise, 1),
                            "coastal_region": coastal_region,
                            "vulnerability_level": "High" if multiplier > 1.3 else "Medium" if multiplier > 1.0 else "Low"
                        })
                
                if country_sea_data:
                    regional_sea_data[country] = {
                        "historical": country_sea_data,
                        "coastal_region": coastal_region,
                        "vulnerability_level": "High" if multiplier > 1.3 else "Medium" if multiplier > 1.0 else "Low",
                        "sea_level_multiplier": multiplier
                    }
        
        return regional_sea_data
    
    def get_comprehensive_climate_data(self):
        """Get comprehensive climate data including CO2, temperature, and sea level data"""
        print("Loading comprehensive climate data...")
        
        # Load CO2 data
        co2_data = self.load_co2_data()
        if not co2_data:
            return None
        
        # Generate temperature and sea level data
        temp_data = self.generate_regional_temperature_data(co2_data)
        sea_level_data = self.generate_regional_sea_level_data(co2_data)
        global_temp = self.load_temperature_data()
        global_sea = self.load_sea_level_data()
        
        # Combine all data
        comprehensive_data = {
            "co2_data": co2_data,
            "temperature_data": temp_data,
            "sea_level_data": sea_level_data,
            "global_metrics": {
                "temperature": global_temp,
                "sea_level": global_sea
            },
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "data_sources": [
                    "OWID CO2 Dataset",
                    "Simulated Temperature Data (based on NOAA trends)",
                    "Simulated Sea Level Data (based on NASA/NOAA trends)"
                ],
                "coverage": {
                    "countries": len(co2_data),
                    "temperature_regions": len(temp_data),
                    "coastal_regions": len(sea_level_data),
                    "year_range": self._get_year_range(co2_data)
                }
            }
        }
        
        return comprehensive_data
    
    def _get_year_range(self, data):
        """Get the year range from the data"""
        all_years = set()
        for country_data in data.values():
            for point in country_data["historical"]:
                all_years.add(point["year"])
        
        if all_years:
            return [min(all_years), max(all_years)]
        return [1990, 2023]
    
    def get_climate_data(self):
        """Get all climate data in a single structure"""
        co2_data = self.load_co2_data()
        temp_data = self.generate_temperature_data()
        sea_data = self.load_sea_level_data()
        
        return {
            'co2': co2_data,
            'temperature': temp_data,
            'sea_level': sea_data,
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'data_sources': ['CO2 emissions dataset', 'Synthetic temperature data', 'Simulated sea level data'],
                'note': 'Temperature and sea level data are synthetic for demonstration purposes'
            }
        }

    def get_climate_summary(self, data):
        """Get summary statistics for climate data"""
        if not data:
            return None
        
        summary = {
            "total_countries": len(data.get("co2_data", {})),
            "temperature_coverage": len(data.get("temperature_data", {})),
            "sea_level_coverage": len(data.get("sea_level_data", {})),
            "global_temperature_trend": "warming",
            "global_sea_level_trend": "rising",
            "key_findings": [
                "Global temperature has risen by approximately 1.1°C since pre-industrial times",
                "Global sea level has risen by approximately 95mm since 1993",
                "CO2 emissions continue to drive climate change across all regions",
                "Arctic regions are warming at twice the global average rate",
                "Small island nations face the highest sea level rise vulnerability"
            ]
        }
        
        return summary

if __name__ == "__main__":
    processor = ClimateDataProcessor()
    
    # Test comprehensive data loading
    comprehensive_data = processor.get_comprehensive_climate_data()
    
    if comprehensive_data:
        print("\n" + "="*60)
        print("COMPREHENSIVE CLIMATE DATA LOADED SUCCESSFULLY")
        print("="*60)
        
        summary = processor.get_climate_summary(comprehensive_data)
        
        print(f"Countries with CO2 data: {summary['total_countries']}")
        print(f"Countries with temperature data: {summary['temperature_coverage']}")
        print(f"Countries with sea level data: {summary['sea_level_coverage']}")
        print(f"Year range: {summary.get('year_range', 'N/A')}")
        
        print("\nKey Climate Findings:")
        for finding in summary['key_findings']:
            print(f"  • {finding}")
        
        # Sample data for a few countries
        sample_countries = ["United States", "China", "India"]
        print(f"\nSample data for {', '.join(sample_countries)}:")
        
        for country in sample_countries:
            if country in comprehensive_data['co2_data']:
                co2_data = comprehensive_data['co2_data'][country]['historical']
                temp_data = comprehensive_data['temperature_data'].get(country, {})
                sea_data = comprehensive_data['sea_level_data'].get(country, {})
                
                print(f"\n{country}:")
                print(f"  CO2 data points: {len(co2_data)}")
                print(f"  Temperature data: {'Available' if temp_data else 'Not available'}")
                print(f"  Sea level data: {'Available' if sea_data else 'Not available'}")
                
                if co2_data:
                    latest = co2_data[-1]
                    print(f"  Latest data (Year {latest['year']}): CO2 = {latest['co2']:.2f} Mt")
                
                if temp_data and temp_data.get('historical'):
                    latest_temp = temp_data['historical'][-1]
                    print(f"  Latest temperature anomaly: {latest_temp['temperature_anomaly']}°C")
                
                if sea_data and sea_data.get('historical'):
                    latest_sea = sea_data['historical'][-1]
                    print(f"  Latest sea level rise: {latest_sea['sea_level_rise']}mm")
        
        print(f"\nGlobal metrics available: {list(comprehensive_data['global_metrics'].keys())}")
        
    else:
        print("❌ Failed to load comprehensive climate data")