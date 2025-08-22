import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase Configuration
# You need to set these values in your .env file or environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jutfhqtwfdmgedmdmizz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp1dGZocXR3ZmRtZ2VkbWRtaXp6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1MDU0OTUsImV4cCI6MjA2OTA4MTQ5NX0.YKGcX4OvtQNJiNndKvC9mlX8gOC2xHpOuM2xnOrjI44")
AUDIO_STORAGE_PATH = os.getenv("AUDIO_STORAGE_PATH", r"gita\Gita_Guru\sloka")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "") 

# Validate that required environment variables are set
def check_environment():
    """Check if required environment variables are set"""
    missing_vars = []
    
    if not SUPABASE_URL:
        missing_vars.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        missing_vars.append("SUPABASE_KEY")
    # Note: SUPABASE_SERVICE_ROLE_KEY is optional for basic functionality
    
    if missing_vars:
        print("⚠️  Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file in the project root with the following content:")
        print("SUPABASE_URL=https://your-project-id.supabase.co")
        print("SUPABASE_KEY=your-anon-key-here")
        print("SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here")
        print("\nYou can find these values in your Supabase dashboard under Settings > API.")
        return False
    
    return True

# Check environment on import
check_environment()
