
#!/usr/bin/env python3
"""
Script to check email confirmation status and provide solutions
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, '.')

from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from supabase import create_client

def check_email_confirmation():
    print("=== Email Confirmation Checker ===")
    
    test_email = "new7@gmail.com"
    
    # Create regular client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print(f"Checking email confirmation status for: {test_email}")
    
    # If we have admin access, check the user's confirmation status
    if SUPABASE_SERVICE_ROLE_KEY:
        admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        try:
            users = admin_client.auth.admin.list_users()
            
            for user in users:
                if user.email == test_email:
                    print(f"✅ Found user: {user.id}")
                    print(f"Email: {user.email}")
                    print(f"Email confirmed: {user.email_confirmed_at is not None}")
                    print(f"Created at: {user.created_at}")
                    
                    if not user.email_confirmed_at:
                        print("\n❌ EMAIL NOT CONFIRMED!")
                        print("This is why signin is failing.")
                        print("\nSolutions:")
                        print("1. User should check their email for confirmation link")
                        print("2. Resend confirmation email")
                        print("3. Admin can manually confirm the email")
                        
                        # Offer to resend confirmation
                        try:
                            print("\nAttempting to resend confirmation email...")
                            supabase.auth.resend({
                                "type": "signup",
                                "email": test_email
                            })
                            print("✅ Confirmation email resent!")
                        except Exception as resend_error:
                            print(f"❌ Failed to resend: {resend_error}")
                            
                        # If admin, offer to manually confirm
                        try:
                            print("\nAttempting admin email confirmation...")
                            admin_client.auth.admin.update_user_by_id(
                                user.id, 
                                {"email_confirm": True}
                            )
                            print("✅ Email manually confirmed by admin!")
                            
                            # Test signin now
                            print("\nTesting signin after confirmation...")
                            auth_response = supabase.auth.sign_in_with_password({
                                "email": test_email,
                                "password": "testpassword123"  # Try with common password
                            })
                            print(f"✅ Signin now works! User ID: {auth_response.user.id}")
                            
                        except Exception as confirm_error:
                            print(f"❌ Manual confirmation failed: {confirm_error}")
                            
                    else:
                        print("✅ Email is already confirmed")
                        print("The signin issue might be due to incorrect password")
                    
                    return
            
            print("❌ User not found in auth system")
            
        except Exception as admin_error:
            print(f"❌ Admin check failed: {admin_error}")
    else:
        print("❌ No admin access available - cannot check email confirmation status")
        print("Try using the password reset feature in the app")

if __name__ == "__main__":
    check_email_confirmation()
