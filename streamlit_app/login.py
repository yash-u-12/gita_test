import streamlit as st
import os
import sys

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from database.db_utils import get_db_manager
from api_client import api_client, get_api_client

# Initialize Supabase client for reference audio only
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
db_manager = get_db_manager()

def init_session_state():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'user_phone' not in st.session_state:
        st.session_state.user_phone = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'selected_chapter' not in st.session_state:
        st.session_state.selected_chapter = None
    if 'selected_sloka' not in st.session_state:
        st.session_state.selected_sloka = None
    if 'signup_step' not in st.session_state:
        st.session_state.signup_step = 'phone'
    if 'signup_phone' not in st.session_state:
        st.session_state.signup_phone = None

def handle_send_otp(phone_number):
    try:
        response = api_client.send_signup_otp(phone_number)
        if response.get('success'):
            st.session_state.signup_phone = phone_number
            st.session_state.signup_step = 'verify'
            st.success("OTP sent successfully! Please check your phone.")
            st.rerun()
            return True
        else:
            # Better error handling with more details
            error_data = response.get('data', {})
            status_code = response.get('status_code', 'Unknown')
            
            if isinstance(error_data, dict):
                error_message = error_data.get('message', error_data.get('error', 'Unknown error'))
            else:
                error_message = str(error_data)
            
            st.error(f"Failed to send OTP (Status: {status_code}): {error_message}")
            
            # Show debug info in expander for troubleshooting
            with st.expander("Debug Information"):
                st.json(response)
            
            return False
    except Exception as e:
        st.error(f"Error sending OTP: {str(e)}")
        return False

def handle_verify_signup(phone_number, otp_code, name, email, password):
    try:
        response = api_client.verify_signup_otp(phone_number, otp_code, name, email, password, True)
        if response.get('success'):
            st.success("Account created successfully! Please sign in.")
            st.session_state.signup_step = 'phone'
            st.session_state.signup_phone = None
            return True
        else:
            st.error(f"Signup verification failed: {response.get('data', {}).get('message', 'Invalid OTP or details')}")
            return False
    except Exception as e:
        st.error(f"Signup error: {str(e)}")
        return False

def handle_signin(phone, password):
    try:
        response = api_client.login(phone, password)
        if response.get('success'):
            user_data = response.get('data', {}).get('user', {})
            st.session_state.user_id = user_data.get('id')
            st.session_state.user_name = user_data.get('name')
            st.session_state.user_phone = user_data.get('phone')
            st.session_state.user_email = user_data.get('email', '')
            st.session_state.logged_in = True
            st.success("Signed in successfully!")
            st.rerun()
            return True
        else:
            st.error(f"Sign in failed: {response.get('data', {}).get('message', 'Invalid credentials')}")
            return False
    except Exception as e:
        st.error(f"Sign in error: {str(e)}")
        return False

def show_auth_forms():
    st.title("🕉️ Gita Guru")
    st.subheader("Welcome to the Bhagavad Gita Learning Platform")

    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

    with tab1:
        st.subheader("Sign In")
        with st.form("signin_form"):
            phone = st.text_input("Phone Number", placeholder="Enter your phone number")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")

            if submit and phone and password:
                handle_signin(phone, password)

    with tab2:
        st.subheader("Create Account")

        if st.session_state.signup_step == 'phone':
            with st.form("send_otp_form"):
                phone_number = st.text_input("Phone Number", placeholder="Enter your phone number (e.g., +91XXXXXXXXXX)")
                submit = st.form_submit_button("Send OTP")

                if submit and phone_number:
                    # Basic phone number validation
                    phone_cleaned = phone_number.strip()
                    if not phone_cleaned:
                        st.error("Please enter a phone number")
                    elif len(phone_cleaned) < 10:
                        st.error("Phone number seems too short")
                    else:
                        handle_send_otp(phone_cleaned)

        elif st.session_state.signup_step == 'verify':
            st.info(f"OTP sent to {st.session_state.signup_phone}")
            with st.form("verify_otp_form"):
                otp_code = st.text_input("Enter OTP", placeholder="6-digit OTP")
                name = st.text_input("Full Name")
                email = st.text_input("Email (optional)")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")

                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Create Account")
                with col2:
                    if st.form_submit_button("← Back"):
                        st.session_state.signup_step = 'phone'
                        st.session_state.signup_phone = None
                        st.rerun()

                if submit:
                    if not all([otp_code, name, password, confirm_password]):
                        st.error("OTP, name, and passwords are required")
                    elif password != confirm_password:
                        st.error("Passwords don't match")
                    else:
                        handle_verify_signup(st.session_state.signup_phone, otp_code, name, email or "", password)

