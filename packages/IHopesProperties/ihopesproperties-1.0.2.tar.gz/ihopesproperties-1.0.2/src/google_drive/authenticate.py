import os
import pickle
from functools import lru_cache
from pathlib import Path
from typing import Tuple

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

# If modifying the scope, delete the token.pickle file.
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]


@lru_cache(maxsize=1)  # Cache only one result
def authenticate() -> Tuple[Resource, Resource]:
    # Authenticate and create the service

    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    parent_path: Path = Path(os.path.abspath(__file__)).parent
    token_file_path: Path = Path(parent_path, 'token.pickle')

    if os.path.exists(token_file_path):
        with open(token_file_path, 'rb') as token:
            # from google.oauth2.credentials import Credentials
            # creds2 = Credentials.from_authorized_user_file('token.json', scopes=['your-scopes'])

            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # if creds and creds.expired and creds.refresh_token:
        #     creds.refresh(Request())
        # else:
        flow = InstalledAppFlow.from_client_secrets_file(f'{parent_path}/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file_path, 'wb') as token:
            pickle.dump(creds, token)

    # Build the Drive API service
    drive_resource: Resource = build('drive', 'v3', credentials=creds)
    sheets_resource: Resource = build('sheets', 'v4', credentials=creds)
    return drive_resource, sheets_resource
