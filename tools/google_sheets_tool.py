import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def update_google_sheet(spreadsheet_id, range_name, values):
    """
    Updates a Google Sheet with the provided values.
    Requires a 'credentials.json' file in the root directory.
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    creds_path = 'credentials.json'
    
    if not os.path.exists(creds_path):
        return "Error: credentials.json not found. Please provide Google Cloud service account credentials."

    try:
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        body = {
            'values': values
        }
        
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        return f"{result.get('updates').get('updatedCells')} cells updated."

    except Exception as e:
        return f"Error updating Google Sheet: {str(e)}"
