from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/calendar.events']

def auth_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        print("Opening browser for Google login... (check your browser window)")
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_emails(service):
    try:
        emails = []
        next_page_token = None

        while True:
            results = service.users().messages().list(
                userId='me',
                q='newer_than:1d',  # last 24 hours
                pageToken=next_page_token
            ).execute()

            messages = results.get('messages', [])
            for msg in messages:
                msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
                subject = next((h['value'] for h in msg_data['payload']['headers'] if h['name'] == 'Subject'), "")
                snippet = msg_data.get('snippet', "")
                emails.append({'subject': subject, 'snippet': snippet})

            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break

        return emails

    except HttpError as error:
        print(f'An error occurred: {error}')
        return []

def main():
    creds = auth_google()
    print("Google Authenticated")

if __name__ == '__main__':
    main()