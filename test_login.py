#!/usr/bin/env python3
"""
Test script to debug login issues with different phone number formats.
"""

import requests
import json
from api_client import SwechaAPIClient

def test_login_variations():
    """Test login with different phone number formats and password variations"""
    
    print("🔍 Testing Login Variations...")
    print("=" * 50)
    
    # Test variations
    test_cases = [
        {"phone": "9491418067", "password": "Yashugupta1206", "desc": "Original format"},
        {"phone": "+919491418067", "password": "Yashugupta1206", "desc": "With country code"},
        {"phone": "919491418067", "password": "Yashugupta1206", "desc": "With country code no plus"},
        {"phone": "9491418067", "password": "Yashugupta@1206", "desc": "With @ symbol"},
        {"phone": "9491418067", "password": "yashugupta1206", "desc": "Lowercase password"},
    ]
    
    api_client = SwechaAPIClient()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['desc']}")
        print(f"   Phone: {test_case['phone']}")
        print(f"   Password: {test_case['password']}")
        
        try:
            response = api_client.login(test_case['phone'], test_case['password'])
            print(f"   📊 Response: {json.dumps(response, indent=2)}")
            
            if response.get("success"):
                print("   ✅ LOGIN SUCCESSFUL!")
                print(f"   🔑 Token: {api_client.auth_token[:20]}..." if api_client.auth_token else "   🔑 No token")
                print(f"   👤 User ID: {api_client.user_data.get('id', 'N/A')}" if api_client.user_data else "   👤 No user data")
                return True
            else:
                print("   ❌ Login failed")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("❌ All login attempts failed!")
    print("\nPossible issues:")
    print("1. Account doesn't exist")
    print("2. Wrong phone number format")
    print("3. Wrong password")
    print("4. Account needs to be created first")
    
    return False

def test_signup_flow():
    """Test if we can create a new account"""
    print("\n🔍 Testing Signup Flow...")
    print("=" * 30)
    
    api_client = SwechaAPIClient()
    
    # Test sending OTP for signup
    test_phone = "9491418067"
    print(f"Testing signup OTP for: {test_phone}")
    
    try:
        response = api_client.send_signup_otp(test_phone)
        print(f"📊 Signup OTP response: {json.dumps(response, indent=2)}")
        
        if response.get("success"):
            print("✅ OTP sent successfully!")
            print("📱 Check your phone for OTP")
        else:
            print("❌ Failed to send OTP")
            print("   This might mean the account already exists")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    print("Testing login variations...")
    success = test_login_variations()
    
    if not success:
        print("\nTrying signup flow...")
        test_signup_flow()
