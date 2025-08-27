import os
import uuid
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        # Public client for reading chapters, slokas, and reference audio
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # ---------------- Chapters / Slokas (Read Only) ----------------
    def get_chapter_by_number(self, chapter_number: int):
        try:
            result = self.supabase.table('chapters').select('*').eq('chapter_number', chapter_number).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting chapter {chapter_number}: {e}")
            return None

    def get_sloka_by_chapter_and_number(self, chapter_id: str, sloka_number: int):
        try:
            result = self.supabase.table('slokas').select('*').eq('chapter_id', chapter_id).eq('sloka_number', sloka_number).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting sloka {sloka_number}: {e}")
            return None

    def get_all_chapters(self):
        try:
            result = self.supabase.table('chapters').select('*').order('chapter_number').execute()
            return result.data
        except Exception as e:
            print(f"Error getting chapters: {e}")
            return []

    def get_slokas_by_chapter(self, chapter_id: str):
        try:
            result = self.supabase.table('slokas').select('*').eq('chapter_id', chapter_id).order('sloka_number').execute()
            return result.data
        except Exception as e:
            print(f"Error getting slokas for chapter {chapter_id}: {e}")
            return []

# Global instance - lazy initialization
_db_manager_instance = None

def get_db_manager():
    """Get the global database manager instance, creating it if necessary"""
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
    return _db_manager_instance

# For backward compatibility
class LazyDBManager:
    def __getattr__(self, name):
        return getattr(get_db_manager(), name)

db_manager = LazyDBManager()