def show_main_app():
    st.title("🕉️ Gita Guru")

    # User info and logout in sidebar
    with st.sidebar:
        st.write(f"Welcome, {st.session_state.user_name}!")
        st.write(f"Phone: {st.session_state.user_phone}")
        if st.session_state.user_email:
            st.write(f"Email: {st.session_state.user_email}")

        st.markdown("---")

        # User contributions section
        if st.button("View My Contributions"):
            try:
                contributions = api_client.get_user_contributions(st.session_state.user_id)
                if contributions.get('success'):
                    contrib_data = contributions.get('data', {})
                    st.write("📊 Your Contributions:")
                    st.json(contrib_data)
                else:
                    st.error("Failed to load contributions")
            except Exception as e:
                st.error(f"Error loading contributions: {str(e)}")

        if st.button("Logout"):
            # Clear session and API client
            api_client.auth_token = None
            api_client.user_data = None
            for key in ['user_id', 'user_name', 'user_phone', 'user_email', 'logged_in']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # Get chapters from database
    chapters = db_manager.get_all_chapters()
    if not chapters:
        st.error("No chapters found in database")
        return

    # Chapter selection
    chapter_options = {f"Chapter {ch['chapter_number']}: {ch['chapter_name']}": ch for ch in chapters}
    selected_chapter_display = st.selectbox("Select Chapter", list(chapter_options.keys()))

    if selected_chapter_display:
        selected_chapter = chapter_options[selected_chapter_display]
        st.session_state.selected_chapter = selected_chapter

        # Get slokas for selected chapter
        slokas = db_manager.get_slokas_by_chapter(selected_chapter['id'])

        if slokas:
            sloka_options = {f"Sloka {sloka['sloka_number']}": sloka for sloka in slokas}
            selected_sloka_display = st.selectbox("Select Sloka", list(sloka_options.keys()))

            if selected_sloka_display:
                selected_sloka = sloka_options[selected_sloka_display]
                st.session_state.selected_sloka = selected_sloka

                # Display sloka content with improved layout
                st.markdown("---")

                # Reference Audio at the top
                st.subheader("📻 Reference Audio")
                if selected_sloka.get('reference_audio_url'):
                    st.audio(selected_sloka['reference_audio_url'], format='audio/mp3')
                else:
                    st.info("No reference audio available for this sloka")

                st.markdown("---")

                # Sloka Text
                st.subheader("📜 Sloka Text")
                st.markdown(f"**Telugu:** {selected_sloka['sloka_text_telugu']}")

                st.markdown("---")

                # Meanings
                st.subheader("💭 Meanings")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Telugu Meaning:**")
                    st.write(selected_sloka['meaning_telugu'])

                with col2:
                    st.markdown("**English Meaning:**")
                    st.write(selected_sloka['meaning_english'])

                st.markdown("---")

                # Audio Upload Section using Swecha API
                st.subheader("🎤 Upload Your Audio")

                upload_tab1, upload_tab2 = st.tabs(["Recitation Audio", "Explanation Audio"])

                with upload_tab1:
                    st.write("Upload your recitation of this sloka")
                    recitation_file = st.file_uploader(
                        "Choose recitation audio file", 
                        type=['mp3', 'wav', 'ogg'],
                        key="recitation_upload"
                    )

                    if recitation_file is not None:
                        if st.button("Upload Recitation", key="upload_recitation"):
                            with st.spinner("Uploading recitation to Swecha Corpus..."):
                                try:
                                    # Read file data
                                    audio_data = recitation_file.read()
                                    filename = f"recitation_{st.session_state.user_id}_{selected_sloka['id']}_{recitation_file.name}"
                                    title = f"Sloka {selected_sloka['sloka_number']} Recitation - Chapter {selected_chapter['chapter_number']}"

                                    # Upload using API client
                                    response = get_api_client().upload_complete_audio(
                                        audio_data=audio_data,
                                        filename=filename,
                                        title=title,
                                        category_id="1",  # You may want to make this configurable
                                        language="te",    # Telugu
                                        release_rights="open",
                                        description=f"User recitation for {title}"
                                    )

                                    if response.get('success'):
                                        st.success("Recitation uploaded successfully to Swecha Corpus!")
                                        upload_data = response.get('data', {})
                                        if upload_data.get('id'):
                                            st.info(f"Upload ID: {upload_data['id']}")
                                    else:
                                        st.error(f"Upload failed: {response.get('data', {}).get('message', 'Unknown error')}")

                                except Exception as e:
                                    st.error(f"Upload error: {str(e)}")

                with upload_tab2:
                    st.write("Upload your explanation of this sloka")
                    explanation_file = st.file_uploader(
                        "Choose explanation audio file", 
                        type=['mp3', 'wav', 'ogg'],
                        key="explanation_upload"
                    )

                    if explanation_file is not None:
                        if st.button("Upload Explanation", key="upload_explanation"):
                            with st.spinner("Uploading explanation to Swecha Corpus..."):
                                try:
                                    # Read file data
                                    audio_data = explanation_file.read()
                                    filename = f"explanation_{st.session_state.user_id}_{selected_sloka['id']}_{explanation_file.name}"
                                    title = f"Sloka {selected_sloka['sloka_number']} Explanation - Chapter {selected_chapter['chapter_number']}"

                                    # Upload using API client
                                    response = get_api_client().upload_complete_audio(
                                        audio_data=audio_data,
                                        filename=filename,
                                        title=title,
                                        category_id="1",  # You may want to make this configurable
                                        language="te",    # Telugu
                                        release_rights="open",
                                        description=f"User explanation for {title}"
                                    )

                                    if response.get('success'):
                                        st.success("Explanation uploaded successfully to Swecha Corpus!")
                                        upload_data = response.get('data', {})
                                        if upload_data.get('id'):
                                            st.info(f"Upload ID: {upload_data['id']}")
                                    else:
                                        st.error(f"Upload failed: {response.get('data', {}).get('message', 'Unknown error')}")

                                except Exception as e:
                                    st.error(f"Upload error: {str(e)}")

def main():
    st.set_page_config(
        page_title="Gita Guru",
        page_icon="🕉️",
        layout="wide"
    )

    init_session_state()

    if st.session_state.logged_in:
        show_main_app()
    else:
        show_auth_forms()

if __name__ == "__main__":
    main()