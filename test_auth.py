#!/usr/bin/env python3
"""
Demo script to test the Flask authentication system
"""

import requests
import json
import time

def test_authentication_system():
    """Test the authentication system endpoints"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Climate Action Hub Authentication System")
    print("=" * 60)
    
    # Test 1: Check if server is running
    print("\n1. Testing server status...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start it with: python auth_app.py")
        return
    
    # Test 2: Test registration
    print("\n2. Testing user registration...")
    registration_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123',
        'confirm_password': 'testpassword123'
    }
    
    try:
        response = requests.post(f"{base_url}/register", data=registration_data)
        if response.status_code == 200:
            print("✅ Registration successful")
        elif response.status_code == 400:
            print("⚠️  User might already exist, continuing with login test")
        else:
            print(f"❌ Registration failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Registration error: {e}")
    
    # Test 3: Test login
    print("\n3. Testing user login...")
    login_data = {
        'username': 'testuser',
        'password': 'testpassword123'
    }
    
    session = requests.Session()
    try:
        response = session.post(f"{base_url}/login", data=login_data)
        if response.status_code == 200:
            print("✅ Login successful")
            print(f"   Session cookies: {dict(session.cookies)}")
        else:
            print(f"❌ Login failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Test 4: Test dashboard access
    print("\n4. Testing dashboard access...")
    try:
        response = session.get(f"{base_url}/dashboard")
        if response.status_code == 200:
            print("✅ Dashboard accessible")
            print(f"   Dashboard contains 'Welcome' text: {'Welcome' in response.text}")
        else:
            print(f"❌ Dashboard access failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard access error: {e}")
    
    # Test 5: Test preferences
    print("\n5. Testing preferences page...")
    try:
        response = session.get(f"{base_url}/preferences")
        if response.status_code == 200:
            print("✅ Preferences page accessible")
            print(f"   Contains theme options: {'theme' in response.text}")
        else:
            print(f"❌ Preferences page failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Preferences page error: {e}")
    
    # Test 6: Test logout
    print("\n6. Testing logout...")
    try:
        response = session.get(f"{base_url}/logout")
        if response.status_code == 200:
            print("✅ Logout successful")
        else:
            print(f"❌ Logout failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Logout error: {e}")
    
    # Test 7: Test dashboard access after logout
    print("\n7. Testing dashboard access after logout...")
    try:
        response = session.get(f"{base_url}/dashboard")
        if response.status_code == 302 or response.status_code == 401:
            print("✅ Dashboard correctly redirects after logout")
        else:
            print(f"❌ Dashboard access after logout failed with status: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard access after logout error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Authentication system test completed!")
    print("\nNext steps:")
    print("1. Start the Flask server: python auth_app.py")
    print("2. Visit http://localhost:5000/login")
    print("3. Register a new user account")
    print("4. Explore the dashboard and preferences")
    print("5. Test saving analyses and customizations")

if __name__ == "__main__":
    test_authentication_system()