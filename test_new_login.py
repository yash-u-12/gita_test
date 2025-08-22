
#!/usr/bin/env python3
"""
Test script for the new login system
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client
from database.db_utils import db_manager

def test_new_login():
    print("=== Testing New Login System ===")
    
    # Test credentials
    test_email = "testuser@example.com"
    test_password = "testpass123"
    test_name = "Test User"
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("1. Creating test user...")
    try:
        # Create auth user
        auth_response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password
        })
        
        if auth_response and auth_response.user:
            user_id = auth_response.user.id
            print(f"✅ Auth user created: {user_id}")
            
            # Create user profile
            user_profile = db_manager.create_user_if_not_exists(
                user_id=user_id,
                name=test_name,
                email=test_email
            )
            
            if user_profile:
                print(f"✅ User profile created: {user_profile}")
            else:
                print("❌ Failed to create user profile")
        else:
            print("❌ Failed to create auth user")
            
    except Exception as e:
        if "already registered" in str(e).lower():
            print("✅ User already exists, testing login...")
        else:
            print(f"❌ Signup error: {e}")
    
    print("\n2. Testing login...")
    try:
        # Clear any existing session
        supabase.auth.sign_out()
        
        # Test login
        login_response = supabase.auth.sign_in_with_password({
            "email": test_email,
            "password": test_password
        })
        
        if login_response and login_response.user:
            user_id = login_response.user.id
            print(f"✅ Login successful: {user_id}")
            
            # Get user profile
            user_profile = db_manager.get_user_by_id(user_id)
            if user_profile:
                print(f"✅ User profile found: {user_profile}")
                print("✅ Login system working correctly!")
            else:
                print("❌ User profile not found")
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"❌ Login error: {e}")

if __name__ == "__main__":
    test_new_login()
