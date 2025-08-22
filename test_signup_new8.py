
#!/usr/bin/env python3
"""
Test script to create the new8@gmail.com user
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client
from database.db_utils import db_manager

def create_test_user():
    print("=== Creating Test User: new8@gmail.com ===")
    
    test_email = "new8@gmail.com"
    test_password = "testpassword123"
    test_name = "New User 8"
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    try:
        # Create auth user
        print(f"Creating auth user for: {test_email}")
        auth_response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password
        })
        
        if auth_response and auth_response.user:
            user_id = auth_response.user.id
            print(f"✅ Auth user created with ID: {user_id}")
            
            # Create user profile
            print("Creating user profile...")
            created = db_manager.create_user_if_not_exists(
                user_id=user_id,
                name=test_name,
                email=test_email
            )
            
            if created:
                print(f"✅ User profile created: {created}")
                print(f"✅ User {test_email} can now sign in with password: {test_password}")
            else:
                print("❌ Failed to create user profile")
                
        else:
            print("❌ Failed to create auth user")
            
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            print(f"✅ User {test_email} already exists in auth system")
            print("Now checking if profile exists...")
            
            # Try to sign in to get user ID
            try:
                auth_response = supabase.auth.sign_in_with_password({
                    "email": test_email,
                    "password": test_password
                })
                
                if auth_response and auth_response.user:
                    user_id = auth_response.user.id
                    
                    # Check if profile exists
                    existing = db_manager.get_user_by_id(user_id)
                    if not existing:
                        print("Creating missing profile...")
                        created = db_manager.create_user_if_not_exists(
                            user_id=user_id,
                            name=test_name,
                            email=test_email
                        )
                        if created:
                            print(f"✅ Profile created: {created}")
                    else:
                        print(f"✅ Profile already exists: {existing}")
                        
            except Exception as signin_error:
                print(f"❌ Could not sign in to check profile: {signin_error}")
        else:
            print(f"❌ Signup error: {e}")

if __name__ == "__main__":
    create_test_user()
