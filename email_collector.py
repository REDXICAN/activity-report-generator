import os
import pickle
import base64
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import Config

class EmailCollector:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        if os.path.exists(Config.GMAIL_TOKEN_FILE):
            with open(Config.GMAIL_TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Config.GMAIL_CREDENTIALS_FILE, Config.GMAIL_SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(Config.GMAIL_TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def get_messages(self, start_date, end_date, query=''):
        """Get messages within date range"""
        try:
            # Format dates for Gmail query
            after = start_date.strftime('%Y/%m/%d')
            before = (end_date + timedelta(days=1)).strftime('%Y/%m/%d')
            
            # Build query
            full_query = f'after:{after} before:{before}'
            if query:
                full_query += f' {query}'
            
            results = self.service.users().messages().list(
                userId='me',
                q=full_query
            ).execute()
            
            messages = results.get('messages', [])
            
            # Get full message details
            detailed_messages = []
            for msg in messages:
                msg_data = self.service.users().messages().get(
                    userId='me',
                    id=msg['id']
                ).execute()
                detailed_messages.append(self.parse_message(msg_data))
            
            return detailed_messages
            
        except Exception as e:
            print(f'An error occurred: {e}')
            return []
    
    def parse_message(self, message):
        """Parse email message"""
        payload = message['payload']
        headers = payload.get('headers', [])
        
        # Extract headers
        msg_info = {
            'id': message['id'],
            'threadId': message['threadId']
        }
        
        for header in headers:
            name = header['name']
            if name in ['From', 'To', 'Subject', 'Date']:
                msg_info[name.lower()] = header['value']
        
        # Extract body
        msg_info['body'] = self.get_message_body(payload)
        
        # Parse date
        if 'date' in msg_info:
            try:
                msg_info['datetime'] = datetime.strptime(
                    msg_info['date'][:31], '%a, %d %b %Y %H:%M:%S'
                )
            except:
                msg_info['datetime'] = None
        
        return msg_info
    
    def get_message_body(self, payload):
        """Extract message body from payload"""
        body = ''
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body += base64.urlsafe_b64decode(data).decode('utf-8')
        elif payload['body'].get('data'):
            body = base64.urlsafe_b64decode(
                payload['body']['data']).decode('utf-8')
        
        return body
    
    def get_sent_emails(self, start_date, end_date):
        """Get sent emails within date range"""
        return self.get_messages(start_date, end_date, 'in:sent')
    
    def get_received_emails(self, start_date, end_date):
        """Get received emails within date range"""
        return self.get_messages(start_date, end_date, 'in:inbox')
    
    def categorize_emails(self, emails):
        """Categorize emails by type/project"""
        categories = {
            'customer_support': [],
            'development': [],
            'meetings': [],
            'reports': [],
            'other': []
        }
        
        for email in emails:
            subject = email.get('subject', '').lower()
            body = email.get('body', '').lower()
            
            if any(word in subject + body for word in ['ticket', 'soporte', 'support', 'problema', 'issue']):
                categories['customer_support'].append(email)
            elif any(word in subject + body for word in ['code', 'github', 'deploy', 'development', 'bug', 'feature']):
                categories['development'].append(email)
            elif any(word in subject + body for word in ['meeting', 'reunion', 'call', 'zoom', 'teams']):
                categories['meetings'].append(email)
            elif any(word in subject + body for word in ['reporte', 'report', 'informe']):
                categories['reports'].append(email)
            else:
                categories['other'].append(email)
        
        return categories