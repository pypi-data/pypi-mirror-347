# sendrella/endpoints/temp_mail.py

from typing import Optional, Dict, Any


class TempMailAPI:
    """
    Temporary/disposable email-related API methods.
    """

    def __init__(self, http_client):
        self.http = http_client

    def check(self, email: str) -> Dict[str, Any]:
        """
        Check if an email is disposable.
        """
        data = {"email": email}
        return self.http.post("/tempmail/check", data)

    def logs(
        self,
        page: int = 1,
        per_page: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve logs of past disposable email checks.
        """
        data = {
            "page": page,
            "per_page": per_page
        }
        if status:
            data["status"] = status
        if search:
            data["search"] = search

        return self.http.post("/tempmail/logs", data)
