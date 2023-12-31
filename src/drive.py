import os.path

import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

def login():
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
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("driveToken.json", "w") as token:
      token.write(creds.to_json())

  try:
    return build("drive", "v3", credentials=creds)
  except HttpError as error:
    print(f"An error occurred: {error}")

def createFolder(service, folderPath):
  pathParts = folderPath.split("/")
  print("creating folder " + pathParts[-1])
  try:
    file_metadata = {
        "name": pathParts[-1],
        "mimeType": "application/vnd.google-apps.folder",
    }

    file = service.files().create(body=file_metadata, fields="id").execute()
    print(f'created folder id: "{file.get("id")}"')
    return file.get("id")

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None

def uploadFile(service, folderId, fileName, folderPath):
  print("uploading " + fileName)
  try:
    file_metadata = {"name": fileName, "parents": [folderId]}

    media = MediaFileUpload(folderPath + "/" + fileName)
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    print("uploaded " + fileName + " id: " + file.get("id"))

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  return file.get("id")

def uploadFolder(folderPath):
  try:
    service = login()
    folderId = createFolder(service, folderPath)

    files = os.listdir(folderPath)
    for fileName in files:
      uploadFile(service, folderId, fileName, folderPath)
  except HttpError as error:
    print(f"An error occurred: {error}")

  return folderId

# uploadFolder("./output/2023-12-30_233708")