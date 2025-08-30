import http.client
import json
import uuid
import os
import websockets
import requests


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
                self.user_data = response["data"].get("user", {})
        
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
    
    def upload_audio_chunk(self, file_data: bytes, filename: str,
                           chunk_index: int, total_chunks: int, upload_uuid: str) -> dict:
        """Upload a single audio chunk (multipart/form-data)."""
        conn = http.client.HTTPSConnection(self.base_host)
        boundary = f"----formdata-{uuid.uuid4().hex}"

        # Build multipart body
        body = []
        # File chunk
        body.append(f"--{boundary}\r\n")
        body.append(f'Content-Disposition: form-data; name="chunk"; filename="{filename}"\r\n')
        body.append("Content-Type: application/octet-stream\r\n\r\n")
        body = "".join(body).encode() + file_data + b"\r\n"

        # Extra fields
        fields = {
            "filename": filename,
            "chunk_index": str(chunk_index),
            "total_chunks": str(total_chunks),
            "upload_uuid": upload_uuid,
        }
        for k, v in fields.items():
            body += (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'
            ).encode()

        body += f"--{boundary}--\r\n".encode()

        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }

        try:
            conn.request("POST", f"{self.api_base}/records/upload/chunk", body, headers)
            res = conn.getresponse()
            data = res.read()
            return {
                "status_code": res.status,
                "data": json.loads(data.decode("utf-8")) if data else {},
                "success": 200 <= res.status < 300,
            }
        finally:
            conn.close()

    def finalize_audio_upload(self, upload_uuid: str, total_chunks: int, filename: str,
                              title: str, category_id: str, language: str,
                              release_rights: str, description: str = "") -> dict:
        """Finalize audio upload with metadata (URL-encoded like JS)."""
        conn = http.client.HTTPSConnection(self.base_host)

        params = {
            "title": title,
            "description": description,
            "category_id": category_id,
            "user_id": self.user_data.get("id") if self.user_data else "",
            "media_type": "audio",
            "upload_uuid": upload_uuid,
            "filename": filename,
            "total_chunks": str(total_chunks),
            "release_rights": release_rights,
            "language": language,
            "use_uid_filename": "false",
        }

        body = urlencode(params)
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            conn.request("POST", f"{self.api_base}/records/upload", body, headers)
            res = conn.getresponse()
            data = res.read()
            return {
                "status_code": res.status,
                "data": json.loads(data.decode("utf-8")) if data else {},
                "success": 200 <= res.status < 300,
            }
        finally:
            conn.close()
    def upload_complete_audio(self, filepath: str, title: str,
                              category_id: str, language: str,
                              release_rights: str, description: str = "") -> dict:
        """
        Upload a full audio file (splits into 5MB chunks, uploads, then finalizes).
        Equivalent to the JavaScript submit handler.
        """
        if not self.auth_token:
            return {"success": False, "data": {"error": "Not authenticated"}}

        filename = filepath.split("/")[-1]
        upload_uuid = str(uuid.uuid4())

        with open(filepath, "rb") as f:
            audio_data = f.read()

        total_size = len(audio_data)
        total_chunks = (total_size + self.chunk_size - 1) // self.chunk_size

        # Upload chunks (0-based indexing)
        for chunk_index in range(total_chunks):
            start = chunk_index * self.chunk_size
            end = min(start + self.chunk_size, total_size)
            chunk_data = audio_data[start:end]

            result = self.upload_audio_chunk(
            chunk_data,      # file_data
            filename,        # filename
            chunk_index,     # chunk_index (0-based)
            total_chunks,    # total_chunks
            upload_uuid      # upload_uuid
            )
            if not result["success"]:
                return result  # stop on failure

        # Finalize upload
        return self.finalize_audio_upload(
            upload_uuid, total_chunks, filename, title,
            category_id, language, release_rights, description
        )

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

# Global API client instance
api_client = SwechaAPIClient()

def get_api_client():
    """Get the global API client instance"""
    return api_client
