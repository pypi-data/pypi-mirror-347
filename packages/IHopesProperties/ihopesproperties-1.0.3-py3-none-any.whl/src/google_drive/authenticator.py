import os
import pickle
import sys
from functools import lru_cache
from pathlib import Path
from typing import Tuple, Optional
from functools import lru_cache

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
import streamlit as st


def is_streamlit_runtime() -> bool:
    """
    Check if the script is running in a Streamlit runtime environment.
    :return:
    """
    return any("streamlit" in arg for arg in sys.argv)


CACHE_DECORATOR = st.cache_resource if is_streamlit_runtime() else lru_cache(maxsize=1)


class GoogleServices:
    _instance: Optional["GoogleServices"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self._creds = None
        self.drive: Optional[Resource] = None
        self.sheets: Optional[Resource] = None

        self.scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]

        self.authenticate()
        self._initialized = True

    def authenticate(self) -> None:
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
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file=f'{parent_path}/credentials.json',
                scopes=self.scopes
            )

            if is_streamlit_runtime():
                auth_url, _ = flow.authorization_url(prompt='consent')

                st.markdown("### 🔐 Google Authentication Required")
                st.markdown(f"[Click here to authenticate]({auth_url})")
                code = st.text_input("Paste the authorization code here:")

                if code:
                    try:
                        flow.fetch_token(code=code)
                        creds = flow.credentials
                        with open(token_file_path, 'wb') as token:
                            pickle.dump(creds, token)
                        st.success("✅ Authentication successful!")
                    except Exception as e:
                        st.error(f"❌ Authentication failed: {e}")
                else:
                    st.stop()
            else:
                creds = flow.run_local_server(port=0)
                with open(token_file_path, 'wb') as token:
                    pickle.dump(creds, token)

        # Build the Drive API service
        self.drive: Resource = build('drive', 'v3', credentials=creds)
        self.sheets: Resource = build('sheets', 'v4', credentials=creds)


def get_google_services() -> GoogleServices:
    return GoogleServices()