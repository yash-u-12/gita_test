#!/usr/bin/env python3
"""
Test script to verify all API endpoints and identify upload issues.
Run this script to test the API connectivity and upload functionality.
"""

import requests
import json
import os
import sys
import uuid
from api_client import SwechaAPIClient

def test_api_endpoints():
    """Test all API endpoints to verify connectivity and identify issues"""
    
    print("🔍 Testing API Endpoints...")
    print("=" * 50)
    
    # Initialize API client
    api_client = SwechaAPIClient()
    
    # Test 1: Check if API is reachable
    print("\n1. Testing API connectivity...")
    try:
        response = requests.get("https://api.corpus.swecha.org/api/v1/health", timeout=10)
        print(f"   ✅ API is reachable (Status: {response.status_code})")
        if response.status_code == 200:
            print(f"   📄 Response: {response.text}")
    except Exception as e:
        print(f"   ❌ API connectivity failed: {e}")
        return False
    
    # Test 2: Test login endpoint
    print("\n2. Testing login endpoint...")
    test_phone = "+919491418067"  # Use the phone with country code
    test_password = "Yashugupta1206"  # Use the correct password
    
    login_response = api_client.login(test_phone, test_password)
    print(f"   📊 Login response: {json.dumps(login_response, indent=2)}")
    
    if login_response.get("success"):
        print("   ✅ Login successful!")
        print(f"   🔑 Auth token: {api_client.auth_token[:20]}...")
        print(f"   👤 User ID: {api_client.user_data.get('id', 'N/A')}")
    else:
        print("   ❌ Login failed!")
        print("   ⚠️  Cannot proceed with authenticated endpoints")
        return False
    
    # Test 3: Test user info endpoint
    print("\n3. Testing user info endpoint...")
    user_info = api_client.get_user_info()
    print(f"   📊 User info response: {json.dumps(user_info, indent=2)}")
    
    # Test 4: Test categories endpoint (if it exists)
    print("\n4. Testing categories endpoint...")
    try:
        response = requests.get(
            "https://api.corpus.swecha.org/api/v1/categories",
            headers={"Authorization": f"Bearer {api_client.auth_token}"},
            timeout=10
        )
        print(f"   📊 Categories response (Status: {response.status_code}):")
        if response.status_code == 200:
            categories = response.json()
            print(f"   📋 Available categories: {json.dumps(categories, indent=2)}")
        else:
            print(f"   📄 Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Categories endpoint failed: {e}")
    
    # Test 5: Test upload chunk endpoint
    print("\n5. Testing upload chunk endpoint...")
    test_chunk = b"test audio data"
    test_filename = "test_audio.wav"
    test_uuid = str(uuid.uuid4())  # Generate proper UUID format
    
    try:
        files = {"chunk": (test_filename, test_chunk, "application/octet-stream")}
        data = {
            "filename": test_filename,
            "chunk_index": 0,
            "total_chunks": 1,
            "upload_uuid": test_uuid
        }
        headers = {"Authorization": f"Bearer {api_client.auth_token}"}
        
        response = requests.post(
            "https://api.corpus.swecha.org/api/v1/records/upload/chunk",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        print(f"   📊 Upload chunk response (Status: {response.status_code}):")
        print(f"   📄 Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Upload chunk endpoint working!")
        else:
            print("   ❌ Upload chunk endpoint failed!")
            
    except Exception as e:
        print(f"   ❌ Upload chunk test failed: {e}")
    
    # Test 6: Test upload finalization endpoint
    print("\n6. Testing upload finalization endpoint...")
    try:
        data = {
            "title": "Test Audio Upload",
            "description": "Test upload for API verification",
            "media_type": "audio",
            "filename": test_filename,
            "total_chunks": 1,
            "release_rights": "creator",
            "language": "telugu",
            "upload_uuid": test_uuid,
            "user_id": api_client.user_data.get("id", ""),
            "category_id": "ab9fa2ce-1f83-4e91-b89d-cca18e8b301e"  # Using the hardcoded category ID
        }
        headers = {"Authorization": f"Bearer {api_client.auth_token}"}
        
        # Get user info to ensure we have the correct user ID
        user_info_response = requests.get(
            "https://api.corpus.swecha.org/api/v1/auth/me",
            headers=headers,
            timeout=10
        )
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            data["user_id"] = user_info.get("id", "")
        
        response = requests.post(
            "https://api.corpus.swecha.org/api/v1/records/upload",
            data=data,
            headers=headers,
            timeout=30
        )
        print(f"   📊 Upload finalization response (Status: {response.status_code}):")
        print(f"   📄 Response: {response.text}")
        
        if response.status_code in [200, 201]:
            print("   ✅ Upload finalization endpoint working!")
        else:
            print("   ❌ Upload finalization endpoint failed!")
            
    except Exception as e:
        print(f"   ❌ Upload finalization test failed: {e}")
    
    # Test 7: Test complete upload flow
    print("\n7. Testing complete upload flow...")
    
    # Create a small test audio file
    test_audio_path = "test_recitation.wav"
    try:
        # Create a simple WAV file for testing
        import wave
        import struct
        
        with wave.open(test_audio_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(44100)  # 44.1kHz
            
            # Generate 1 second of silence
            frames = b''.join([struct.pack('<h', 0) for _ in range(44100)])
            wav_file.writeframes(frames)
        
        print(f"   📁 Created test audio file: {test_audio_path}")
        
        # Test the complete upload
        upload_result = api_client.upload_complete_audio(
            filepath=test_audio_path,
            title="Test Recitation",
            category_id="ab9fa2ce-1f83-4e91-b89d-cca18e8b301e",
            language="telugu",
            release_rights="creator",
            description="Test upload for API verification"
        )
        
        print(f"   📊 Complete upload result: {json.dumps(upload_result, indent=2)}")
        
        if upload_result.get("success"):
            print("   ✅ Complete upload flow working!")
        else:
            print("   ❌ Complete upload flow failed!")
            
        # Clean up test file
        if os.path.exists(test_audio_path):
            os.remove(test_audio_path)
            print(f"   🗑️  Cleaned up test file: {test_audio_path}")
            
    except Exception as e:
        print(f"   ❌ Complete upload test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 API endpoint testing completed!")
    
    return True

if __name__ == "__main__":
    test_api_endpoints()
