#!/usr/bin/env python3
"""
Test script to verify exact credentials and signup process
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

def test_exact_credentials():
    print("Testing exact credentials...")
    
    # Test email and password that user is trying
    test_email = "new5@gmail.com"
    test_password = "testpassword123"  # Assuming this is the password
    
    print(f"Testing email: {test_email}")
    print(f"Testing password: {test_password}")
    
    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # First, try to sign in (this should fail if user doesn't exist)
    print("\n1. Testing signin (should fail if user doesn't exist)...")
    try:
        signin_response = supabase.auth.sign_in_with_password({
            "email": test_email,
            "password": test_password
        })
        print(f"Signin successful: {signin_response}")
    except Exception as e:
        print(f"Signin failed (expected): {e}")
    
    # Now try to sign up with these exact credentials
    print("\n2. Testing signup with exact credentials...")
    try:
        signup_response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password
        })
        print(f"Signup response: {signup_response}")
        
        if hasattr(signup_response, 'user') and signup_response.user:
            print(f"User created with ID: {signup_response.user.id}")
            
            # Now try to sign in immediately
            print("\n3. Testing immediate signin after signup...")
            try:
                immediate_signin = supabase.auth.sign_in_with_password({
                    "email": test_email,
                    "password": test_password
                })
                print(f"Immediate signin successful: {immediate_signin}")
            except Exception as immediate_error:
                print(f"Immediate signin failed: {immediate_error}")
        else:
            print("No user created during signup")
            
    except Exception as e:
        print(f"Signup failed: {e}")

if __name__ == "__main__":
    test_exact_credentials()

