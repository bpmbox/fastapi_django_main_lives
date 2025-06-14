import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleAppsScript:
    def __init__(self, script_id):
        self.script_id = script_id
        self.service = self._build_service()

    def _build_service(self):
        api_name = "script"
        api_version = "v1"
        client_secret_file = "client_secret.json"
        scopes = ["https://www.googleapis.com/auth/script.projects"]

        creds, project = self._get_credentials(client_secret_file, scopes)
        service = build(api_name, api_version, credentials=creds)
        return service

    def _get_credentials(self, client_secret_file, scopes):
        import os
        import json
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request

        creds = None
        if os.path.exists(client_secret_file):
            creds = service_account.Credentials.from_service_account_file(
                client_secret_file, scopes=scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds = service_account.Credentials.from_service_account_file(
                    client_secret_file, scopes=scopes)
        return creds, None

    def execute_script(self, function_name, params):
        try:
            request = {"function": function_name, "parameters": params}
            response = self.service.scripts().run(body=request, scriptId=self.script_id).execute()
            return response.get("response", {}).get("result")
        except HttpError as e:
            print(f"Error: {e.resp.status} {e.resp.reason}")
            return None