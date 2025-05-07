class APIClient:
    """
    A reusable API client for authenticating and interacting with the CrowdStrike API.
    Handles session creation, token management, and retry logic.
    """

    def __init__(self, base_url, client_id, client_secret):
        """
        Initializes the APIClient with credentials and base URL.
        Creates a session and retrieves an OAuth2 token.

        Args:
            base_url (str): The base URL of the CrowdStrike API.
            client_id (str): The client ID for authentication.
            client_secret (str): The client secret for authentication.
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = self.__InitSession__()
        self.token = self.GetAuthToken()

    def __InitSession__(self):
        """
        Initializes an HTTP session with retry logic for transient failures.

        Returns:
            requests.Session: Configured session with retry adapters.
        """
        from requests import Session
        from requests.adapters import HTTPAdapter
        from requests.packages.urllib3.util.retry import Retry
        
        session = Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        return session

    def GetAuthToken(self):
        """
        Authenticates with the API and retrieves an OAuth2 token.

        Returns:
            str: The access token for use in subsequent API requests.

        Raises:
            RuntimeError: If authentication fails due to request error or bad credentials.
        """
        from logging import error
        from requests import RequestException

        url = f"{self.base_url}/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        try:
            response = self.session.post(url, data=data, timeout=10)
            response.raise_for_status()
            return response.json()["access_token"]
        except RequestException as e:
            error("Failed to obtain authentication token.", exc_info=True)
            raise RuntimeError("Authentication failed.") from e

    def Request(self, method, endpoint, **kwargs):
        """
        Sends an authenticated HTTP request to the API.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST', 'DELETE').
            endpoint (str): The API endpoint path to request.
            **kwargs: Optional keyword arguments passed to `requests.request()`.

        Returns:
            requests.Response: The response object from the API call.

        Raises:
            ValueError: If the provided JSON payload is not a dictionary.
            RuntimeError: If the request fails due to a connection or API error.
        """
        from logging import error
        from requests import RequestException

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"

        try:
            if "json" in kwargs and not isinstance(kwargs["json"], dict):
                raise ValueError("If provided, 'json' must be a dictionary.")

            response = self.session.request(
                method, f"{self.base_url}{endpoint}", headers=headers, timeout=10, **kwargs
            )

            response.raise_for_status()
            return response
        except RequestException as e:
            error(f"API request failed: {method} {endpoint}", exc_info=True)
            raise RuntimeError(f"API request failed: {method} {endpoint}") from e