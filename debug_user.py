
#!/usr/bin/env python3
"""
Debug script to check user status in Supabase
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client

def debug_user_status():
    print("=== Debugging User Status ===")
    
    # Test email
    test_email = "new7@gmail.com"
    print(f"Checking email: {test_email}")
    
    # Create clients
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    if SUPABASE_SERVICE_ROLE_KEY:
        admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    else:
        admin_client = None
        print("Warning: No service role key available")
    
    # 1. Check if user exists in auth.users (requires admin client)
    print("\n1. Checking auth.users table...")
    if admin_client:
        try:
            # Use admin client to query auth.users
            auth_users = admin_client.auth.admin.list_users()
            user_found = False
            for user in auth_users:
                if user.email == test_email:
                    print(f"✅ User found in auth.users:")
                    print(f"   ID: {user.id}")
                    print(f"   Email: {user.email}")
                    print(f"   Email confirmed: {user.email_confirmed_at is not None}")
                    print(f"   Created: {user.created_at}")
                    user_found = True
                    break
            
            if not user_found:
                print(f"❌ User {test_email} NOT found in auth.users")
        except Exception as e:
            print(f"❌ Failed to check auth.users: {e}")
    else:
        print("❌ Cannot check auth.users without service role key")
    
    # 2. Check if user exists in public.users table
    print("\n2. Checking public.users table...")
    try:
        if admin_client:
            result = admin_client.table('users').select('*').eq('email', test_email).execute()
        else:
            result = supabase.table('users').select('*').eq('email', test_email).execute()
        
        if result.data:
            print(f"✅ User found in users table:")
            for user in result.data:
                print(f"   ID: {user['id']}")
                print(f"   Name: {user['name']}")
                print(f"   Email: {user['email']}")
        else:
            print(f"❌ User {test_email} NOT found in users table")
    except Exception as e:
        print(f"❌ Failed to check users table: {e}")
    
    # 3. Test signup with this email to see what happens
    print("\n3. Testing signup to see current status...")
    try:
        signup_response = supabase.auth.sign_up({
            "email": test_email,
            "password": "testpassword123"  # Use a test password
        })
        print(f"Signup response: {signup_response}")
        
        if hasattr(signup_response, 'user') and signup_response.user:
            print(f"User object returned: {signup_response.user}")
        else:
            print("No user object in signup response")
            
    except Exception as e:
        print(f"Signup test result: {e}")
        if "already registered" in str(e).lower():
            print("✅ User already exists in auth system")
        elif "signup_disabled" in str(e).lower():
            print("❌ Signup is disabled in Supabase")

if __name__ == "__main__":
    debug_user_status()
