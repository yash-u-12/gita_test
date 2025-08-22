
#!/usr/bin/env python3
"""
Test script to debug and fix the specific signin issue
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client
from database.db_utils import db_manager

def test_signin_fix():
    print("=== Testing Signin Fix ===")
    
    # Test with the problematic email
    test_email = "new7@gmail.com"
    test_password = "testpassword123"  # Common test password
    
    print(f"Testing signin for: {test_email}")
    
    # Create clients
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    try:
        # Clear any existing session
        supabase.auth.sign_out()
        print("Cleared existing session")
    except:
        pass
    
    # Test signin
    try:
        print(f"Attempting signin with email: {test_email}")
        auth_response = supabase.auth.sign_in_with_password({
            "email": test_email, 
            "password": test_password
        })
        
        print(f"✅ Signin successful!")
        print(f"User ID: {auth_response.user.id}")
        print(f"Email confirmed: {auth_response.user.email_confirmed_at is not None}")
        
        # Check if user exists in database
        existing_user = db_manager.get_user_by_id(auth_response.user.id)
        print(f"User in database: {existing_user is not None}")
        
        if not existing_user:
            print("Creating user profile in database...")
            created = db_manager.create_user_if_not_exists(
                user_id=auth_response.user.id,
                name=f"User {auth_response.user.email.split('@')[0]}",
                email=auth_response.user.email
            )
            print(f"Profile created: {created is not None}")
        
    except Exception as e:
        print(f"❌ Signin failed: {e}")
        
        # Try different common passwords
        common_passwords = ["password123", "123456", "password", "test123"]
        
        for pwd in common_passwords:
            try:
                print(f"Trying password: {pwd}")
                auth_response = supabase.auth.sign_in_with_password({
                    "email": test_email, 
                    "password": pwd
                })
                print(f"✅ Success with password: {pwd}")
                break
            except:
                continue
        else:
            print("❌ No common passwords worked")
            
            # Check if we need to reset the user
            print("\nChecking user status in auth system...")
            if SUPABASE_SERVICE_ROLE_KEY:
                admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
                try:
                    # List users to find our problematic user
                    users = admin_client.auth.admin.list_users()
                    for user in users:
                        if user.email == test_email:
                            print(f"Found user in auth: {user.id}")
                            print(f"Email confirmed: {user.email_confirmed_at is not None}")
                            print(f"Created at: {user.created_at}")
                            
                            # If email is not confirmed, that might be the issue
                            if not user.email_confirmed_at:
                                print("❌ Email is not confirmed - this is likely the issue!")
                                print("The user needs to confirm their email before they can sign in.")
                            
                            break
                    else:
                        print("User not found in auth system")
                except Exception as admin_error:
                    print(f"Admin check failed: {admin_error}")

if __name__ == "__main__":
    test_signin_fix()
