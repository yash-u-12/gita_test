
#!/usr/bin/env python3
"""
Test script to verify login works without email confirmation
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client
from database.db_utils import db_manager

def test_login_fix():
    print("=== Testing Login Fix ===")
    
    test_email = "new7@gmail.com"
    test_password = "testpassword123"  # You'll need to know the actual password
    
    # Create client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    try:
        print(f"Testing signin for: {test_email}")
        
        # Clear any existing session
        try:
            supabase.auth.sign_out()
        except:
            pass
        
        # Attempt signin
        auth_response = supabase.auth.sign_in_with_password({
            "email": test_email, 
            "password": test_password
        })
        
        if auth_response and auth_response.user:
            user_id = auth_response.user.id
            print(f"✅ Authentication successful! User ID: {user_id}")
            
            # Check if user profile exists
            user_profile = db_manager.get_user_by_id(user_id)
            if user_profile:
                print(f"✅ User profile found: {user_profile}")
                print("✅ Login should work in the app now!")
            else:
                print("❌ User profile not found in database")
                
        else:
            print("❌ Authentication failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # If it's still failing due to invalid credentials, 
        # the user might need to reset their password
        if "Invalid login credentials" in str(e):
            print("\n💡 The user may need to reset their password.")
            print("Try using the password reset feature in the app.")

if __name__ == "__main__":
    test_login_fix()
