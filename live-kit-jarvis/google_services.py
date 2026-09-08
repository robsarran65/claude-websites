import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_google_creds() -> Credentials:
    """Load cached Google OAuth credentials, refreshing or re-authenticating as needed."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def gmail_service():
    return build("gmail", "v1", credentials=get_google_creds())


def calendar_service():
    return build("calendar", "v3", credentials=get_google_creds())
