import httpx
import aiohttp
import requests
from typing import Optional, Dict, Any


class AiohttpChatbotAPI:
    """
    A Python client for interacting with a FastAPI chatbot service.

    This client provides methods to:
    - Send chat messages to the chatbot.
    - Validate an API key for expiration and usage.
    """

    def __init__(self, apikey: str, base_url: str = "https://your-api-url.com"):
        """
        Initialize the ChatbotAPIClient.

        Args:
            base_url (str): The base URL of the FastAPI backend (e.g., "https://example.com").
        """
        self.apikey = apikey
        self.base_url: str = base_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _ensure_session(self) -> None:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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

    async def _post(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._ensure_session()
        url = f"{self.base_url}{endpoint}"

        async with self.session.post(url, params=params) as response:
            if response.status != 200:
                try:
                    error_data = await response.json()
                except Exception:
                    error_data = await response.text()
                raise Exception(f"API Error: {response.status} - {error_data}")
            return await response.json()

    async def chatbot(self, message: str) -> Dict[str, Any]:
        """
        Send a message to the chatbot and receive a response.

        Args:
            message (str): The message to send to the chatbot.

        Returns:
            Dict[str, Any]: The JSON response from the chatbot API.

        Raises:
            aiohttp.ClientResponseError: If the API responds with an error status.
        """
        params = {"apikey": self.apikey, "message": message}
        return await self._post("/api/v1/chatbot", params)

    async def validate_key(self) -> Dict[str, Any]:
        """
        Validate an API key to check expiration and usage limits.

        Returns:
            Dict[str, Any]: The JSON response with validation details.

        Raises:
            aiohttp.ClientResponseError: If the API responds with an error status.
        """
        params = {"apikey": self.apikey}
        return await self._get("/api/v1/chatbot/validate_key", params)

    async def close(self) -> None:
        """
        Gracefully close the underlying HTTP client session.
        """
        if self.session and not self.session.closed:
            await self.session.close()




class HttpxChatbotAPI:
    """
    A Python client for interacting with a FastAPI chatbot service.

    This client provides methods to:
    - Send chat messages to the chatbot.
    - Validate an API key for expiration and usage.
    """

    def __init__(self, apikey: str, base_url: str = "https://your-api-url.com"):
        """
        Initialize the ChatbotAPIClient.

        Args:
            base_url (str): The base URL of the FastAPI backend (e.g., "https://example.com").
        """
        self.apikey = apikey
        self.base_url: str = base_url.rstrip("/")
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> "HttpxChatbotAPI":
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def _ensure_client(self) -> None:
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient()

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._ensure_client()
        url = f"{self.base_url}{endpoint}"
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def _post(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._ensure_client()
        url = f"{self.base_url}{endpoint}"
        response = await self.client.post(url, params=params)
        response.raise_for_status()
        return response.json()

    async def chatbot(self, message: str) -> Dict[str, Any]:
        """
        Send a message to the chatbot and receive a response.

        Args:
            message (str): The message to send to the chatbot.

        Returns:
            Dict[str, Any]: The JSON response from the chatbot API.

        Raises:
            httpx.HTTPStatusError: If the API responds with an error status.
        """
        params = {"apikey": self.apikey, "message": message}
        return await self._post("/api/v1/chatbot", params)

    async def validate_key(self) -> Dict[str, Any]:
        """
        Validate an API key to check expiration and usage limits.

        Returns:
            Dict[str, Any]: The JSON response with validation details.

        Raises:
            httpx.HTTPStatusError: If the API responds with an error status.
        """
        params = {"apikey": self.apikey}
        return await self._get("/api/v1/chatbot/validate_key", params)

    async def close(self) -> None:
        """
        Gracefully close the underlying HTTP client session.
        """
        if self.client and not self.client.is_closed:
            await self.client.aclose()






class RequestsChatbotAPI:
    """
    A Python client for interacting with a FastAPI chatbot service.

    This client provides methods to:
    - Send chat messages to the chatbot.
    - Validate an API key for expiration and usage.
    """

    def __init__(self, apikey: str, base_url: str = "https://your-api-url.com"):
        """
        Initialize the ChatbotAPIClient.

        Args:
            apikey (str): The API key for authenticating with the chatbot service.
            base_url (str): The base URL of the FastAPI backend (e.g., "https://example.com").
        """
        self.apikey = apikey
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def chatbot(self, message: str) -> Dict[str, Any]:
        """
        Send a message to the chatbot and receive a response.

        Args:
            message (str): The message to send to the chatbot.

        Returns:
            Dict[str, Any]: The JSON response from the chatbot API.

        Raises:
            requests.HTTPError: If the API responds with an error status.
        """
        url = f"{self.base_url}/api/v1/chatbot"
        params = {"apikey": self.apikey, "message": message}
        response = self.session.post(url, params=params)
        response.raise_for_status()
        return response.json()

    def validate_key(self) -> Dict[str, Any]:
        """
        Validate an API key to check expiration and usage limits.

        Returns:
            Dict[str, Any]: The JSON response with validation details.

        Raises:
            requests.HTTPError: If the API responds with an error status.
        """
        url = f"{self.base_url}/api/v1/chatbot/validate_key"
        params = {"apikey": self.apikey}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """
        Gracefully close the underlying HTTP session.
        """
        self.session.close()
