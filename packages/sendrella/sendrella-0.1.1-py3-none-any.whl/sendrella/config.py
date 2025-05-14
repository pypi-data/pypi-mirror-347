# sendrella/config.py

class SendrellaConfig:
    """
    Central configuration class for Sendrella API settings.
    """
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://sendrella.com/dashboard/api/v1",
        timeout: int = 20,
        user_agent: str = "Sendrella-Python-SDK/1.0"
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": self.user_agent
        }
