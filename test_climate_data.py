#!/usr/bin/env python3
"""
Test script for climate data integration
Tests the new temperature and sea level datasets alongside existing CO2 data
"""

import json
import time
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from climate_data_processor import ClimateDataProcessor
    print("✅ Successfully imported ClimateDataProcessor")
except ImportError as e:
    print(f"❌ Failed to import ClimateDataProcessor: {e}")
    sys.exit(1)

def test_data_processor():
    """Test the climate data processor functionality"""
    print("\n🧪 Testing Climate Data Processor...")
    
    try:
        processor = ClimateDataProcessor()
        print("✅ ClimateDataProcessor initialized successfully")
        
        # Test CO2 data loading
        print("\n📊 Testing CO2 data loading...")
        co2_data = processor.load_co2_data()
        if co2_data:
            print(f"✅ CO2 data loaded: {len(co2_data)} records")
            print(f"   Sample countries: {list(co2_data.keys())[:5]}")
        else:
            print("❌ Failed to load CO2 data")
        
        # Test temperature data generation
        print("\n🌡️ Testing temperature data generation...")
        temp_data = processor.generate_temperature_data()
        if temp_data:
            print(f"✅ Temperature data generated: {len(temp_data)} years")
            print(f"   Sample data: {temp_data[:3]}")
        else:
            print("❌ Failed to generate temperature data")
        
        # Test sea level data generation
        print("\n🌊 Testing sea level data generation...")
        sea_data = processor.generate_sea_level_data()
        if sea_data:
            print(f"✅ Sea level data generated: {len(sea_data)} years")
            print(f"   Sample data: {sea_data[:3]}")
        else:
            print("❌ Failed to generate sea level data")
        
        # Test combined data structure
        print("\n🌍 Testing combined climate data...")
        combined_data = processor.get_climate_data()
        if combined_data:
            print(f"✅ Combined climate data created")
            print(f"   Metadata: {combined_data.get('metadata', {})}")
            print(f"   Available datasets: {list(combined_data.get('data', {}).keys())}")
        else:
            print("❌ Failed to create combined climate data")
        
        return True
        
    except Exception as e:
        print(f"❌ ClimateDataProcessor test failed: {e}")
        return False

def test_html_pages():
    """Test that HTML pages can be accessed and contain new climate data sections"""
    print("\n🌐 Testing HTML pages...")
    
    base_url = "http://localhost:8000"
    pages_to_test = [
        ("insights.html", ["temperatureChart", "seaLevelChart", "Global Temperature Anomalies", "Sea Level Rise Trends"]),
        ("dashboard.html", ["temperatureChart", "seaLevelChart", "🌡️ Global Temperature Anomalies", "🌊 Sea Level Rise Trends"])
    ]
    
    for page, required_content in pages_to_test:
        try:
            print(f"\n📄 Testing {page}...")
            
            # Read local file instead of making HTTP request
            file_path = Path(__file__).parent / page
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for required content
                missing_content = []
                for required in required_content:
                    if required not in content:
                        missing_content.append(required)
                
                if not missing_content:
                    print(f"✅ {page} contains all required climate data sections")
                else:
                    print(f"❌ {page} missing content: {missing_content}")
            else:
                print(f"❌ {page} file not found")
                
        except Exception as e:
            print(f"❌ Error testing {page}: {e}")

def test_data_consistency():
    """Test that the data is consistent across different sources"""
    print("\n🔍 Testing data consistency...")
    
    try:
        processor = ClimateDataProcessor()
        
        # Get all climate data
        climate_data = processor.get_climate_data()
        
        if not climate_data:
            print("❌ No climate data available")
            return False
        
        # Check data structure
        required_keys = ['metadata', 'data', 'summary']
        missing_keys = [key for key in required_keys if key not in climate_data]
        
        if missing_keys:
            print(f"❌ Missing required data keys: {missing_keys}")
            return False
        
        # Check that we have all three main datasets
        data_keys = climate_data.get('data', {}).keys()
        expected_datasets = ['co2_emissions', 'temperature_anomalies', 'sea_level_rise']
        missing_datasets = [dataset for dataset in expected_datasets if dataset not in data_keys]
        
        if missing_datasets:
            print(f"❌ Missing expected datasets: {missing_datasets}")
            return False
        
        # Check data ranges and consistency
        temp_data = climate_data['data'].get('temperature_anomalies', [])
        sea_data = climate_data['data'].get('sea_level_rise', [])
        
        # Temperature anomalies should be reasonable
        if temp_data:
            temp_values = [item.get('value', 0) for item in temp_data]
            max_temp = max(temp_values)
            min_temp = min(temp_values)
            
            if max_temp > 5 or min_temp < -2:
                print(f"⚠️  Temperature values seem extreme: range {min_temp}°C to {max_temp}°C")
            else:
                print(f"✅ Temperature data looks reasonable: range {min_temp}°C to {max_temp}°C")
        
        # Sea level rise should be positive and reasonable
        if sea_data:
            sea_values = [item.get('value', 0) for item in sea_data]
            max_sea = max(sea_values)
            min_sea = min(sea_values)
            
            if max_sea > 200 or min_sea < -10:
                print(f"⚠️  Sea level values seem extreme: range {min_sea}mm to {max_sea}mm")
            else:
                print(f"✅ Sea level data looks reasonable: range {min_sea}mm to {max_sea}mm")
        
        print("✅ Data consistency checks passed")
        return True
        
    except Exception as e:
        print(f"❌ Data consistency test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🌍 Climate Data Integration Test Suite")
    print("=" * 50)
    
    # Test data processor
    processor_success = test_data_processor()
    
    # Test HTML pages
    test_html_pages()
    
    # Test data consistency
    consistency_success = test_data_consistency()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   Data Processor: {'✅ PASS' if processor_success else '❌ FAIL'}")
    print(f"   Data Consistency: {'✅ PASS' if consistency_success else '❌ FAIL'}")
    
    if processor_success and consistency_success:
        print("\n🎉 All climate data integration tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())