# sendrella/endpoints/utils.py

from typing import Dict, Any


class UtilityAPI:
    """
    Miscellaneous utility API methods: credits, token validation.
    """

    def __init__(self, http_client):
        self.http = http_client

    def credits(self) -> Dict[str, Any]:
        """
        Fetch current credit balance and usage details.
        Sends api_key in body.
        """
        api_key = self._get_api_key_from_headers()
        data = {"api_key": api_key}
        return self.http.post("/utils/credits", data)

    def validate_key(self) -> Dict[str, Any]:
        """
        Validate the provided API key and fetch account display name.
        Sends api_key in body.
        """
        api_key = self._get_api_key_from_headers()
        data = {"api_key": api_key}
        return self.http.post("/token/validate", data)

    def _get_api_key_from_headers(self) -> str:
        """
        Extracts the Bearer token from the HTTP Authorization header.
        """
        auth_header = self.http.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer "):
            return auth_header[7:].strip()
        return ""
