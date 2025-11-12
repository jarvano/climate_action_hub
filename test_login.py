#!/usr/bin/env python3
"""
Test script to verify the login functionality and access user pages
"""

import requests
import json

# Test the login functionality
session = requests.Session()

# Test login
login_data = {
    'username': 'admin',
    'password': 'admin123',
    'remember': 'true'
}

print("Testing login...")
try:
    # Login
    response = session.post('http://localhost:5000/login', data=login_data)
    print(f"Login response status: {response.status_code}")
    
    if response.status_code == 200:
        print("Login successful!")
        
        # Test accessing dashboard
        print("Testing dashboard access...")
        dashboard_response = session.get('http://localhost:5000/dashboard')
        print(f"Dashboard response status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            print("Dashboard accessible!")
            
            # Test other user pages
            pages = ['profile', 'analytics', 'saved_analyses']
            for page in pages:
                print(f"Testing {page} page...")
                page_response = session.get(f'http://localhost:5000/{page}')
                print(f"{page} response status: {page_response.status_code}")
                
        else:
            print("Dashboard not accessible - may need authentication")
            
    else:
        print("Login failed")
        
except Exception as e:
    print(f"Error during testing: {e}")

print("Test completed!")