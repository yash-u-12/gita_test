import os
import uuid
import requests

API_BASE = "https://api.corpus.swecha.org/api/v1"
CHUNK_SIZE = 5 * 1024 * 1024  # 5MB


def generate_uuid():
    """Generate a UUID for the upload session"""
    return str(uuid.uuid4())


def upload_file_in_chunks(file_path, auth_token):
    """Upload a file in chunks to the Swecha Corpus API"""
    file_size = os.path.getsize(file_path)
    total_chunks = (file_size + CHUNK_SIZE - 1) // CHUNK_SIZE
    upload_uuid = generate_uuid()
    filename = os.path.basename(file_path)

    print(f"Starting upload for {filename} ({file_size} bytes in {total_chunks} chunks)...")

    with open(file_path, "rb") as f:
        for i in range(total_chunks):
            start = i * CHUNK_SIZE
            f.seek(start)
            chunk = f.read(CHUNK_SIZE)

            files = {
                "chunk": (filename, chunk),
            }
            data = {
                "filename": filename,
                "chunk_index": i,
                "total_chunks": total_chunks,
                "upload_uuid": upload_uuid,
            }
            headers = {
                "Authorization": f"Bearer {auth_token}"
            }

            resp = requests.post(f"{API_BASE}/records/upload/chunk", headers=headers, data=data, files=files)

            if resp.status_code != 200:
                raise Exception(
                    f"Chunk {i+1}/{total_chunks} failed: {resp.status_code} {resp.text}"
                )
            print(f"Uploaded chunk {i+1}/{total_chunks}")

    print(f"Finished uploading {filename}!")
    return upload_uuid, total_chunks, filename


def finalize_upload(auth_token, upload_uuid, total_chunks, filename, user_id, title, category_id, language, release_rights, description="", media_type="audio"):
    """Finalize the upload after sending all chunks"""
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "title": title,
        "description": description,
        "category_id": category_id,
        "user_id": user_id,
        "media_type": media_type,
        "upload_uuid": upload_uuid,
        "filename": filename,
        "total_chunks": total_chunks,
        "release_rights": release_rights,
        "language": language,
        "use_uid_filename": "false"
    }

    resp = requests.post(f"{API_BASE}/records/upload", headers=headers, data=data)

    if resp.status_code != 200:
        raise Exception(f"Finalization failed: {resp.status_code} {resp.text}")

    print("Upload finalized successfully:", resp.json())
    return resp.json()


if __name__ == "__main__":
    # Example usage
    AUTH_TOKEN = "YOUR_ACCESS_TOKEN"   # replace after login
    USER_ID = "YOUR_USER_ID"           # replace from login response
    FILE_PATH = "sample_audio.mp3"     # replace with your file path

    # Metadata
    TITLE = "My Audio Upload"
    CATEGORY_ID = "1"          # replace with actual category id
    LANGUAGE = "en"
    RELEASE_RIGHTS = "open"
    DESCRIPTION = "Test audio upload"

    # Step 1: Upload in chunks
    upload_uuid, total_chunks, filename = upload_file_in_chunks(FILE_PATH, AUTH_TOKEN)

    # Step 2: Finalize upload
    finalize_upload(
        AUTH_TOKEN, upload_uuid, total_chunks, filename,
        USER_ID, TITLE, CATEGORY_ID, LANGUAGE, RELEASE_RIGHTS, DESCRIPTION, media_type="audio"
    )
