import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class AppScript:
    def __init__(self, credentials):
        self.credentials = credentials
        self.service = self._get_service()

    def _get_service(self):
        return build('script', 'v1', credentials=self.credentials)

    def loggers(self, message):
        logging.info(message)

    def google_chat_insert(self, message):
        try:
            request = {
                'requests': [
                    {
                        'insertText': {
                            'location': {
                                'index': 0
                            },
                            'text': message
                        }
                    }
                ]
            }
            response = self.service.documents().batchUpdate(
                documentId='your_document_id', body=request).execute()
            logging.info(f'Response: {response}')
        except HttpError as error:
            logging.error(f'Error: {error}')