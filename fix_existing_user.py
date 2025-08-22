
#!/usr/bin/env python3
"""
Script to fix the existing user who is in auth but not in users table
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client
from database.db_utils import db_manager

def fix_existing_user():
    print("=== Fixing Existing User ===")
    
    # The problematic user from your debug output
    user_id = "e0b3d317-aa8b-4773-aa56-2fce3994d58a"
    email = "new7@gmail.com"
    name = "New User 7"  # Default name since we don't have it
    
    print(f"Fixing user: {email} with ID: {user_id}")
    
    # Create the user profile
    created = db_manager.create_user_if_not_exists(
        user_id=user_id,
        name=name,
        email=email
    )
    
    if created:
        print(f"✅ Successfully fixed user: {created}")
        
        # Verify the fix
        found_user = db_manager.get_user_by_id(user_id)
        print(f"✅ Verification - found user: {found_user}")
        
        # Also verify by email
        found_by_email = db_manager.get_user_by_email(email)
        print(f"✅ Verification - found by email: {found_by_email}")
        
    else:
        print("❌ Failed to fix user")

if __name__ == "__main__":
    fix_existing_user()
