import requests
from typing import Dict, Optional


class AuthManager:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = self.authenticate()
        self.expiration = None

    def authenticate(self) -> str:
        """
        Authenticate with the API and get an access token.
        """
        url = f"{self.base_url}/api/user/login"
        payload = {
            "user_name": self.username,
            "password": self.password
        }
        headers = {
            "Content-Type": "application/json",
            "accept": "*/*"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        self.token = data.get("token")
        #self.expiration = data.get("expiration")
        
        return self.token
    
    def get_token(self) -> Optional[str]:
        """
        Get the current token.
        """
        return self.token
