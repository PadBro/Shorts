"""Module providing google drive connectivity."""

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

def login():
    """Function retriving google drive credentials."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("driveToken.json"):
        creds = Credentials.from_authorized_user_file("driveToken.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json", SCOPES
            )
            creds = flow.run_local_server(bind_addr="0.0.0.0", port=62432, open_browser=False)
        # Save the credentials for the next run
        with open("driveToken.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    try:
        return build("drive", "v3", credentials=creds)
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def create_folder(service, folder_path):
    """Function creatring folder in google drive."""
    path_parts = folder_path.split("/")
    print("creating folder " + path_parts[-1])
    try:
        file_metadata = {
            "name": path_parts[-1],
            "mimeType": "application/vnd.google-apps.folder",
        }

        file = service.files().create(body=file_metadata, fields="id").execute()
        print(f'created folder id: "{file.get("id")}"')
        return file.get("id")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def upload_file(service, folder_id, file_name, folder_path):
    """Function uploading a file to the provided folder in google drive."""
    print("uploading " + file_name)
    try:
        file_metadata = {"name": file_name, "parents": [folder_id]}

        media = MediaFileUpload(folder_path + "/" + file_name, resumable=True)
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print("uploaded " + file_name + " id: " + file.get("id"))

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.get("id")

def upload_folder(folder_path):
    """Function uploading the provided folder in google drive."""
    try:
        service = login()
        folder_id = create_folder(service, folder_path)

        files = os.listdir(folder_path)
        for file_name in files:
            upload_file(service, folder_id, file_name, folder_path)
        return folder_id
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
