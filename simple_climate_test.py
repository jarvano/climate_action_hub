#!/usr/bin/env python3
"""
Simple test script for climate data integration
Tests the new temperature and sea level HTML content
"""

import sys
from pathlib import Path

def test_html_content():
    """Test that HTML pages contain the new climate data sections"""
    print("🌍 Climate Data Integration Test Suite")
    print("=" * 50)
    
    base_dir = Path(__file__).parent
    pages_to_test = [
        ("insights.html", [
            "temperatureChart", 
            "seaLevelChart", 
            "Global Temperature Anomalies", 
            "Sea Level Rise Trends",
            "🌡️ Global Temperature Anomalies",
            "🌊 Sea Level Rise Trends"
        ]),
        ("dashboard.html", [
            "temperatureChart", 
            "seaLevelChart", 
            "🌡️ Global Temperature Anomalies", 
            "🌊 Sea Level Rise Trends",
            "initTemperatureChart",
            "initSeaLevelChart"
        ])
    ]
    
    all_tests_passed = True
    
    for page, required_content in pages_to_test:
        try:
            print(f"\n📄 Testing {page}...")
            
            file_path = base_dir / page
            if not file_path.exists():
                print(f"❌ {page} file not found")
                all_tests_passed = False
                continue
            
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
                all_tests_passed = False
                
            # Additional checks for dashboard
            if page == "dashboard.html":
                # Check for chart initialization
                if "initTemperatureChart()" in content and "initSeaLevelChart()" in content:
                    print(f"✅ {page} has proper chart initialization")
                else:
                    print(f"❌ {page} missing chart initialization")
                    all_tests_passed = False
                
                # Check for temperature stats
                temp_stats = ["tempAnomaly2023", "arcticAnomaly2023", "seaLevelRise2023", "islandRise2023"]
                missing_stats = [stat for stat in temp_stats if stat not in content]
                if not missing_stats:
                    print(f"✅ {page} has all temperature and sea level statistics")
                else:
                    print(f"❌ {page} missing statistics: {missing_stats}")
                    all_tests_passed = False
                    
            # Additional checks for insights
            if page == "insights.html":
                # Check for key findings sections
                key_findings = [
                    "Global average temperature has increased by approximately 1.1°C since pre-industrial times",
                    "Arctic warming is occurring at twice the global average rate",
                    "Global sea levels have risen by approximately 94.9mm since 1993",
                    "Small island developing states experience 30% higher sea level rise"
                ]
                missing_findings = [finding for finding in key_findings if finding not in content]
                if not missing_findings:
                    print(f"✅ {page} has all key findings")
                else:
                    print(f"❌ {page} missing key findings: {missing_findings}")
                    all_tests_passed = False
                
        except Exception as e:
            print(f"❌ Error testing {page}: {e}")
            all_tests_passed = False
    
    # Test climate data processor file
    print(f"\n📊 Testing climate_data_processor.py...")
    processor_path = base_dir / "src" / "climate_data_processor.py"
    if processor_path.exists():
        try:
            with open(processor_path, 'r', encoding='utf-8') as f:
                processor_content = f.read()
            
            # Check for key functions
            key_functions = ["load_co2_data", "generate_temperature_data", "load_sea_level_data", "get_climate_data"]
            missing_functions = [func for func in key_functions if func not in processor_content]
            
            if not missing_functions:
                print(f"✅ climate_data_processor.py has all required functions")
            else:
                print(f"❌ climate_data_processor.py missing functions: {missing_functions}")
                all_tests_passed = False
                
        except Exception as e:
            print(f"❌ Error testing climate_data_processor.py: {e}")
            all_tests_passed = False
    else:
        print(f"❌ climate_data_processor.py not found")
        all_tests_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    
    if all_tests_passed:
        print("\n🎉 All climate data integration tests passed!")
        print("✅ Temperature and sea level datasets have been successfully integrated")
        print("✅ Both insights.html and dashboard.html contain the new climate visualizations")
        print("✅ Climate data processor is properly structured")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(test_html_content())