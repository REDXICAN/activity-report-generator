import os
import json
import pickle
import webbrowser
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from github import Github
import threading
import time

class OAuthManager:
    def __init__(self):
        self.gmail_service = None
        self.github_client = None
        self.credentials_cache = {}
        
    def setup_gmail_oauth(self, credentials_file=None):
        """Setup Gmail OAuth with automatic authentication"""
        if not credentials_file:
            credentials_file = 'credentials.json'
        
        if not os.path.exists(credentials_file):
            raise FileNotFoundError(f"Gmail credentials file not found: {credentials_file}")
        
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        token_file = 'token.json'
        
        # Load existing token
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                # Use a different port and handle authentication
                creds = flow.run_local_server(port=8080, open_browser=True)
            
            # Save credentials
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.gmail_service = build('gmail', 'v1', credentials=creds)
        self.credentials_cache['gmail'] = creds
        return True
    
    def setup_github_oauth(self, token=None):
        """Setup GitHub OAuth/token authentication"""
        if not token:
            # Try to load from environment or prompt
            token = os.getenv('GITHUB_TOKEN')
            if not token:
                raise ValueError("GitHub token not provided. Please set GITHUB_TOKEN environment variable or provide token parameter.")
        
        try:
            self.github_client = Github(token)
            # Test the connection
            user = self.github_client.get_user()
            print(f"Connected to GitHub as: {user.login}")
            self.credentials_cache['github'] = token
            return True
        except Exception as e:
            print(f"GitHub authentication failed: {e}")
            return False
    
    def auto_discover_accounts(self):
        """Automatically discover and connect to available accounts"""
        discovered_accounts = {
            'gmail_accounts': [],
            'github_accounts': [],
            'status': {}
        }
        
        # Gmail discovery
        if self.gmail_service:
            try:
                profile = self.gmail_service.users().getProfile(userId='me').execute()
                discovered_accounts['gmail_accounts'].append({
                    'email': profile.get('emailAddress'),
                    'messages_total': profile.get('messagesTotal', 0),
                    'threads_total': profile.get('threadsTotal', 0)
                })
                discovered_accounts['status']['gmail'] = 'connected'
            except Exception as e:
                discovered_accounts['status']['gmail'] = f'error: {str(e)}'
        
        # GitHub discovery
        if self.github_client:
            try:
                user = self.github_client.get_user()
                discovered_accounts['github_accounts'].append({
                    'username': user.login,
                    'name': user.name,
                    'public_repos': user.public_repos,
                    'followers': user.followers,
                    'following': user.following
                })
                discovered_accounts['status']['github'] = 'connected'
            except Exception as e:
                discovered_accounts['status']['github'] = f'error: {str(e)}'
        
        return discovered_accounts
    
    def get_oauth_urls(self):
        """Get OAuth URLs for manual authentication if needed"""
        urls = {}
        
        # Gmail OAuth URL
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                ['https://www.googleapis.com/auth/gmail.readonly']
            )
            auth_url, _ = flow.authorization_url(prompt='consent')
            urls['gmail'] = auth_url
        except:
            urls['gmail'] = None
        
        # GitHub OAuth URL (for reference)
        urls['github'] = "https://github.com/settings/tokens/new?scopes=repo,read:user"
        
        return urls
    
    def test_connections(self):
        """Test all OAuth connections"""
        results = {}
        
        # Test Gmail
        if self.gmail_service:
            try:
                profile = self.gmail_service.users().getProfile(userId='me').execute()
                results['gmail'] = {
                    'status': 'success',
                    'email': profile.get('emailAddress'),
                    'message': 'Gmail connection successful'
                }
            except Exception as e:
                results['gmail'] = {
                    'status': 'error',
                    'message': str(e)
                }
        else:
            results['gmail'] = {
                'status': 'not_connected',
                'message': 'Gmail not connected'
            }
        
        # Test GitHub
        if self.github_client:
            try:
                user = self.github_client.get_user()
                results['github'] = {
                    'status': 'success',
                    'username': user.login,
                    'message': 'GitHub connection successful'
                }
            except Exception as e:
                results['github'] = {
                    'status': 'error',
                    'message': str(e)
                }
        else:
            results['github'] = {
                'status': 'not_connected',
                'message': 'GitHub not connected'
            }
        
        return results
    
    def refresh_all_tokens(self):
        """Refresh all OAuth tokens"""
        refreshed = {}
        
        # Refresh Gmail token
        if 'gmail' in self.credentials_cache:
            try:
                creds = self.credentials_cache['gmail']
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open('token.json', 'wb') as token:
                        pickle.dump(creds, token)
                    refreshed['gmail'] = 'success'
                else:
                    refreshed['gmail'] = 'not_needed'
            except Exception as e:
                refreshed['gmail'] = f'error: {str(e)}'
        
        # GitHub tokens don't expire but we can test them
        if 'github' in self.credentials_cache:
            try:
                user = self.github_client.get_user()
                refreshed['github'] = 'valid'
            except Exception as e:
                refreshed['github'] = f'error: {str(e)}'
        
        return refreshed
    
    def get_connection_status(self):
        """Get detailed connection status for all services"""
        status = {
            'gmail': {
                'connected': self.gmail_service is not None,
                'authenticated': False,
                'email': None,
                'last_check': datetime.now().isoformat()
            },
            'github': {
                'connected': self.github_client is not None,
                'authenticated': False,
                'username': None,
                'last_check': datetime.now().isoformat()
            }
        }
        
        # Check Gmail status
        if self.gmail_service:
            try:
                profile = self.gmail_service.users().getProfile(userId='me').execute()
                status['gmail']['authenticated'] = True
                status['gmail']['email'] = profile.get('emailAddress')
            except:
                status['gmail']['authenticated'] = False
        
        # Check GitHub status
        if self.github_client:
            try:
                user = self.github_client.get_user()
                status['github']['authenticated'] = True
                status['github']['username'] = user.login
            except:
                status['github']['authenticated'] = False
        
        return status
    
    def setup_automated_authentication(self, config):
        """Setup automated authentication with provided configuration"""
        results = {}
        
        # Setup Gmail if credentials provided
        if config.get('gmail_credentials_file'):
            try:
                success = self.setup_gmail_oauth(config['gmail_credentials_file'])
                results['gmail'] = 'success' if success else 'failed'
            except Exception as e:
                results['gmail'] = f'error: {str(e)}'
        
        # Setup GitHub if token provided
        if config.get('github_token'):
            try:
                success = self.setup_github_oauth(config['github_token'])
                results['github'] = 'success' if success else 'failed'
            except Exception as e:
                results['github'] = f'error: {str(e)}'
        
        return results
    
    def get_authenticated_services(self):
        """Get dictionary of authenticated services for use by collectors"""
        services = {}
        
        if self.gmail_service:
            services['gmail'] = self.gmail_service
        
        if self.github_client:
            services['github'] = self.github_client
        
        return services
    
    def save_oauth_config(self, config):
        """Save OAuth configuration securely"""
        secure_config = {
            'gmail_credentials_file': config.get('gmail_credentials_file'),
            'github_username': config.get('github_username'),
            'last_updated': datetime.now().isoformat(),
            'auto_refresh': config.get('auto_refresh', True)
        }
        
        # Don't save sensitive tokens to file
        with open('oauth_config.json', 'w') as f:
            json.dump(secure_config, f, indent=2)
        
        return secure_config
    
    def load_oauth_config(self):
        """Load OAuth configuration"""
        try:
            with open('oauth_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def revoke_all_tokens(self):
        """Revoke all OAuth tokens (logout)"""
        revoked = {}
        
        # Revoke Gmail tokens
        if 'gmail' in self.credentials_cache:
            try:
                creds = self.credentials_cache['gmail']
                if hasattr(creds, 'revoke'):
                    creds.revoke(Request())
                
                # Remove token file
                if os.path.exists('token.json'):
                    os.remove('token.json')
                
                self.gmail_service = None
                revoked['gmail'] = 'success'
            except Exception as e:
                revoked['gmail'] = f'error: {str(e)}'
        
        # Clear GitHub client (tokens can't be revoked programmatically)
        if self.github_client:
            self.github_client = None
            revoked['github'] = 'cleared'
        
        # Clear cache
        self.credentials_cache.clear()
        
        return revoked