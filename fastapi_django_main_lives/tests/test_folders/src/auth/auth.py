import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request

class Authenticator:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file

    def authenticate(self):
        # Load credentials from file
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_file, scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        # Create a client instance with the credentials
        client = Request()
        credentials.refresh_token = client.request()
        return credentials