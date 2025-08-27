import streamlit as st
import requests
import json
import os
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from database.db_utils import get_db_manager
from apis import signup_user, signin_user
from audio import upload_audio

# Initialize Supabase client for reference audio only
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
db_manager = get_db_manager()

def init_session_state():
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'selected_chapter' not in st.session_state:
        st.session_state.selected_chapter = None
    if 'selected_sloka' not in st.session_state:
        st.session_state.selected_sloka = None

def handle_signup(name, email, password):
    try:
        response = signup_user(name, email, password)
        if response.get('success'):
            st.success("Account created successfully! Please sign in.")
            return True
        else:
            st.error(f"Signup failed: {response.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Signup error: {str(e)}")
        return False

def handle_signin(email, password):
    try:
        response = signin_user(email, password)
        if response.get('success'):
            user_data = response.get('user', {})
            st.session_state.user_id = user_data.get('id')
            st.session_state.user_name = user_data.get('name')
            st.session_state.user_email = user_data.get('email')
            st.session_state.logged_in = True
            st.success("Signed in successfully!")
            st.rerun()
            return True
        else:
            st.error(f"Sign in failed: {response.get('message', 'Invalid credentials')}")
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
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")

            if submit and email and password:
                handle_signin(email, password)

    with tab2:
        st.subheader("Create Account")
        with st.form("signup_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")

            if submit:
                if not all([name, email, password, confirm_password]):
                    st.error("All fields are required")
                elif password != confirm_password:
                    st.error("Passwords don't match")
                else:
                    handle_signup(name, email, password)

def show_main_app():
    st.title("🕉️ Gita Guru")

    # User info and logout in sidebar
    with st.sidebar:
        st.write(f"Welcome, {st.session_state.user_name}!")
        if st.button("Logout"):
            for key in ['user_id', 'user_name', 'user_email', 'logged_in']:
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

                # Audio Upload Section
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
                            with st.spinner("Uploading recitation..."):
                                try:
                                    # Convert file to bytes
                                    audio_bytes = recitation_file.read()

                                    # Use the upload_audio function from audio.py
                                    response = upload_audio(
                                        audio_bytes,
                                        f"recitation_{st.session_state.user_id}_{selected_sloka['id']}.mp3",
                                        st.session_state.user_id,
                                        selected_sloka['id'],
                                        "recitation"
                                    )

                                    if response.get('success'):
                                        st.success("Recitation uploaded successfully!")
                                    else:
                                        st.error(f"Upload failed: {response.get('message', 'Unknown error')}")

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
                            with st.spinner("Uploading explanation..."):
                                try:
                                    # Convert file to bytes
                                    audio_bytes = explanation_file.read()

                                    # Use the upload_audio function from audio.py
                                    response = upload_audio(
                                        audio_bytes,
                                        f"explanation_{st.session_state.user_id}_{selected_sloka['id']}.mp3",
                                        st.session_state.user_id,
                                        selected_sloka['id'],
                                        "explanation"
                                    )

                                    if response.get('success'):
                                        st.success("Explanation uploaded successfully!")
                                    else:
                                        st.error(f"Upload failed: {response.get('message', 'Unknown error')}")

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