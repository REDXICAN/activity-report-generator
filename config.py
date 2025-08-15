import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Gmail settings
    GMAIL_CREDENTIALS_FILE = os.getenv('GMAIL_CREDENTIALS_FILE', 'credentials.json')
    GMAIL_TOKEN_FILE = os.getenv('GMAIL_TOKEN_FILE', 'token.json')
    GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    # GitHub settings
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
    
    # WhatsApp settings
    WHATSAPP_DATA_PATH = os.getenv('WHATSAPP_DATA_PATH')
    
    # Report settings
    REPORT_TEMPLATE_PATH = os.getenv('REPORT_TEMPLATE_PATH', 
        r'O:\OneDrive\Documentos\-- TurboAir\-- Reportes de Actividad\Formato reporte de Actividades.xlsx')
    REPORT_OUTPUT_PATH = os.getenv('REPORT_OUTPUT_PATH',
        r'O:\OneDrive\Documentos\-- TurboAir\-- Reportes de Actividad')
    
    # Email accounts
    EMAIL_ACCOUNTS = os.getenv('EMAIL_ACCOUNTS', '').split(',')
    
    @staticmethod
    def get_report_period(start_date=None, end_date=None):
        """Get report period dates"""
        if not end_date:
            end_date = datetime.now()
        if not start_date:
            # Default to 15-day period
            if end_date.day <= 15:
                start_date = end_date.replace(day=1)
            else:
                start_date = end_date.replace(day=16)
        return start_date, end_date