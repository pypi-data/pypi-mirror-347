import requests
from typing import Dict, Any, Optional
from ..helpers.logger import logger
from mdas_python_sdk.auth import AuthManager

class HttpClient:
    def __init__(self, base_url: str, auth_manager: AuthManager):
        self.base_url = base_url
        self.auth_manager = auth_manager
        self.token = self.auth_manager.get_token()
    
    def set_token(self, token: str):
        """Set the authentication token"""
        self.token = token
    
    def _get_headers(self, additional_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Get headers with authentication token.
        """
        headers = {
            "accept": "application/json;odata.metadata=minimal;odata.streaming=true"
        }
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
            
        if additional_headers:
            headers.update(additional_headers)
            
        return headers
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Send a GET request to the API.
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(headers)
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:  # Unauthorized, possibly due to expired token
                logger.info("Token expired, re-authenticating...")
                self.token = self.auth_manager.authenticate()  # Re-authenticate
                return self.get(endpoint, params, headers)  # Retry the request
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            # Handle other exceptions
            logger.error(f"An unexpected error occurred: {e}")
            raise
    
    def post(self, endpoint: str, data: Dict[str, Any] = None,
             headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Send a POST request to the API.
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(headers)
        
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:  # Unauthorized, possibly due to expired token
                logger.info("Token expired, re-authenticating...")
                self.token = self.auth_manager.authenticate()  # Re-authenticate
                return self.post(endpoint, data, headers)  # Retry the request
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise 