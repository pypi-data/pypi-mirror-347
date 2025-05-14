# sendrella/endpoints/bounce.py

from typing import Optional, List, Dict, Any


class BounceAPI:
    """
    Bounce-related API methods.
    """

    def __init__(self, http_client):
        self.http = http_client

    def check(self, email: str) -> Dict[str, Any]:
        """
        Check if an email is valid, risky, or undeliverable.
        """
        data = {"email": email}
        return self.http.post("/bounce/check", data)

    def logs(
        self,
        page: int = 1,
        per_page: int = 10,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve bounce logs with optional filtering.
        """
        data = {
            "page": page,
            "per_page": per_page
        }
        if status:
            data["status"] = status
        if search:
            data["search"] = search

        return self.http.post("/bounce/logs", data)
