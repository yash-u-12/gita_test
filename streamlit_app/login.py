import streamlit as st
import sys
import os
import uuid
from datetime import datetime
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
import wave, contextlib

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
from database.db_utils import db_manager

# Clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# Admin client only if service role key is available
admin_client = None
if SUPABASE_SERVICE_ROLE_KEY:
    admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)  # server-side admin checks

# Use your bucket; override with .env SUPABASE_BUCKET if needed
BUCKET_NAME = os.getenv("SUPABASE_BUCKET", "gita-guru")

# Page configuration
st.set_page_config(
    page_title="Gita Guru - Divine Learning Platform",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 0;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        text-align: center;
        color: white;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    .auth-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        max-width: 500px;
        margin: 0 auto;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .auth-tabs {
        display: flex;
        background: #f8f9fa;
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 2rem;
    }
    
    .auth-tab {
        flex: 1;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .auth-tab.active {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #667eea;
    }
    
    .auth-tab:not(.active) {
        color: #6c757d;
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        font-weight: 500;
        color: #495057;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 12px 16px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .success-message {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .error-message {
        background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #dee2e6, transparent);
        margin: 2rem 0;
    }
    
    .features {
        display: flex;
        justify-content: space-around;
        margin-top: 3rem;
        text-align: center;
    }
    
    .feature {
        color: white;
        opacity: 0.8;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .feature-desc {
        font-size: 0.9rem;
        opacity: 0.7;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <div class="main-title">🕉️ Gita Guru</div>
    <div class="subtitle">Divine Learning Platform</div>
</div>
""", unsafe_allow_html=True)

# Auth container
with st.container():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Tab selection
    col1, col2 = st.columns(2)
    with col1:
        signin_selected = st.button("Sign In", key="signin_tab", use_container_width=True)
    with col2:
        signup_selected = st.button("Sign Up", key="signup_tab", use_container_width=True)
    
    # Default to sign in if no selection
    if not signin_selected and not signup_selected:
        signin_selected = True
    
    # ----------------- SIGN IN -----------------
    if signin_selected:
        st.markdown("### Welcome Back 🙏")
        st.markdown("Sign in to continue your spiritual journey")
        
        with st.form("signin_form"):
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("🚀 Sign In", use_container_width=True)

        if submit:
            if not email or not password:
                st.markdown('<div class="error-message">Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                try:
                    st.write(f"Debug: Attempting signin for email: {email}")
                    
                    # Clear any existing session first
                    try:
                        supabase.auth.sign_out()
                    except:
                        pass  # Ignore sign out errors
                    
                    # Attempt signin
                    auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.write(f"Debug: Signin response type: {type(auth_response)}")
                    
                    # Handle successful authentication
                    if auth_response and hasattr(auth_response, 'user') and auth_response.user:
                        user_obj = auth_response.user
                        user_id = user_obj.id
                        st.write(f"Debug: Successfully authenticated user ID: {user_id}")

                        # Check if email is confirmed
                        if not user_obj.email_confirmed_at:
                            st.markdown('<div class="warning-message">📧 Please check your email and confirm your account before signing in.</div>', unsafe_allow_html=True)
                            st.stop()

                        # Try to get or create user profile
                        try:
                            st.write(f"Debug: Looking for user profile with ID: {user_id}")
                            
                            # First try to find existing user
                            existing = db_manager.get_user_by_id(user_id)
                            st.write(f"Debug: Found existing user: {existing}")

                            if existing:
                                st.markdown('<div class="success-message">✅ Sign in successful — redirecting...</div>', unsafe_allow_html=True)
                                st.session_state["user"] = {"id": existing["id"], "email": existing["email"], "name": existing["name"]}
                                st.switch_page("pages/user_portal.py")
                            else:
                                # User exists in auth but not in users table - create profile
                                st.write("Debug: User not found in users table, creating profile...")
                                
                                # Use email as name if no display name available
                                display_name = getattr(user_obj, 'user_metadata', {}).get('name', user_obj.email)
                                if not display_name:
                                    display_name = user_obj.email.split('@')[0]  # Use part before @ as name
                                
                                created = db_manager.create_user_if_not_exists(
                                    user_id=user_id, 
                                    name=display_name, 
                                    email=user_obj.email
                                )
                                
                                if created:
                                    st.markdown('<div class="success-message">✅ Profile created and sign in successful — redirecting...</div>', unsafe_allow_html=True)
                                    st.session_state["user"] = {"id": created["id"], "email": created["email"], "name": created["name"]}
                                    st.switch_page("pages/user_portal.py")
                                else:
                                    st.markdown('<div class="error-message">❌ Could not create user profile. Please contact support.</div>', unsafe_allow_html=True)
                                    
                        except Exception as db_error:
                            st.markdown(f'<div class="error-message">❌ Database error: {str(db_error)}</div>', unsafe_allow_html=True)
                            st.write(f"Debug: Database error details: {db_error}")
                    else:
                        st.markdown('<div class="error-message">❌ Authentication failed. Invalid response from server.</div>', unsafe_allow_html=True)
                        st.write(f"Debug: Auth response: {auth_response}")
                        
                except Exception as e:
                    error_msg = str(e)
                    st.write(f"Debug: Full error details: {e}")
                    
                    # Handle specific error cases
                    if "Invalid login credentials" in error_msg or "invalid_credentials" in error_msg:
                        st.markdown('<div class="error-message">❌ Invalid email or password. If you just signed up, please check your email for confirmation first.</div>', unsafe_allow_html=True)
                        st.markdown('<div class="info-message">💡 <strong>Troubleshooting:</strong><br/>• Make sure you\'ve confirmed your email address<br/>• Check that your password is correct<br/>• Try signing up again if you haven\'t received a confirmation email</div>', unsafe_allow_html=True)
                    elif "Email not confirmed" in error_msg or "email_not_confirmed" in error_msg:
                        st.markdown('<div class="warning-message">📧 Please confirm your email address before signing in. Check your email inbox for a confirmation link.</div>', unsafe_allow_html=True)
                    elif "signup_disabled" in error_msg:
                        st.markdown('<div class="error-message">❌ User registration is disabled. Please contact the administrator.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-message">❌ Sign in error: {error_msg}</div>', unsafe_allow_html=True)
                        
                        # Offer password reset option
                        with st.expander("Need help?"):
                            st.write("If you're having trouble signing in:")
                            st.write("1. Make sure your email is confirmed")
                            st.write("2. Try resetting your password")
                            
                            if st.button("Send Password Reset Email"):
                                try:
                                    supabase.auth.reset_password_email(email)
                                    st.success("Password reset email sent! Check your inbox.")
                                except Exception as reset_error:
                                    st.error(f"Could not send reset email: {reset_error}")

    # ----------------- SIGN UP -----------------
    else:
        st.markdown("### Join the Journey 🌟")
        st.markdown("Create your account to begin learning")
        
        with st.form("signup_form"):
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
            register = st.form_submit_button("✨ Create Account", use_container_width=True)

        if register:
            if not name or not email or not password:
                st.markdown('<div class="error-message">Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                try:
                    # Create auth user
                    st.write(f"Debug: Creating auth user for email: {email}")
                    auth_response = supabase.auth.sign_up({"email": email, "password": password})
                    st.write(f"Debug: Auth response: {auth_response}")

                    if auth_response and getattr(auth_response, "user", None):
                        user_id = auth_response.user.id
                        st.write(f"Debug: User ID from auth: {user_id}")
                        
                        # Check if email confirmation is required
                        if hasattr(auth_response, 'session') and auth_response.session is None:
                            st.markdown('<div class="warning-message">📧 Please check your email and confirm your account before signing in.</div>', unsafe_allow_html=True)
                            st.markdown('<div class="info-message">After confirming your email, you can sign in with your credentials.</div>', unsafe_allow_html=True)
                        else:
                            # Create user row if not exists — use admin to check/insert
                            try:
                                st.write(f"Debug: Creating user profile in database...")
                                created = db_manager.create_user_if_not_exists(user_id=user_id, name=name, email=email)
                                st.write(f"Debug: User profile creation result: {created}")
                                
                                if created:
                                    # Save session state and proceed
                                    st.markdown('<div class="success-message">✅ Account created successfully! Welcome to Gita Guru.</div>', unsafe_allow_html=True)
                                    st.session_state["user"] = {"id": created["id"], "email": email, "name": name}
                                    
                                    st.switch_page("pages/user_portal.py")
                                    st.rerun()
                                else:
                                    st.markdown('<div class="error-message">❌ User profile creation failed. Please try again.</div>', unsafe_allow_html=True)
                            except Exception as db_error:
                                st.markdown(f'<div class="error-message">❌ Database error: {str(db_error)}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">❌ Sign up failed. Please try again.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-message">❌ Sign up failed: {str(e)}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Features section
st.markdown("""
<div class="features">
    <div class="feature">
        <div class="feature-icon">📚</div>
        <div class="feature-title">Sacred Texts</div>
        <div class="feature-desc">Learn from ancient wisdom</div>
    </div>
    <div class="feature">
        <div class="feature-icon">🎤</div>
        <div class="feature-title">Audio Learning</div>
        <div class="feature-desc">Listen and practice</div>
    </div>
    <div class="feature">
        <div class="feature-icon">🌟</div>
        <div class="feature-title">Spiritual Growth</div>
        <div class="feature-desc">Transform your life</div>
    </div>
</div>
""", unsafe_allow_html=True)
