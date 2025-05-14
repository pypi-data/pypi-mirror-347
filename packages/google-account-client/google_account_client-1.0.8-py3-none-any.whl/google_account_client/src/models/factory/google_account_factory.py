from ..google_account.google_account import GoogleAccount
from ..auxiliar import Logger

from google.oauth2.credentials import Credentials

import os

class GoogleAccountFactory(Logger):
    def __init__(self, client_secrets: str, enable_logs: bool = True):
        """
        Factory to create GoogleAccount instances using a shared client secret (OAuth client).

        Args:
            client_secrets_path (str): Path to the OAuth client secrets JSON file.
            enable_logs (bool): If True, enables debug/info logging.
        """
        self.setup_logger('Factory', enable_logs)
        self.client_secrets = client_secrets

        if not os.path.exists(client_secrets):
            raise FileNotFoundError(f"Client secret file not found: {client_secrets}")

    def create_account(self, name: str, token: any = None) -> GoogleAccount:
        """
        Creates a new GoogleAccount instance with valid credentials.

        Args:
            name (str): Account identifier.
            token (str | dict | Credentials, optional): Path, dict or Credentials instance for the user token.

        Returns:
            GoogleAccount
        """

        return GoogleAccount(
            name=name,
            user_token=token,
            credentials=self.client_secrets,
            enable_logs=self.enable_logs
        )
