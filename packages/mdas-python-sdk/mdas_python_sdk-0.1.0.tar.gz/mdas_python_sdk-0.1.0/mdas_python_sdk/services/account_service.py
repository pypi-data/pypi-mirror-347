from typing import Dict, Any, Union, List
from mdas_python_sdk.core.http_client import HttpClient

class AccountService:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def get_user_by_name(self, username: str) -> Dict[str, Any]:
        """Get a user by their exact username."""
        return self.http_client.get(f"/api/user/user-by-name/{username}")

    def get_user_name_by_id(self, user_id: str) -> Dict[str, Any]:
        """Get a username by user ID."""
        return self.http_client.get(f"/api/user/user-name-by-id/{user_id}")

    def get_user_id_by_name(self, username: str) -> Dict[str, Any]:
        """Get a user ID by username."""
        return self.http_client.get(f"/api/user/user-id-by-name/{username}")

    def get_user_information_by_id(self, user_id: str) -> Dict[str, Any]:
        return self.http_client.get(f"/api/user/user-information-by-id/{user_id}")

    def get_users_by_id(self, user_ids: Union[str, List[str]]) -> Dict[str, Any]:
        """Search users by exactly user IDs."""
        if isinstance(user_ids, list):
            user_ids = ",".join(user_ids)
        return self.http_client.get(f"/api/user/users-by-id?user_ids={user_ids}")

    def get_user_role(self, user_id: str) -> Dict[str, Any]:
        """Search a user role by user ID."""
        return self.http_client.get(f"/api/user/user-role?user_id={user_id}")
