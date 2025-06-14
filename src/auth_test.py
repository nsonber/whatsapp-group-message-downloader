from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate():
    creds = None
    token_path = 'token.json'
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds

def test_drive_api(creds):
    drive_service = build('drive', 'v3', credentials=creds)
    results = drive_service.files().list(pageSize=10, fields="files(id, name)").execute()
    files = results.get('files', [])
    print("Drive files:")
    for file in files:
        print(f"{file['name']} ({file['id']})")

def test_sheets_api(creds):
    sheets_service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '19O2xCcJSxcoOJEj4hI3y8oEyScH-h8WHMCjiCqyu_cU'  # Replace with VKA_Messages ID
    result = sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Sheet1!A1:F1').execute()
    print("Sheets headers:")
    print(result.get('values', []))

if __name__ == '__main__':
    creds = authenticate()
    test_drive_api(creds)
    test_sheets_api(creds)