import os
import uuid
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY

class DatabaseManager:
    def __init__(self):
        # Public client (anon) used for storage and regular reads (subject to RLS)
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        # Admin client (service role) for checks/inserts that must bypass RLS (server-side use only)
        if SUPABASE_SERVICE_ROLE_KEY:
            self.admin_client: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        else:
            self.admin_client = None

    # ---------------- Chapters / Slokas ----------------
    def create_chapter(self, chapter_number: int, chapter_name: str):
        try:
            if not self.admin_client:
                print("Admin client not available. Cannot create chapter.")
                return None
            data = {'chapter_number': chapter_number, 'chapter_name': chapter_name}
            result = self.admin_client.table('chapters').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating chapter {chapter_number}: {e}")
            return None

    def upsert_sloka(self, chapter_id: str, sloka_number: int, sloka_text_telugu: str,
                     meaning_telugu: str, meaning_english: str, reference_audio_url: str = None):
        try:
            if not self.admin_client:
                print("Admin client not available. Cannot upsert sloka.")
                return None
            existing = self.admin_client.table('slokas').select('*').eq('chapter_id', chapter_id).eq('sloka_number', sloka_number).execute()
            data = {
                'chapter_id': chapter_id,
                'sloka_number': sloka_number,
                'sloka_text_telugu': sloka_text_telugu,
                'meaning_telugu': meaning_telugu,
                'meaning_english': meaning_english,
                'reference_audio_url': reference_audio_url
            }
            if existing.data:
                result = self.admin_client.table('slokas').update(data).eq('id', existing.data[0]['id']).execute()
            else:
                result = self.admin_client.table('slokas').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error upserting sloka {sloka_number}: {e}")
            return None

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

    def update_sloka_audio_url(self, sloka_id: str, audio_url: str):
        try:
            if not self.admin_client:
                print("Admin client not available. Cannot update sloka audio URL.")
                return None
            result = self.admin_client.table('slokas').update({'reference_audio_url': audio_url}).eq('id', sloka_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating sloka audio URL: {e}")
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

    # ---------------- Users ----------------
    def create_user(self, user_id: str, name: str, email: str):
        """
        Inserts user using admin client (bypassing RLS). Use only from trusted server code.
        """
        try:
            if not self.admin_client:
                print("Admin client not available. Cannot create user.")
                return None
            data = {'id': user_id, 'name': name, 'email': email}
            result = self.admin_client.table('users').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def get_user_by_email(self, email: str):
        try:
            if self.admin_client:
                result = self.admin_client.table('users').select('*').eq('email', email).execute()
            else:
                result = self.supabase.table('users').select('*').eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    def get_user_by_id(self, user_id: str):
        try:
            if self.admin_client:
                result = self.admin_client.table('users').select('*').eq('id', user_id).execute()
            else:
                result = self.supabase.table('users').select('*').eq('id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None

    def create_user_if_not_exists(self, user_id: str, name: str, email: str):
        """
        Ensure a single canonical user row: check by id and email and create only when missing.
        Returns existing/new user row.
        """
        try:
            # Check by id
            existing = self.get_user_by_id(user_id)
            if existing:
                return existing

            # Check by email
            existing = self.get_user_by_email(email)
            if existing:
                return existing

            # Try to insert using available client
            if self.admin_client:
                # Use admin client if available (bypasses RLS)
                result = self.admin_client.table('users').insert({
                    'id': user_id,
                    'name': name,
                    'email': email
                }).execute()
            else:
                # Use regular client (subject to RLS policies)
                result = self.supabase.table('users').insert({
                    'id': user_id,
                    'name': name,
                    'email': email
                }).execute()

            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user: {e}")
            # Return a mock user object if creation fails
            return {
                'id': user_id,
                'name': name,
                'email': email
            }

    # ---------------- Submissions ----------------
    def create_user_submission(self, user_id: str, sloka_id: str, recitation_audio_url: str = None, explanation_audio_url: str = None):
        try:
            data = {
                'user_id': user_id,
                'sloka_id': sloka_id,
                'recitation_audio_url': recitation_audio_url,
                'explanation_audio_url': explanation_audio_url,
                'status': 'Submitted'
            }
            result = self.admin_client.table('user_submissions').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user submission: {e}")
            return None

    def get_user_submissions(self, user_id: str = None, sloka_id: str = None, status: str = None):
        try:
            query = self.admin_client.table('user_submissions').select('*, users(name, email), slokas(sloka_number, sloka_text_telugu)')
            if user_id:
                query = query.eq('user_id', user_id)
            if sloka_id:
                query = query.eq('sloka_id', sloka_id)
            if status:
                query = query.eq('status', status)
            result = query.order('created_at', desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error getting user submissions: {e}")
            return []

    def update_submission_status(self, submission_id: str, status: str, admin_notes: str = None):
        try:
            data = {'status': status}
            if admin_notes:
                data['admin_notes'] = admin_notes
            result = self.admin_client.table('user_submissions').update(data).eq('id', submission_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating submission status: {e}")
            return None

    # exposing admin_client for convenience if needed elsewhere (use carefully)
    @property
    def admin(self):
        return self.admin_client

# Global instance - lazy initialization
_db_manager_instance = None

def get_db_manager():
    """Get the global database manager instance, creating it if necessary"""
    global _db_manager_instance
    if _db_manager_instance is None:
        _db_manager_instance = DatabaseManager()
    return _db_manager_instance

# For backward compatibility - create a property that calls get_db_manager
class LazyDBManager:
    def __getattr__(self, name):
        return getattr(get_db_manager(), name)

db_manager = LazyDBManager()
