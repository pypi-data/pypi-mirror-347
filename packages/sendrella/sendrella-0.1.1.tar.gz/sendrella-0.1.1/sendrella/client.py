# sendrella/client.py

from .config import SendrellaConfig
from .http import HTTPClient
from .endpoints import bounce, temp_mail, utils


class SendrellaClient:
    """
    Main client to interact with the Sendrella API.
    """
    def __init__(self, api_key: str, timeout: int = 20, base_url: str = None):
        self.config = SendrellaConfig(
            api_key=api_key,
            base_url=base_url or "https://sendrella.com/dashboard/api/v1",
            timeout=timeout
        )
        self.http = HTTPClient(
            base_url=self.config.base_url,
            headers=self.config.get_headers(),
            timeout=self.config.timeout
        )

        # Endpoint namespaces
        self.bounce = bounce.BounceAPI(self.http)
        self.temp_mail = temp_mail.TempMailAPI(self.http)
        self.utils = utils.UtilityAPI(self.http)
