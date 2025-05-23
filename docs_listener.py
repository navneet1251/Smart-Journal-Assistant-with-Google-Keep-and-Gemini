from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

# Scopes
SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/tasks"  # ✅ This is missing
]

def get_doc_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('docs', 'v1', credentials=creds)
    return service

def extract_text_from_doc(doc_id):
    """
    Returns the full Google Docs API response as a dictionary.
    """
    service = get_doc_service()
    doc = service.documents().get(documentId=doc_id).execute()
    return doc  # <-- Return the full doc object (dictionary)

# For direct running/testing
if __name__ == "__main__": 
    doc_id = "GOOGLE_DOC_ID"  # Hardcoded for testing
    doc_dict = extract_text_from_doc(doc_id)
    print("\nFull Google Doc Dictionary Response:")
    print(doc_dict)
