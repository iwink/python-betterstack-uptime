"""Authentication handlers for the BetterStack API."""

from __future__ import annotations

from requests.auth import AuthBase
from requests.models import PreparedRequest


class BearerAuth(AuthBase):
    """Bearer token authentication for requests.

    This class implements the requests AuthBase interface to automatically
    add Bearer token authentication to all requests.

    Example:
        >>> auth = BearerAuth("your-api-token")
        >>> requests.get("https://api.example.com", auth=auth)
    """

    def __init__(self, token: str) -> None:
        """Initialize BearerAuth with a token.

        Args:
            token: The bearer token to use for authentication.
        """
        self.token = token

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        """Add Authorization header to the request.

        Args:
            r: The prepared request to modify.

        Returns:
            The modified request with Authorization header.
        """
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
