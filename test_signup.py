#!/usr/bin/env python3
"""
Test script to debug Supabase signup process
"""
import sys
import os
import uuid

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

def test_signup():
    print("Testing Supabase signup process...")
    print(f"URL: {SUPABASE_URL}")
    
    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Generate test email
    test_email = f"test{uuid.uuid4().hex[:8]}@example.com"
    test_password = "testpassword123"
    
    print(f"Test email: {test_email}")
    print(f"Test password: {test_password}")
    
    try:
        # Attempt signup
        print("\nAttempting signup...")
        response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password
        })
        
        print(f"Signup response type: {type(response)}")
        print(f"Signup response: {response}")
        
        if hasattr(response, 'user') and response.user:
            print(f"User created: {response.user}")
            print(f"User ID: {response.user.id}")
            print(f"User email: {response.user.email}")
        else:
            print("No user created")
            
        if hasattr(response, 'session') and response.session:
            print(f"Session created: {response.session}")
        else:
            print("No session created (email confirmation likely required)")
            
        # Try to sign in immediately
        print("\nAttempting immediate signin...")
        try:
            signin_response = supabase.auth.sign_in_with_password({
                "email": test_email,
                "password": test_password
            })
            print(f"Signin successful: {signin_response}")
        except Exception as signin_error:
            print(f"Signin failed: {signin_error}")
            
    except Exception as e:
        print(f"Signup failed: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_signup()
