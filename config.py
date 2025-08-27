
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase Configuration (only for reference audio)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jutfhqtwfdmgedmdmizz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dGZocXR3ZmRtZ2VkbWRtaXp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1MDU0OTUsImV4cCI6MjA2OTA4MTQ5NX0.YKGcX4OvtQNJiNndKvC9mlX8gOC2xHpOuM2xnOrjI44")

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "")
SIGNIN_API_KEY = os.getenv("SIGNIN_API_KEY", "")
SIGNUP_API_KEY = os.getenv("SIGNUP_API_KEY", "")
AUDIO_UPLOAD_API_KEY = os.getenv("AUDIO_UPLOAD_API_KEY", "")

# Legacy configuration (kept for reference audio functionality)
AUDIO_STORAGE_PATH = os.getenv("AUDIO_STORAGE_PATH", r"gita\Gita_Guru\sloka")

# Validate that required environment variables are set
def check_environment():
    """Check if required environment variables are set"""
    missing_vars = []
    
    # Check Supabase for reference audio
    if not SUPABASE_URL:
        missing_vars.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing_vars.append("SUPABASE_KEY")
    
    # Check API configuration
    if not API_BASE_URL:
        missing_vars.append("API_BASE_URL")
    if not SIGNIN_API_KEY:
        missing_vars.append("SIGNIN_API_KEY")
    if not SIGNUP_API_KEY:
        missing_vars.append("SIGNUP_API_KEY")
    if not AUDIO_UPLOAD_API_KEY:
        missing_vars.append("AUDIO_UPLOAD_API_KEY")
    
    if missing_vars:
        print("⚠️  Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file in the project root with the following content:")
        print("# Supabase (for reference audio only)")
        print("SUPABASE_URL=https://your-project-id.supabase.co")
        print("SUPABASE_KEY=your-anon-key-here")
        print("\n# API Configuration")
        print("API_BASE_URL=your-api-base-url")
        print("SIGNIN_API_KEY=your-signin-api-key")
        print("SIGNUP_API_KEY=your-signup-api-key")
        print("AUDIO_UPLOAD_API_KEY=your-audio-upload-api-key")
        return False
    
    return True

# Check environment on import
check_environment()
