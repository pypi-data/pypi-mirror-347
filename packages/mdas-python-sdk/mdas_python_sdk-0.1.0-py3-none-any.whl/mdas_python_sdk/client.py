# mdas-python-sdk/client.py
from mdas_python_sdk.auth import AuthManager
from mdas_python_sdk.services.quote_service import QuoteService
from mdas_python_sdk.core.http_client import HttpClient
from mdas_python_sdk.services.account_service import AccountService


class MdasClient:
    def __init__(self, base_url: str, username: str, password: str):

        self.auth_manager = AuthManager(base_url, username, password)
        self.http_client = HttpClient(base_url, self.auth_manager)

        # Services
        self.quote = QuoteService(self.http_client)
        self.account = AccountService(self.http_client)

    def refresh_token(self):
        """Refresh the authentication token"""
        token = self.auth_manager.authenticate()
        self.http_client.set_token(token)
