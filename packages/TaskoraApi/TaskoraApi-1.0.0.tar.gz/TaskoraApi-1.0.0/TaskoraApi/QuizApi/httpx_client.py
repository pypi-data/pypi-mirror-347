import httpx
from typing import List, Optional, Dict


class HttpxQuizAPI:
    """
    Asynchronous client for interacting with the Quiz API using httpx.
    """

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.base_url = "https://taskora.onrender.com"
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self.client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _ensure_client(self):
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient()

    async def _get(self, endpoint: str, params: Optional[Dict] = None) -> dict:
        await self._ensure_client()
        url = f"{self.base_url}{endpoint}"

        response = await self.client.get(url, params=params)
        if response.status_code != 200:
            try:
                error_data = response.json()
            except Exception:
                error_data = response.text
            raise Exception(f"API Error: {response.status_code} - {error_data}")

        return response.json()


    async def get_collections_info(self) -> dict:
        """Fetch all quiz collections and the number of questions in each."""
        return await self._get("/api/v1/quiz/collections")

    async def check_status(self) -> dict:
        """Check the overall API status."""
        return await self._get("/api/v1/status")

    async def is_key_validate(self) -> dict:
        """Validate the current API key."""
        return await self._get("/api/v1/quiz/validate_key", {"apikey": self.apikey})

    async def get_author_info(self) -> dict:
        """Fetch author details and API metadata."""
        return await self._get("/api/v1/author")

    async def _get_quiz(self, category: str, size: int = 1) -> List[dict]:
        """
        Retrieve quiz questions for a specific category.

        Args:
            category (str): The quiz category name (e.g., 'Python').
            size (int): Number of questions to retrieve (1 to 15).

        Returns:
            List[dict]: A list of quiz questions.
        """
        if not 1 <= size <= 15:
            raise ValueError("Quiz size must be between 1 and 15.")

        params = {
            "apikey": self.apikey,
            "QuizType": category,
            "size": size
        }
        data = await self._get("/api/v1/quiz", params)
        return data.get("questions", [])

    # Public quiz methods for each category
    async def get_anime_quiz(self, size: int = 1) -> List[dict]:
        return await self._get_quiz("Anime", size)

    async def get_games_quiz(self, size: int = 1) -> List[dict]:
        return await self._get_quiz("Games", size)

    async def get_world_capital_quiz(self, size: int = 1) -> List[dict]:
        return await self._get_quiz("WorldCapital", size)

    async def get_python_quiz(self, size: int = 1) -> List[dict]:
        return await self._get_quiz("Python", size)

    async def get_biology_quiz(self, size: int = 1) -> List[dict]:
        return await self._get_quiz("Biology", size)

    async def get_cpp_quiz(self, size: int = 1) -> List[dict]:
        return await self._get_quiz("Cpp", size)

    async def get_c_quiz(self, size: int = 1) -> List[dict]:
        return await self._get_quiz("C", size)

    async def close(self):
        """Close the httpx AsyncClient session."""
        if self.client and not self.client.is_closed:
            await self.client.aclose()
