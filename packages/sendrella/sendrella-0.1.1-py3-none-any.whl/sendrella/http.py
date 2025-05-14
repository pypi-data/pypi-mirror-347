# sendrella/http.py

import requests
from typing import Optional, Dict, Any
from requests.exceptions import RequestException, Timeout, ConnectionError as ReqConnectionError

from .exceptions import (
    AuthenticationError,
    BadRequestError,
    ServerError,
    TimeoutError,
    NotFoundError,
    APIConnectionError
)


class HTTPClient:
    """
    Lightweight wrapper around requests for API interactions.
    """
    def __init__(self, base_url: str, headers: dict, timeout: int = 20):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Make a POST request to the given endpoint with optional headers/data.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        final_headers = headers or self.headers
        try:
            response = requests.post(
                url,
                json=data or {},
                headers=final_headers,
                timeout=timeout or self.timeout
            )
            if response.status_code == 400:
                raise BadRequestError(response.text)
            elif response.status_code == 401:
                raise AuthenticationError("Unauthorized or invalid API key")
            elif response.status_code == 403:
                raise AuthenticationError("Access forbidden. Check your permissions.")
            elif response.status_code == 404:
                raise NotFoundError("Endpoint not found")
            elif 500 <= response.status_code < 600:
                raise ServerError("Internal server error")

            return response.json()

        except Timeout:
            raise TimeoutError("Request timed out")
        except ReqConnectionError:
            raise APIConnectionError("Failed to connect to the API server")
        except RequestException as e:
            raise ServerError(f"Unhandled request error: {e}")
        except ValueError:
            raise ServerError("Failed to parse JSON from response")
