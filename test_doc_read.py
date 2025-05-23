from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Scopes
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_doc_service():
    creds = None
    if os.path.exists('token.json'):
        from google.oauth2.credentials import Credentials
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

if __name__ == "__main__":
    doc_id = "11NjQ6cJG7D-pQVwi76f6d0gxXo87Yw3zK7oBXIFZGUQ"  # Directly hardcoded
    service = get_doc_service()
    try:
        doc = service.documents().get(documentId=doc_id).execute()
        print(doc)
    except Exception as e:
        print("ERROR OCCURRED", e)

def extract_text_from_doc(doc):
    text = ''
    for element in doc.get('body', {}).get('content', []):
        paragraph = element.get('paragraph')
        if paragraph:
            for elem in paragraph.get('elements', []):
                text_run = elem.get('textRun')
                if text_run:
                    text += text_run.get('content', '')
    return text.strip()
text = extract_text_from_doc(doc)
print("\nExtracted Text from Google Doc:")
print(text)