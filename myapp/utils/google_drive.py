from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from pathlib import Path

# Ambil path dasar proyek (lokasi manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Path ke service account JSON
SERVICE_ACCOUNT_FILE = BASE_DIR / "credentials" / "drive_service_account.json"

# Scope untuk akses Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def upload_to_drive(file_path, file_name, folder_id=None):
    """
    Upload file ke Google Drive
    :param file_path: path lokal file
    :param file_name: nama file di Drive
    :param folder_id: (opsional) ID folder di Drive
    :return: tuple (file_id, webViewLink)
    """

    # Autentikasi dengan Service Account
    creds = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE), scopes=SCOPES
    )

    # Bangun service
    service = build("drive", "v3", credentials=creds)

    # Metadata file
    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    # Siapkan media upload
    media = MediaFileUpload(file_path, resumable=True)

    # Eksekusi upload
    file = service.files().create(
        body=file_metadata, media_body=media, fields="id, webViewLink"
    ).execute()

    return file.get("id"), file.get("webViewLink")
