from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleApiClient:
    def __init__(self, credentials):
        self.credentials = credentials

    def build_service(self, api_name, api_version):
        # Build the API client instance
        return build(api_name, api_version, credentials=self.credentials)