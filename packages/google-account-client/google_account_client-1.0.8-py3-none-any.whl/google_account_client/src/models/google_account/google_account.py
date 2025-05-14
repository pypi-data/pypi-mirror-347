"""
google_account.py

Defines the GoogleAccount class, a high-level interface that consolidates Google Calendar
functionality and Google API authentication/authorization handling. It inherits behavior
from service and calendar mixins, and provides scoped, logged access to Google APIs
with user-specific credentials.
"""

from .google_service import GoogleServiceCredentials
from .google_calendar import GoogleCalendar
from ...settings import Config

# Google Cloud lib
from google.oauth2.service_account import Credentials

class GoogleAccount(GoogleServiceCredentials, GoogleCalendar):
    """
    GoogleAccount is the main interface for managing a user's Google Calendar and 
    authentication credentials.

    Inherits from:
        - GoogleServiceCredentials: Handles credential loading and refreshing.
        - GoogleCalendar: Provides calendar-related methods (listing, creating events, etc.).
    """
    def __init__(self, name: str, user_token: any = None, credentials: Credentials = None, enable_logs: bool = False):
        """
        Initializes a new GoogleAccount instance.

        Args:
            name (str): User or account identifier.
            user_token (any): Existing credentials object (optional).
            credentials (any): Raw credential information or dict (optional).
            enable_logs (bool): If True, enables debug/info logging.
        """
        # Personal Info
        self.name = name

        # Config
        self.SCOPES = Config.SCOPES
        self.setup_logger(self.name, enable_logs)

        # Google-Service-Credentials
        self._user_token = self._load_token(user_token, credentials)
        self._service = self._load_service(self._user_token)

    def get_user_token(self) -> any:
        """
        Returns the current credentials token for the account.

        Returns:
            Any: The stored OAuth credentials.
        """
        return self._user_token
    
    def __repr__(self):
        return f"<GoogleAccount name='{self.name}'>"