import http.client
import json
import uuid
import os
import websockets
import requests
import streamlit as st


from typing import Optional, Dict, Any
from urllib.parse import urlencode

class SwechaAPIClient:
    def __init__(self):
        self.base_host = "api.corpus.swecha.org"
        self.api_base = "/api/v1"
        self.api_base_url = "https://api.corpus.swecha.org/api/v1"
        self.auth_token = None
        self.user_data = None
        self.chunk_size = 5 * 1024 * 1024  # 5MB 

        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, payload: Dict = None, headers: Dict = None, require_auth: bool = False) -> Dict:
        """Make HTTP request to Swecha API"""
        conn = http.client.HTTPSConnection(self.base_host, timeout=10)  # Add timeout
        
        default_headers = {"content-type": "application/json"}
        if headers:
            default_headers.update(headers)
        
        if require_auth and self.auth_token:
            default_headers["authorization"] = f"Bearer {self.auth_token}"
        
        payload_str = json.dumps(payload) if payload else None
        
        try:
            conn.request(method, f"{self.api_base}{endpoint}", payload_str, default_headers)
            res = conn.getresponse()
            data = res.read()
            try:
                response_data = json.loads(data.decode("utf-8"))
            except Exception:
                response_data = {"raw": data.decode("utf-8")}
            # Add debug info for server errors
            if res.status >= 500:
                print("DEBUG: Server Error", res.status, endpoint)
                print("Payload:", payload)
                print("Response:", response_data)
            return {
                "status_code": res.status,
                "data": response_data,
                "success": 200 <= res.status < 300
            }
        except Exception as e:
            print("DEBUG: Exception during API request:", str(e))
            return {
                "status_code": 500,
                "data": {"error": str(e)},
                "success": False
            }
        finally:
            conn.close()
    
    def login(self, phone: str, password: str) -> Dict[str, Any]:
        """Login user with phone and password"""
        payload = {
            "phone": phone,
            "password": password
        }
        
        response = self._make_request("POST", "/auth/login", payload)
        
        if response["success"]:
            # Extract token and user data from response
            token = response["data"].get("access_token")
            if token:
                self.auth_token = token
                # For login endpoint, user data might be in a different structure
                # Try to get user data from the response
                user_data = response["data"].get("user", {})
                if not user_data:
                    # If no user data in response, we'll get it from /auth/me endpoint
                    user_info = self.get_user_info()
                    if user_info.get("success"):
                        user_data = user_info.get("data", {})
                self.user_data = user_data
                # Set authorization header in session
                self.session.headers.update({"Authorization": f"Bearer {token}"})
        
        return response
    
    def send_signup_otp(self, phone_number: str) -> Dict[str, Any]:
        """Send OTP for signup"""
        payload = {
            "phone_number": phone_number
        }
        
        return self._make_request("POST", "/auth/signup/send-otp", payload)
    
    def verify_signup_otp(self, phone_number: str, otp_code: str, name: str, email: str, password: str, has_given_consent: bool = True) -> Dict[str, Any]:
        """Verify OTP and complete signup"""
        payload = {
            "phone_number": phone_number,
            "otp_code": otp_code,
            "name": name,
            "email": email,
            "password": password,
            "has_given_consent": has_given_consent
        }
        
        return self._make_request("POST", "/auth/signup/verify-otp", payload)
    
    def change_password(self, current_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password"""
        payload = {
            "current_password": current_password,
            "new_password": new_password
        }
        
        return self._make_request("POST", "/auth/change-password", payload, require_auth=True)
    
    def get_user_contributions(self, user_id: str) -> Dict[str, Any]:
        """Get user contributions"""
        return self._make_request("GET", f"/users/{user_id}/contributions", require_auth=True)
    def _handle_response(self, response: requests.Response) -> Optional[Dict]:
        """Handle API response and errors"""
        try:
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 401:
                st.error("Authentication failed. Please login again.")
                st.session_state.authenticated = False
                return None
            elif response.status_code == 422:
                try:
                    error_detail = response.json().get('detail', 'Validation error')
                    st.error(f"Validation error: {error_detail}. Full response: {response.text}") # Log full response text
                except ValueError:
                    st.error(f"Validation error: Could not parse error detail. Full response: {response.text}")
                return None
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")
                return None
        except Exception as e:
            st.error(f"Error processing response: {str(e)}")
            return None 
    
    def upload_audio_chunk(self, chunk_data: bytes, filename: str, chunk_index: int, total_chunks: int, upload_uuid: str) -> Dict:
        """Upload a single chunk of a file (POST /api/v1/records/upload/chunk)"""
        try:
            files = {"chunk": (filename, chunk_data, "application/octet-stream")}
            data = {
                "filename": filename,
                "chunk_index": chunk_index,
                "total_chunks": total_chunks,
                "upload_uuid": upload_uuid
            }
            
            # Ensure authorization header is set
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"

            response = self.session.post(
                f"{self.api_base_url}/records/upload/chunk",  # Fixed URL - removed duplicate /api/v1
                files=files,
                data=data,
                headers=headers
            )
            response_data = self._handle_response(response)
            if response_data:
                st.info(f"Chunk upload response: {response_data}") # Log the response
                return {"success": True, "data": response_data}
            else:
                return {"success": False, "data": {"error": "Failed to upload chunk"}}
        except requests.RequestException as e:
            st.error(f"File chunk upload error: {str(e)}")
            return {"success": False, "data": {"error": str(e)}}

    def finalize_audio_upload(self, title: str, description: str, media_type: str, filename: str, total_chunks: int, release_rights: str, language: str, upload_uuid: str, user_id: str, category_id: str, latitude: Optional[float] = None, longitude: Optional[float] = None, use_uid_filename: Optional[bool] = None) -> Optional[Dict]:
        """Finalize chunked upload and create a record (POST /api/v1/records/upload)"""
        try:
            data = {
                "title": title,
                "description": description,
                "media_type": media_type,
                "filename": filename,
                "total_chunks": total_chunks,
                "release_rights": release_rights,
                "language": language,
                "upload_uuid": upload_uuid,
                "user_id": user_id,
                "category_id": category_id,
            }
            if latitude is not None:
                data["latitude"] = latitude
            if longitude is not None:
                data["longitude"] = longitude
            if use_uid_filename is not None:
                data["use_uid_filename"] = use_uid_filename

            st.info(f"Finalizing record with data: {data}") # Added logging for data being sent

            # Set authorization header
            headers = {}
            if self.auth_token:
                headers["Authorization"] = f"Bearer {self.auth_token}"

            response = self.session.post(
                f"{self.api_base_url}/records/upload",  # Fixed URL - removed duplicate /api/v1
                data=data, # Send data as form-encoded
                headers=headers
            )
            response_data = self._handle_response(response)
            if response_data:
                return {"success": True, "data": response_data}
            else:
                return {"success": False, "data": {"error": "Failed to finalize upload"}}
        except requests.RequestException as e:
            st.error(f"Record finalization error: {str(e)}")
            return None

    def upload_complete_audio(self, filepath: str = None, audio_data: bytes = None, filename: str = None, title: str = "",
                              category_id: str = "", language: str = "telugu",
                              release_rights: str = "creator", description: str = "") -> dict:
        """
        Upload a full audio file (splits into 5MB chunks, uploads, then finalizes).
        Supports both filepath and audio_data parameters.
        """
        if not self.auth_token:
            return {"success": False, "data": {"error": "Not authenticated"}}

        # Handle audio_data parameter
        if audio_data is not None:
            if not filename:
                filename = f"audio_{uuid.uuid4().hex[:8]}.wav"
            audio_bytes = audio_data
        elif filepath:
            filename = filepath.split("/")[-1]
            with open(filepath, "rb") as f:
                audio_bytes = f.read()
        else:
            return {"success": False, "data": {"error": "Either filepath or audio_data must be provided"}}

        upload_uuid = str(uuid.uuid4())
        total_size = len(audio_bytes)
        total_chunks = (total_size + self.chunk_size - 1) // self.chunk_size
        media_type = "audio"
        user_id = self.user_data.get("id", "")

        # Upload chunks (0-based indexing)
        for chunk_index in range(total_chunks):
            start = chunk_index * self.chunk_size
            end = min(start + self.chunk_size, total_size)
            chunk_data = audio_bytes[start:end]

            result = self.upload_audio_chunk(
            chunk_data,      # file_data
            filename,        # filename
            chunk_index,     # chunk_index (0-based)
            total_chunks,    # total_chunks
            upload_uuid      # upload_uuid
            )
            if not result.get("success"):
                return result  # stop on failure

        # Finalize upload
        finalize_result = self.finalize_audio_upload(
            title,description,media_type,filename,total_chunks, release_rights, 
             language,upload_uuid,user_id,category_id,latitude=None,longitude=None,use_uid_filename=None
        )
        
        if finalize_result:
            return {"success": True, "data": finalize_result}
        else:
            return {"success": False, "data": {"error": "Failed to finalize upload"}}

    def send_login_otp(self, phone_number: str) -> dict:
        """Send OTP for login"""
        payload = {
            "phone_number": phone_number
        }
        return self._make_request("POST", "/auth/login/send-otp", payload)

    def verify_login_otp(self, phone_number: str, otp_code: str, has_given_consent: bool = True) -> dict:
        """Verify OTP and login"""
        payload = {
            "phone_number": phone_number,
            "otp_code": otp_code,
            "has_given_consent": has_given_consent
        }
        response = self._make_request("POST", "/auth/login/verify-otp", payload)
        if response.get("success"):
            token = response["data"].get("access_token")
            if token:
                self.auth_token = token
                self.user_data = response["data"].get("user", {})
                # Set authorization header in session
                self.session.headers.update({"Authorization": f"Bearer {token}"})
        return response

    def get_user_info(self) -> dict:
        """Get user info using auth token"""
        if not self.auth_token:
            return {"success": False, "data": {"error": "Not authenticated"}}
        headers = {"authorization": f"Bearer {self.auth_token}"}
        return self._make_request("GET", "/auth/me", headers=headers, require_auth=True)

    def get_user_audio_contributions(self, user_id: str) -> dict:
        """Get only audio contributions count for user"""
        if not self.auth_token:
            return {"success": False, "data": {"error": "Not authenticated"}}
        headers = {"authorization": f"Bearer {self.auth_token}"}
        endpoint = f"/users/{user_id}/contributions"
        response = self._make_request("GET", endpoint, headers=headers, require_auth=True)
        audio_count = 0
        if response.get("success"):
            contrib = response.get("data", {}).get("contributions_by_media_type", {})
            audio_count = contrib.get("audio", 0)
        response["audio_count"] = audio_count
        return response

    def get_categories(self) -> dict:
        """Get available categories for uploads"""
        if not self.auth_token:
            return {"success": False, "data": {"error": "Not authenticated"}}
        
        try:
            response = self.session.get(
                f"{self.api_base_url}/categories",
                headers={"Authorization": f"Bearer {self.auth_token}"},
                timeout=10
            )
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "data": {"error": f"Status {response.status_code}: {response.text}"}}
        except requests.RequestException as e:
            return {"success": False, "data": {"error": str(e)}}

# Global API client instance
api_client = SwechaAPIClient()

def get_api_client():
    """Get the global API client instance"""
    return api_client
