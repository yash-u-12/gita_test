import streamlit as st
import os
import sys
import websockets
import io
import wave
from typing import Optional


# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from database.db_utils import get_db_manager
from api_client import api_client, get_api_client

# Optional dependencies for in-app recording (prefer audio-recorder-streamlit)
_RECORDING_AVAILABLE = False
_RECORDER_IMPL = None
try:
    from audio_recorder_streamlit import audio_recorder
    _RECORDING_AVAILABLE = True
    _RECORDER_IMPL = "audio_recorder_streamlit"
except Exception:
    try:
        from streamlit_mic_recorder import mic_recorder
        _RECORDING_AVAILABLE = True
        _RECORDER_IMPL = "mic_recorder"
    except Exception:
        try:
            from audiorecorder import audiorecorder
            _RECORDING_AVAILABLE = True
            _RECORDER_IMPL = "audiorecorder"
        except Exception:
            _RECORDING_AVAILABLE = False
            _RECORDER_IMPL = None

# Test bypass credentials for OTP login (skips API when enabled)
TEST_LOGIN_PHONE = os.getenv("TEST_LOGIN_PHONE", "+910000000000")
TEST_LOGIN_OTP = os.getenv("TEST_LOGIN_OTP", "123456")

db_manager = get_db_manager()

def _compute_wav_duration_seconds(wav_bytes: bytes) -> float:
    try:
        import contextlib
        with contextlib.closing(wave.open(io.BytesIO(wav_bytes), 'rb')) as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate > 0:
                return round(frames / float(rate), 2)
    except Exception:
        pass
    return 0.0

def _slugify(text: str) -> str:
    try:
        import re
        text = re.sub(r"[^A-Za-z0-9]+", "-", text or "").strip("-")
        return text.lower() or "untitled"
    except Exception:
        return "untitled"

