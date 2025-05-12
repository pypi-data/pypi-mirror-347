import aiohttp
import httpx
import requests
from typing import Optional, Dict, Any

class AiohttpreChaptchaAPI:
    """
    Asynchronous client using aiohttp for interacting with the Quiz API.
    """

    def __init__(self, apikey: str):
        """
        Initialize the API client.
        
        :param apikey: Your API key for accessing the service.
        """
        self.apikey = apikey
        self.base_url = "https://taskora.onrender.com"
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the session."""
        if self.session:
            await self.session.close()

    async def _ensure_session(self):
        """Ensure the aiohttp session is initialized and open."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a GET request to the given endpoint.

        :param endpoint: API route path (e.g., /api/v1/...).
        :param params: Query parameters to include in the request.
        :return: JSON response as a dictionary.
        """
        await self._ensure_session()
        url = f"{self.base_url}{endpoint}"

        async with self.session.get(url, params=params) as response:
            if response.status != 200:
                try:
                    error_data = await response.json()
                except Exception:
                    error_data = await response.text()
                raise Exception(f"API Error: {response.status} - {error_data}")
            return await response.json()

    async def rechaptcha_v3_solver(self, anchorUrl: str) -> Dict[str, Any]:
        """
        Solve a reCAPTCHA v3 challenge.

        :param anchorUrl: The anchor URL from the reCAPTCHA widget.
        :return: Solved token and related data from API.
        """
        params = {
            "apikey": self.apikey,
            "anchor_url": anchorUrl
        }
        return await self._get("/api/v1/recaptcha-solver/v3", params=params)

    async def rechaptcha_key_status(self) -> Dict[str, Any]:
        """
        Check the validity and status of the API key.

        :return: API key validation status.
        """
        params = {"apikey": self.apikey}
        return await self._get("/api/v1/recaptcha-solver/validate_key", params=params)








class HttpxreChaptchaAPI:
    """
    Asynchronous client using httpx for interacting with the Quiz API.
    """

    def __init__(self, apikey: str):
        """
        Initialize the API client.
        :param apikey: Your API key for accessing the service.
        """
        self.apikey = apikey
        self.base_url = "https://taskora.onrender.com"
        self.client = httpx.AsyncClient()

    async def close(self):
        """Close the HTTPX client session."""
        await self.client.aclose()

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a GET request to the given endpoint.

        :param endpoint: API route path.
        :param params: Optional query parameters.
        :return: JSON response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise Exception(f"API Error: {e.response.status_code} - {e.response.text}")

    async def rechaptcha_v3_solver(self, anchorUrl: str) -> Dict[str, Any]:
        """
        Solve a reCAPTCHA v3 challenge.

        :param anchorUrl: Anchor URL of the reCAPTCHA.
        :return: Dictionary with the solver result.
        """
        params = {
            "apikey": self.apikey,
            "anchor_url": anchorUrl
        }
        return await self._get("/api/v1/recaptcha-solver/v3", params=params)

    async def rechaptcha_key_status(self) -> Dict[str, Any]:
        """
        Check API key status and expiration.

        :return: Dictionary with API key status.
        """
        return await self._get("/api/v1/recaptcha-solver/validate_key", params={"apikey": self.apikey})





import requests
from typing import Optional, Dict, Any


class RequestsreChaptchaAPI:
    """
    Synchronous client using requests for interacting with the Quiz API.
    """

    def __init__(self, apikey: str):
        """
        Initialize the API client.

        :param apikey: Your API key for accessing the service.
        """
        self.apikey = apikey
        self.base_url = "https://taskora.onrender.com"

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a synchronous GET request.

        :param endpoint: API path.
        :param params: Query parameters.
        :return: JSON response as dictionary.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"API Error: {response.status_code if response else 'N/A'} - {str(e)}")

    def rechaptcha_v3_solver(self, anchorUrl: str) -> Dict[str, Any]:
        """
        Solve a reCAPTCHA v3 challenge synchronously.

        :param anchorUrl: Anchor URL to solve.
        :return: Solver result from the API.
        """
        params = {
            "apikey": self.apikey,
            "anchor_url": anchorUrl
        }
        return self._get("/api/v1/recaptcha-solver/v3", params=params)

    def rechaptcha_key_status(self) -> Dict[str, Any]:
        """
        Check API key status synchronously.

        :return: Status response.
        """
        return self._get("/api/v1/recaptcha-solver/validate_key", params={"apikey": self.apikey})
