import streamlit as st
import sys
import os
import uuid
from datetime import datetime

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from database.db_utils import db_manager

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Page configuration
st.set_page_config(
    page_title="Gita Guru - Divine Learning Platform",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
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

    .info-message {
        background: linear-gradient(135deg, #17a2b8 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
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

# Initialize session state for tab management
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "signin"

# Auth container
with st.container():
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)

    # Tab buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔑 Sign In", use_container_width=True, 
                     type="primary" if st.session_state.active_tab == "signin" else "secondary"):
            st.session_state.active_tab = "signin"
            st.rerun()

    with col2:
        if st.button("✨ Sign Up", use_container_width=True,
                     type="primary" if st.session_state.active_tab == "signup" else "secondary"):
            st.session_state.active_tab = "signup"
            st.rerun()

    st.markdown("---")

    # SIGN IN TAB
    if st.session_state.active_tab == "signin":
        st.markdown("### Welcome Back! 🙏")
        st.markdown("Sign in to continue your spiritual journey")

        with st.form("signin_form", clear_on_submit=True):
            email = st.text_input("📧 Email", placeholder="Enter your email address")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            signin_button = st.form_submit_button("🚀 Sign In", use_container_width=True)

        if signin_button:
            if not email or not password:
                st.markdown('<div class="error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                try:
                    # Clear any existing sessions
                    try:
                        supabase.auth.sign_out()
                    except:
                        pass

                    # Attempt authentication
                    response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    if response and response.user:
                        user_id = response.user.id
                        user_email = response.user.email

                        # Get or create user profile
                        user_profile = db_manager.get_user_by_id(user_id)

                        if not user_profile:
                            # Create user profile if it doesn't exist
                            user_name = user_email.split('@')[0].title()  # Use email prefix as name
                            user_profile = db_manager.create_user_if_not_exists(
                                user_id=user_id,
                                name=user_name,
                                email=user_email
                            )

                        if user_profile:
                            # Success! Store user in session and redirect
                            st.session_state["user"] = {
                                "id": user_profile["id"],
                                "email": user_profile["email"],
                                "name": user_profile["name"]
                            }
                            st.markdown('<div class="success-message">✅ Welcome back! Redirecting...</div>', unsafe_allow_html=True)
                            st.switch_page("pages/user_portal.py")
                        else:
                            st.markdown('<div class="error-message">❌ Failed to load user profile</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">❌ Authentication failed</div>', unsafe_allow_html=True)

                except Exception as e:
                    error_message = str(e).lower()
                    if "invalid" in error_message or "credential" in error_message:
                        st.markdown('<div class="error-message">❌ Invalid email or password. Please check your credentials.</div>', unsafe_allow_html=True)
                        st.markdown('<div class="info-message">💡 Don\'t have an account? Click "Sign Up" above to create one.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-message">❌ Sign in error: {str(e)}</div>', unsafe_allow_html=True)

    # SIGN UP TAB
    else:
        st.markdown("### Join the Journey! 🌟")
        st.markdown("Create your account to begin learning")

        with st.form("signup_form", clear_on_submit=True):
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email", placeholder="Enter your email address")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a password (min 6 characters)")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            signup_button = st.form_submit_button("🎯 Create Account", use_container_width=True)

        if signup_button:
            if not all([name, email, password, confirm_password]):
                st.markdown('<div class="error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
            elif len(password) < 6:
                st.markdown('<div class="error-message">❌ Password must be at least 6 characters long</div>', unsafe_allow_html=True)
            else:
                try:
                    # Create user account
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    if response and response.user:
                        user_id = response.user.id

                        # Create user profile immediately
                        user_profile = db_manager.create_user_if_not_exists(
                            user_id=user_id,
                            name=name,
                            email=email
                        )

                        if user_profile:
                            # Success! Store user in session and redirect
                            st.session_state["user"] = {
                                "id": user_profile["id"],
                                "email": user_profile["email"],
                                "name": user_profile["name"]
                            }
                            st.markdown('<div class="success-message">✅ Account created successfully! Welcome to Gita Guru!</div>', unsafe_allow_html=True)
                            st.switch_page("pages/user_portal.py")
                        else:
                            st.markdown('<div class="error-message">❌ Failed to create user profile</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-message">❌ Account creation failed</div>', unsafe_allow_html=True)

                except Exception as e:
                    error_message = str(e).lower()
                    if "already registered" in error_message or "email" in error_message and "exists" in error_message:
                        st.markdown('<div class="error-message">❌ This email is already registered. Please sign in instead.</div>', unsafe_allow_html=True)
                        st.markdown('<div class="info-message">💡 Already have an account? Click "Sign In" above.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-message">❌ Sign up error: {str(e)}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Features section
st.markdown("---")
st.markdown("""
<div style="display: flex; justify-content: space-around; margin-top: 3rem; text-align: center; color: white;">
    <div style="opacity: 0.8;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📚</div>
        <div style="font-weight: 600;">Sacred Texts</div>
        <div style="font-size: 0.9rem; opacity: 0.7;">Learn from ancient wisdom</div>
    </div>
    <div style="opacity: 0.8;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎤</div>
        <div style="font-weight: 600;">Audio Learning</div>
        <div style="font-size: 0.9rem; opacity: 0.7;">Listen and practice</div>
    </div>
    <div style="opacity: 0.8;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌟</div>
        <div style="font-weight: 600;">Spiritual Growth</div>
        <div style="font-size: 0.9rem; opacity: 0.7;">Transform your life</div>
    </div>
</div>
""", unsafe_allow_html=True)