def _build_media_metadata(selected_chapter: dict, selected_sloka: dict, user_id: str, kind: str, original_filename: str | None = None) -> tuple[str, str, str]:
    """Return (filename, title, description) for recitation/explanation.
    kind: 'recitation' | 'explanation'
    """
    chapter_num = selected_chapter.get('chapter_number')
    chapter_name = selected_chapter.get('chapter_name', '')
    sloka_num = selected_sloka.get('sloka_number')
    safe_ch_name = _slugify(str(chapter_name))
    base = f"ch{chapter_num}_sloka{sloka_num}_{kind}"
    # preserve extension if provided, else default wav
    ext = None
    if original_filename and "." in original_filename:
        ext = "." + original_filename.rsplit(".", 1)[-1].lower()
    if not ext:
        ext = ".wav"
    filename = f"{base}_{_slugify(str(user_id))}{ext}"
    title = f"Sloka {sloka_num} {kind.capitalize()} - Chapter {chapter_num}"
    description = f"{kind.capitalize()} audio of sloka {sloka_num} from adhyaya {chapter_num} ({chapter_name})"
    return filename, title, description

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
    if 'login_otp_step' not in st.session_state:
        st.session_state.login_otp_step = 'phone'
    if 'login_otp_phone' not in st.session_state:
        st.session_state.login_otp_phone = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # No cookie-based restore

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
            error_data = response.get('data', {})
            status_code = response.get('status_code', 'Unknown')
            if status_code == 500 or error_data.get('detail') == "Internal server error":
                st.error("⚠️ Internal server error from backend. Please try again later or contact support.")
                with st.expander("Debug Information"):
                    st.json(response)
            else:
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
            error_msg = response.get('data', {}).get('message', 'Invalid OTP or details')
            status_code = response.get('status_code', 'Unknown')
            error_data = response.get('data', {})
            if status_code == 500 or error_data.get('detail') == "Internal server error":
                st.error("⚠️ Internal server error from backend. Please try again later or contact support.")
                with st.expander("Signup Debug Info"):
                    st.json(response)
            else:
                st.error(f"Signup verification failed: {error_msg}")
                with st.expander("Signup Debug Info"):
                    st.json(response)
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
            # No cookie persistence
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
        login_mode = st.radio("Choose login method:", ["Password", "OTP"], horizontal=True)
        if login_mode == "Password":
            with st.form("signin_form"):
                phone = st.text_input("Phone Number", placeholder="Enter your phone number")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In")
                if submit and phone and password:
                    handle_signin(phone, password)
        else:
            if st.session_state.login_otp_step == 'phone':
                with st.form("send_login_otp_form"):
                    phone_number = st.text_input("Phone Number", placeholder="Enter your phone number (e.g., +91XXXXXXXXXX)")
                    submit = st.form_submit_button("Send OTP")
                    if submit and phone_number:
                        phone_cleaned = phone_number.strip()
                        if not phone_cleaned:
                            st.error("Please enter a phone number")
                        elif len(phone_cleaned) < 10:
                            st.error("Phone number seems too short")
                        else:
                            # Test bypass: skip API for configured phone number
                            if phone_cleaned == TEST_LOGIN_PHONE:
                                st.session_state.login_otp_phone = phone_cleaned
                                st.session_state.login_otp_step = 'verify'
                                st.info("Test mode enabled. Use the preset OTP to continue.")
                                st.rerun()
                            else:
                                response = api_client.send_login_otp(phone_cleaned)
                                if response.get('success'):
                                    st.session_state.login_otp_phone = phone_cleaned
                                    st.session_state.login_otp_step = 'verify'
                                    st.success("OTP sent successfully! Please check your phone.")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to send OTP: {response.get('data', {}).get('message', 'Unknown error')}")
            elif st.session_state.login_otp_step == 'verify':
                st.info(f"OTP sent to {st.session_state.login_otp_phone}")
                with st.form("verify_login_otp_form"):
                    otp_code = st.text_input("Enter OTP", placeholder="6-digit OTP")
                    submit = st.form_submit_button("Verify & Login")
                    col1, col2 = st.columns(2)
                    with col2:
                        if st.form_submit_button("← Back"):
                            st.session_state.login_otp_step = 'phone'
                            st.session_state.login_otp_phone = None
                            st.rerun()
                    if submit and otp_code:
                        # Test bypass: verify without API if configured phone and OTP match
                        if st.session_state.login_otp_phone == TEST_LOGIN_PHONE and otp_code == TEST_LOGIN_OTP:
                            fake_user = {
                                'id': 'test-user-id',
                                'name': 'Test User',
                                'phone': TEST_LOGIN_PHONE,
                                'email': 'test@example.com',
                            }
                            api_client.auth_token = api_client.auth_token or 'TEST_TOKEN'
                            api_client.user_data = fake_user
                            st.session_state.user_id = fake_user['id']
                            st.session_state.user_name = fake_user['name']
                            st.session_state.user_phone = fake_user['phone']
                            st.session_state.user_email = fake_user['email']
                            st.session_state.logged_in = True
                            # No cookie persistence in test mode
                            st.success("Signed in successfully (test mode)!")
                            st.session_state.login_otp_step = 'phone'
                            st.session_state.login_otp_phone = None
                            st.rerun()
                        else:
                            response = api_client.verify_login_otp(
                                st.session_state.login_otp_phone, otp_code, True
                            )
                            if response.get('success'):
                                user_data = response.get('data', {}).get('user', {})
                                st.session_state.user_id = user_data.get('id')
                                st.session_state.user_name = user_data.get('name')
                                st.session_state.user_phone = user_data.get('phone')
                                st.session_state.user_email = user_data.get('email', '')
                                st.session_state.logged_in = True
                                st.success("Signed in successfully!")
                                st.session_state.login_otp_step = 'phone'
                                st.session_state.login_otp_phone = None
                                st.rerun()
                            else:
                                st.error(f"OTP login failed: {response.get('data', {}).get('message', 'Invalid OTP')}")

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
                        st.error("Phone number seems to short")
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
        # Fetch user info (uses auth token in api_client)
        user_info = api_client.get_user_info()
        user_name = "User"
        user_phone = ""
        user_email = ""
        user_data = {}

        if user_info.get("success"):
            user_data = user_info.get("data", {})
            user_name = user_data.get("name", "User")
            user_phone = user_data.get("phone", "")
            user_email = user_data.get("email", "")
            # Ensure session has user_id even after reloads
            if not st.session_state.get("user_id"):
                st.session_state.user_id = user_data.get("id")

        # Display only name by default
        st.write(f"Welcome, {user_name}!")

        # Show Profile button - when clicked show details
        if st.button("Show Profile"):
            st.markdown("---")
            if user_info.get("success"):
                st.write(f"**Phone:** {user_phone if user_phone else 'N/A'}")
                st.write(f"**Email:** {user_email if user_email else 'N/A'}")
            else:
                st.write("User details not available.")

            # Fetch and show audio contributions
            uid = (
                st.session_state.user_id
                or user_data.get("id")
                or (getattr(api_client, "user_data", {}) or {}).get("id")
            )
            if uid:
                contrib = api_client.get_user_contributions(uid)
                if contrib.get("success"):
                    audio_count = contrib.get("data", {}).get("contributions_by_media_type", {}).get("audio", 0)
                    st.write(f"🎤 Audio contributions: {audio_count}")
                else:
                    st.write("Could not fetch contributions.")
            else:
                st.write("No user id available.")

        st.markdown("---")

        # Logout button
        if st.button("Logout"):
            api_client.auth_token = None
            api_client.user_data = None
            for key in ['user_id', 'user_name', 'user_phone', 'user_email', 'logged_in']:
                if key in st.session_state:
                    del st.session_state[key]
            # No cookie clearing
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
                st.markdown(f"**Telugu:** {selected_sloka.get('sloka_text_telugu', 'N/A')}")

                st.markdown("---")

                # Meanings
                st.subheader("💭 Meanings")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Telugu Meaning:**")
                    st.write(selected_sloka.get('meaning_telugu', 'N/A'))

                with col2:
                    st.markdown("**English Meaning:**")
                    st.write(selected_sloka.get('meaning_english', 'N/A'))

                st.markdown("---")

                # Audio Upload Section using Swecha API
                st.subheader("🎤 Upload Your Audio")
                # Recorder detection status (for troubleshooting)
                recorder_label = _RECORDER_IMPL or "none"
                st.caption(f"Recorder backend: {recorder_label}")

                with st.expander("Recording diagnostics", expanded=False):
                    try:
                        import sys as _sys
                        st.write({
                            "python": _sys.version.split(" ")[0],
                            "executable": _sys.executable,
                            "recorder_impl": recorder_label,
                            "auth_token_set": bool(api_client.auth_token),
                        })
                        try:
                            import importlib
                            m0 = importlib.util.find_spec("audio_recorder_streamlit") is not None
                            m1 = importlib.util.find_spec("streamlit_mic_recorder") is not None
                            m2 = importlib.util.find_spec("audiorecorder") is not None
                            st.write({
                                "audio_recorder_streamlit_installed": m0,
                                "streamlit_mic_recorder_installed": m1,
                                "audiorecorder_installed": m2,
                            })
                        except Exception as _:
                            pass
                    except Exception as _:
                        pass

                # Category ID (UUID) required by backend
                category_id_input = st.text_input("Category ID (UUID)", value="", help="Enter a valid category UUID from Swecha Corpus")

                upload_tab1, upload_tab2 = st.tabs(["Recitation Audio", "Explanation Audio"])

                with upload_tab1:
                    st.write("Upload your recitation of this sloka")

                    upload_mode = st.radio(
                        "Choose input method",
                        ["Record audio", "Upload file"],
                        horizontal=True,
                        key="recitation_mode"
                    )

                    audio_bytes = None
                    filename = None

                    if upload_mode == "Upload file":
                        recitation_file = st.file_uploader(
                            "Choose recitation audio file",
                            type=['mp3', 'wav', 'ogg'],
                            key="recitation_upload",
                        )
                        if recitation_file is not None:
                            audio_bytes = recitation_file.read()
                            filename = (
                                f"recitation_{st.session_state.get('user_id') or (getattr(api_client, 'user_data', {}) or {}).get('id')}_{selected_sloka['id']}_{recitation_file.name}"
                            )

                    else:
                        if _RECORDING_AVAILABLE and _RECORDER_IMPL == "audio_recorder_streamlit":
                            st.markdown("<div style='padding:12px;border:1px solid rgba(255,255,255,0.2);border-radius:12px;background:rgba(255,255,255,0.06);margin-bottom:8px'>", unsafe_allow_html=True)
                            st.markdown("<div style='color:#fff;font-weight:600;margin-bottom:6px'>🎙️ Record Recitation</div>", unsafe_allow_html=True)
                            rec = audio_recorder(
                                text="",
                                icon_size="2x",
                                sample_rate=44100,
                                key="recitation_recorder",
                            )
                            st.markdown("</div>", unsafe_allow_html=True)
                            if rec:
                                st.audio(rec, format='audio/wav')
                                dur = _compute_wav_duration_seconds(rec)
                                st.caption(f"Duration: {dur} seconds")
                                audio_bytes = rec
                                uid = st.session_state.get('user_id') or (getattr(api_client, 'user_data', {}) or {}).get('id')
                                filename, title, description = _build_media_metadata(selected_chapter, selected_sloka, uid or "user", "recitation")
                        elif _RECORDING_AVAILABLE and _RECORDER_IMPL == "mic_recorder":
                            st.markdown("<div style='padding:12px;border:1px solid rgba(255,255,255,0.2);border-radius:12px;background:rgba(255,255,255,0.06);margin-bottom:8px'>", unsafe_allow_html=True)
                            st.markdown("<div style='color:#fff;font-weight:600;margin-bottom:6px'>🎙️ Hold to Record</div>", unsafe_allow_html=True)
                            rec = mic_recorder(start_prompt="🎙️ Hold to record", stop_prompt="⬆️ Release to stop", just_once=False, use_container_width=True, key="recitation_mic")
                            st.markdown("</div>", unsafe_allow_html=True)
                            if rec and rec.get('bytes'):
                                st.audio(rec['bytes'], format='audio/wav')
                                dur = _compute_wav_duration_seconds(rec['bytes'])
                                st.caption(f"Duration: {dur} seconds")
                                audio_bytes = rec['bytes']
                                uid = st.session_state.get('user_id') or (getattr(api_client, 'user_data', {}) or {}).get('id')
                                filename, title, description = _build_media_metadata(selected_chapter, selected_sloka, uid or "user", "recitation")
                        elif _RECORDING_AVAILABLE and _RECORDER_IMPL == "audiorecorder":
                            st.markdown("<div style='padding:12px;border:1px solid rgba(255,255,255,0.2);border-radius:12px;background:rgba(255,255,255,0.06);margin-bottom:8px'>", unsafe_allow_html=True)
                            st.markdown("<div style='color:#fff;font-weight:600;margin-bottom:6px'>🎙️ Click to Record</div>", unsafe_allow_html=True)
                            recorded = audiorecorder("Start recording", "Stop recording")
                            st.markdown("</div>", unsafe_allow_html=True)
                            if recorded and len(recorded) > 0:
                                preview_buf = io.BytesIO()
                                with wave.open(preview_buf, 'wb') as wf:
                                    wf.setnchannels(getattr(recorded, 'channels', 1))
                                    wf.setsampwidth(getattr(recorded, 'sample_width', 2))
                                    wf.setframerate(getattr(recorded, 'frame_rate', 44100))
                                    wf.writeframes(recorded.raw_data)
                                st.audio(preview_buf.getvalue(), format='audio/wav')
                                dur = _compute_wav_duration_seconds(preview_buf.getvalue())
                                st.caption(f"Duration: {dur} seconds")
                                audio_bytes = preview_buf.getvalue()
                                uid = st.session_state.get('user_id') or (getattr(api_client, 'user_data', {}) or {}).get('id')
                                filename, title, description = _build_media_metadata(selected_chapter, selected_sloka, uid or "user", "recitation")
                        else:
                            st.warning("Recording not available. Please install 'audio-recorder-streamlit==0.0.10' and restart the app.")

                    if audio_bytes is not None and st.button("Upload Recitation", key="upload_recitation"):
                        if not api_client.auth_token or api_client.auth_token == 'TEST_TOKEN':
                            st.error("You must be signed in with a real account to upload.")
                            with st.expander("Why did this fail?"):
                                st.write("Uploads require a valid backend token. Test mode tokens cannot upload.")
                        elif len(audio_bytes or b"") < 1000:
                            st.error("Recording seems too short or empty. Please record again.")
                        else:
                            with st.spinner("Uploading recitation to Swecha Corpus..."):
                                try:
                                    with open("recitation.wav", "wb") as f:
                                        f.write(audio_bytes)
                                    response = get_api_client().upload_complete_audio(
                                        #audio_data=audio_bytes,
                                        #filename=filename or "recitation.wav",
                                        filepath="recitation.wav",
                                        title = st.text_input("Enter Title", value="Bhagavad Gita Sloka") or "Untitled",

                                        category_id="ab9fa2ce-1f83-4e91-b89d-cca18e8b301e",
                                        language="telugu",
                                        release_rights="creator",
                                        description=st.text_input("Enter description", value="the sloka belongs to which chapter")
                                    )
                                    if response.get('success'):
                                        st.success("Recitation uploaded successfully to Swecha Corpus!")
                                        upload_data = response.get('data', {})
                                        if upload_data.get('id'):
                                            st.info(f"Upload ID: {upload_data['id']}")
                                    else:
                                        data = response.get('data', {}) or {}
                                        msg = data.get('message') or data.get('error') or data.get('detail') or 'Unknown error'
                                        st.error(f"Upload failed: {msg}")
                                        with st.expander("Show server response"):
                                            st.write({
                                                'status_code': response.get('status_code'),
                                                'data': data,
                                                'filename': filename,
                                                'bytes': len(audio_bytes or b'')
                                            })
                                except Exception as e:
                                    st.error(f"Upload error: {str(e)}")

                with upload_tab2:
                    st.write("Upload your explanation of this sloka")

                    upload_mode_exp = st.radio(
                        "Choose input method",
                        ["Record audio", "Upload file"],
                        horizontal=True,
                        key="explanation_mode"
                    )

                    audio_bytes_exp = None
                    filename_exp = None

                    if upload_mode_exp == "Upload file":
                        explanation_file = st.file_uploader(
                            "Choose explanation audio file",
                            type=['mp3', 'wav', 'ogg'],
                            key="explanation_upload",
                        )
                        if explanation_file is not None:
                            audio_bytes_exp = explanation_file.read()
                            filename_exp = (
                                f"explanation_{st.session_state.get('user_id') or (getattr(api_client, 'user_data', {}) or {}).get('id')}_{selected_sloka['id']}_{explanation_file.name}"
                            )
                    else:
                        if _RECORDING_AVAILABLE and _RECORDER_IMPL == "audio_recorder_streamlit":
                            st.markdown("<div style='padding:12px;border:1px solid rgba(255,255,255,0.2);border-radius:12px;background:rgba(255,255,255,0.06);margin-bottom:8px'>", unsafe_allow_html=True)
                            st.markdown("<div style='color:#fff;font-weight:600;margin-bottom:6px'>🎙️ Record Explanation</div>", unsafe_allow_html=True)
                            rec2 = audio_recorder(text="", icon_size="2x", sample_rate=44100, key="explanation_recorder")
                            st.markdown("</div>", unsafe_allow_html=True)
                            if rec2:
                                st.audio(rec2, format='audio/wav')
                                dur = _compute_wav_duration_seconds(rec2)
                                st.caption(f"Duration: {dur} seconds")
                                audio_bytes_exp = rec2
                                uid = st.session_state.get('user_id') or (getattr(api_client, 'user_data', {}) or {}).get('id')
                                filename_exp, title, description = _build_media_metadata(selected_chapter, selected_sloka, uid or "user", "explanation")
                        elif _RECORDING_AVAILABLE and _RECORDER_IMPL == "mic_recorder":
                            st.markdown("<div style='padding:12px;border:1px solid rgba(255,255,255,0.2);border-radius:12px;background:rgba(255,255,255,0.06);margin-bottom:8px'>", unsafe_allow_html=True)
                            st.markdown("<div style='color:#fff;font-weight:600;margin-bottom:6px'>🎙️ Hold to Record</div>", unsafe_allow_html=True)
                            rec2 = mic_recorder(start_prompt="🎙️ Hold to record", stop_prompt="⬆️ Release to stop", just_once=False, use_container_width=True, key="explanation_mic")
                            st.markdown("</div>", unsafe_allow_html=True)
                            if rec2 and rec2.get('bytes'):
                                st.audio(rec2['bytes'], format='audio/wav')
                                dur = _compute_wav_duration_seconds(rec2['bytes'])
                                st.caption(f"Duration: {dur} seconds")
                                audio_bytes_exp = rec2['bytes']
                                uid = st.session_state.get('user_id') or (getattr(api_client, 'user_data', {}) or {}).get('id')
                                filename_exp, title, description = _build_media_metadata(selected_chapter, selected_sloka, uid or "user", "explanation")
                        elif _RECORDING_AVAILABLE and _RECORDER_IMPL == "audiorecorder":
                            st.markdown("<div style='padding:12px;border:1px solid rgba(255,255,255,0.2);border-radius:12px;background:rgba(255,255,255,0.06);margin-bottom:8px'>", unsafe_allow_html=True)
                            st.markdown("<div style='color:#fff;font-weight:600;margin-bottom:6px'>🎙️ Click to Record</div>", unsafe_allow_html=True)
                            recorded_exp = audiorecorder("Start recording", "Stop recording")
                            st.markdown("</div>", unsafe_allow_html=True)
                            if recorded_exp and len(recorded_exp) > 0:
                                preview_buf2 = io.BytesIO()
                                with wave.open(preview_buf2, 'wb') as wf:
                                    wf.setnchannels(getattr(recorded_exp, 'channels', 1))
                                    wf.setsampwidth(getattr(recorded_exp, 'sample_width', 2))
                                    wf.setframerate(getattr(recorded_exp, 'frame_rate', 44100))
                                    wf.writeframes(recorded_exp.raw_data)
                                st.audio(preview_buf2.getvalue(), format='audio/wav')
                                dur = _compute_wav_duration_seconds(preview_buf2.getvalue())
                                st.caption(f"Duration: {dur} seconds")
                                audio_bytes_exp = preview_buf2.getvalue()
                                uid = st.session_state.get('user_id') or (getattr(api_client, 'user_data', {}) or {}).get('id')
                                filename_exp, title, description = _build_media_metadata(selected_chapter, selected_sloka, uid or "user", "explanation")
                        else:
                            st.warning("Recording not available. Please install 'audio-recorder-streamlit==0.0.10' and restart the app.")

                    if audio_bytes_exp is not None and st.button("Upload Explanation", key="upload_explanation"):
                        if not api_client.auth_token or api_client.auth_token == 'TEST_TOKEN':
                            st.error("You must be signed in with a real account to upload.")
                            with st.expander("Why did this fail?"):
                                st.write("Uploads require a valid backend token. Test mode tokens cannot upload.")
                        elif len(audio_bytes_exp or b"") < 1000:
                            st.error("Recording seems too short or empty. Please record again.")
                        else:
                            with st.spinner("Uploading explanation to Swecha Corpus..."):
                                try:
                                    response = get_api_client.upload_complete_audio(
                                        audio_data=audio_bytes_exp,
                                        filename=filename_exp or "explanation.wav",
                                        title=title,
                                        category_id=category_id_input.strip() or "1",
                                        language="telugu",
                                        release_rights="creator",
                                        description=description
                                    )
                                    if response.get('success'):
                                        st.success("Explanation uploaded successfully to Swecha Corpus!")
                                        upload_data = response.get('data', {})
                                        if upload_data.get('id'):
                                            st.info(f"Upload ID: {upload_data['id']}")
                                    else:
                                        data = response.get('data', {}) or {}
                                        msg = data.get('message') or data.get('error') or data.get('detail') or 'Unknown error'
                                        st.error(f"Upload failed: {msg}")
                                        with st.expander("Show server response"):
                                            st.write({
                                                'status_code': response.get('status_code'),
                                                'data': data,
                                                'filename': filename_exp,
                                                'bytes': len(audio_bytes_exp or b'')
                                            })
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