import aiohttp
from typing import Dict, Any


class AiohttpInstagramAPI:
    """
    A client wrapper for the FastAPI-based Instagram API hosted at taskora.onrender.com using aiohttp.
    """

    def __init__(self, apikey: str, timeout: int = 60):
        """
        Initialize the API wrapper.

        Args:
            apikey (str): Your API key for authenticating with the backend.
            timeout (int): Request timeout in seconds (default: 60).
        """
        self.apikey = apikey
        self.timeout = timeout
        self.base_url = "https://taskora.onrender.com/api/v1/"

    async def _get(self, endpoint: str, url_param: str) -> Dict[str, Any]:
        """
        Internal helper for making GET requests.

        Args:
            endpoint (str): API endpoint path (e.g., 'get', 'hls').
            url_param (str): Instagram URL to pass as a query parameter.

        Returns:
            Dict[str, Any]: JSON response from the API.
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                self.base_url + endpoint,
                params={"apikey": self.apikey, "url": url_param}
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def _post(self, endpoint: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal helper for making POST requests with query parameters.

        Args:
            endpoint (str): API endpoint path.
            query_params (Dict[str, Any]): Dictionary of query parameters.

        Returns:
            Dict[str, Any]: JSON response from the API.
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        params = {"apikey": self.apikey, **query_params}
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.base_url + endpoint,
                params=params
            ) as response:
                response.raise_for_status()
                return await response.json()

    # ----------- GET Endpoints ------------

    async def get_post(self, url: str) -> Dict[str, Any]:
        """
        Fetch a public Instagram post using the /get endpoint.

        Args:
            url (str): URL of the Instagram post.

        Returns:
            Dict[str, Any]: JSON data of the post, including media and metadata.
        """
        return await self._get("get", url)

    async def get_post_alt(self, url: str) -> Dict[str, Any]:
        """
        Alternate way to fetch a public Instagram post using the /GET endpoint.

        Args:
            url (str): URL of the Instagram post.

        Returns:
            Dict[str, Any]: JSON data of the post.
        """
        return await self._get("GET", url)

    async def get_hls_stream(self, url: str) -> Dict[str, Any]:
        """
        Retrieve metadata for an HLS video stream.

        Args:
            url (str): URL of the HLS media.

        Returns:
            Dict[str, Any]: Information about the stream and playback options.
        """
        return await self._get("hls", url)

    # ----------- POST Endpoints (via Query Params) ------------

    async def get_links(self, url: str) -> Dict[str, Any]:
        """
        Extract download links from an Instagram post or reel.

        Args:
            url (str): Instagram media URL.

        Returns:
            Dict[str, Any]: Media download links and type info.
        """
        return await self._post("links", {"url": url})

    async def get_profile(self, username: str) -> Dict[str, Any]:
        """
        Fetch profile information for an Instagram user.

        Args:
            username (str): Instagram username.

        Returns:
            Dict[str, Any]: Profile metadata (bio, followers, etc.).
        """
        return await self._post("profile", {"username": username})

    async def get_stories(self, username: str) -> Dict[str, Any]:
        """
        Retrieve active stories from a user's profile.

        Args:
            username (str): Instagram username.

        Returns:
            Dict[str, Any]: List of current story media and metadata.
        """
        return await self._post("stories", {"username": username})

    async def get_story(self, story_id: str) -> Dict[str, Any]:
        """
        Retrieve a single story by its ID.

        Args:
            story_id (str): Unique ID of the Instagram story.

        Returns:
            Dict[str, Any]: Details of the story including media.
        """
        return await self._post("story", {"story_id": story_id})

    async def get_highlights(self, username: str) -> Dict[str, Any]:
        """
        Fetch highlight reel metadata for a user.

        Args:
            username (str): Instagram username.

        Returns:
            Dict[str, Any]: Highlight titles, IDs, and thumbnails.
        """
        return await self._post("highlights", {"username": username})

    async def get_highlight_stories(self, highlight_id: str) -> Dict[str, Any]:
        """
        Retrieve all stories within a given highlight reel.

        Args:
            highlight_id (str): ID of the highlight.

        Returns:
            Dict[str, Any]: Story media in the specified highlight.
        """
        return await self._post("highlight_stories", {"highlight_id": highlight_id})

    async def get_user_info(self, username: str) -> Dict[str, Any]:
        """
        Retrieve basic user profile information.

        Args:
            username (str): Instagram username.

        Returns:
            Dict[str, Any]: Profile image, bio, verification status, etc.
        """
        return await self._post("userInfo", {"username": username})

    async def get_reels(self, username: str) -> Dict[str, Any]:
        """
        Fetch all public reels posted by a user.

        Args:
            username (str): Instagram username.

        Returns:
            Dict[str, Any]: List of reel media and metadata.
        """
        return await self._post("reels", {"username": username})

    async def get_posts(self, username: str) -> Dict[str, Any]:
        """
        Retrieve recent posts for a user profile.

        Args:
            username (str): Instagram username.

        Returns:
            Dict[str, Any]: List of posts with media links and captions.
        """
        return await self._post("posts", {"username": username})

    # ----------- API Key Validation (Optional) ------------

    async def validate_key(self) -> Dict[str, Any]:
        """
        Validate the provided API key and get usage metadata.

        Returns:
            Dict[str, Any]: API key status, rate limits, and expiry.
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                self.base_url + "instagram/validate_key",
                params={"apikey": self.apikey}
            ) as response:
                response.raise_for_status()
                return await response.json()
