import requests
from typing import List, Optional, Dict


class RequestQuizAPI:
    """
    Synchronous client for interacting with the Quiz API using `requests`.
    """

    def __init__(self, apikey: str):
        self.apikey = apikey
        self.base_url = "https://taskora.onrender.com"
        self.session = requests.Session()

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> dict:
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, timeout=60)

        if response.status_code != 200:
            try:
                error_data = response.json()
            except Exception:
                error_data = response.text
            raise Exception(f"API Error: {response.status_code} - {error_data}")

        return response.json()

    def check_status(self) -> dict:
        """Check the overall API status."""
        return self._get("/api/v1/status")

    def is_key_validate(self) -> dict:
        """Validate the current API key."""
        return self._get("/api/v1/quiz/validate_key", {"apikey": self.apikey})

    def get_author_info(self) -> dict:
        """Fetch author details and API metadata."""
        return self._get("/api/v1/author")

    def _get_quiz(self, category: str, size: int = 1) -> List[dict]:
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
        data = self._get("/api/v1/quiz", params)
        return data.get("questions", [])

    def get_collections_info(self) -> dict:
        """Fetch all quiz collections and the number of questions in each."""
        return self._get("/api/v1/quiz/collections")

    # Public quiz methods for each category
    def get_anime_quiz(self, size: int = 1) -> List[dict]:
        return self._get_quiz("Anime", size)

    def get_games_quiz(self, size: int = 1) -> List[dict]:
        return self._get_quiz("Games", size)

    def get_world_capital_quiz(self, size: int = 1) -> List[dict]:
        return self._get_quiz("WorldCapital", size)

    def get_python_quiz(self, size: int = 1) -> List[dict]:
        return self._get_quiz("Python", size)

    def get_biology_quiz(self, size: int = 1) -> List[dict]:
        return self._get_quiz("Biology", size)

    def get_cpp_quiz(self, size: int = 1) -> List[dict]:
        return self._get_quiz("Cpp", size)

    def get_c_quiz(self, size: int = 1) -> List[dict]:
        return self._get_quiz("C", size)

    def close(self):
        """Close the requests session."""
        self.session.close()
