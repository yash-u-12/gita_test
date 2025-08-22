#!/usr/bin/env python3
"""
Test script to debug user profile creation in database
"""
import sys
import os
import uuid

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client
from database.db_utils import db_manager

def test_user_profile_creation():
    print("Testing user profile creation in database...")
    
    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Generate test user data
    test_email = f"test{uuid.uuid4().hex[:8]}@example.com"
    test_password = "testpassword123"
    test_name = "Test User"
    
    print(f"Test email: {test_email}")
    print(f"Test password: {test_password}")
    print(f"Test name: {test_name}")
    
    try:
        # Step 1: Create auth user
        print("\n1. Creating auth user...")
        auth_response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password
        })
        
        if auth_response and hasattr(auth_response, "user") and auth_response.user:
            user_id = auth_response.user.id
            print(f"Auth user created with ID: {user_id}")
            
            # Step 2: Create user profile in database
            print("\n2. Creating user profile in database...")
            try:
                created_user = db_manager.create_user_if_not_exists(
                    user_id=user_id,
                    name=test_name,
                    email=test_email
                )
                print(f"User profile creation result: {created_user}")
                
                # Step 3: Try to find the user profile
                print("\n3. Searching for user profile...")
                found_user = db_manager.get_user_by_id(user_id)
                print(f"Found user by ID: {found_user}")
                
                found_user_by_email = db_manager.get_user_by_email(test_email)
                print(f"Found user by email: {found_user_by_email}")
                
            except Exception as db_error:
                print(f"Database error: {db_error}")
                
        else:
            print("Failed to create auth user")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_user_profile_creation()

