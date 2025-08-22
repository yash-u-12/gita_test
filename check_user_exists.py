
#!/usr/bin/env python3
"""
Script to check if a user exists in the authentication system
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client

def check_user_exists(email):
    print(f"=== Checking User: {email} ===")
    
    # Create clients
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    if SUPABASE_SERVICE_ROLE_KEY:
        admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    else:
        admin_client = None
        print("⚠️ No admin client available")
    
    # Check if user exists in auth system
    if admin_client:
        try:
            users = admin_client.auth.admin.list_users()
            user_found = False
            for user in users:
                if user.email == email:
                    print(f"✅ User EXISTS in auth system:")
                    print(f"   Email: {user.email}")
                    print(f"   ID: {user.id}")
                    print(f"   Email confirmed: {user.email_confirmed_at is not None}")
                    print(f"   Created: {user.created_at}")
                    user_found = True
                    break
            
            if not user_found:
                print(f"❌ User {email} does NOT exist in auth system")
                print("💡 User needs to SIGN UP first before they can sign in")
                
        except Exception as e:
            print(f"❌ Error checking auth users: {e}")
    
    # Check public users table
    try:
        result = supabase.table('users').select('*').eq('email', email).execute()
        if result.data:
            print(f"✅ User profile exists in database:")
            for user in result.data:
                print(f"   ID: {user['id']}")
                print(f"   Name: {user['name']}")
                print(f"   Email: {user['email']}")
        else:
            print(f"❌ No user profile found in database for {email}")
    except Exception as e:
        print(f"❌ Error checking users table: {e}")

if __name__ == "__main__":
    # Test the problematic emails
    test_emails = ["new8@gmail.com", "new7@gmail.com"]
    
    for email in test_emails:
        check_user_exists(email)
        print("-" * 50)
