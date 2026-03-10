"""REST API client classes for the BetterStack Uptime API."""

from __future__ import annotations

from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import BearerAuth
from .exceptions import (
    APIError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)


class RESTAPI:
    """Low-level REST API client with session management and retry logic.

    This class handles all HTTP communication with the BetterStack API,
    including authentication, request retries, and error handling.

    Attributes:
        base_url: The base URL for all API requests.
        session: The requests session used for all HTTP calls.
    """

    def __init__(
        self,
        base_url: str,
        auth: BearerAuth,
        retries: int = 3,
        backoff_factor: float = 0.5,
        timeout: float = 30.0,
    ) -> None:
        """Initialize RESTAPI with session and retry configuration.

        Args:
            base_url: The URL to be called, must end with a forward slash.
            auth: Authentication class to be used with requests.
            retries: Number of retries for failed requests.
            backoff_factor: Backoff factor for retry delays.
            timeout: Default timeout for requests in seconds.

        Raises:
            ValueError: If base_url doesn't end with a forward slash.
        """
        if not base_url.endswith("/"):
            raise ValueError("base_url should end with a /")

        self.base_url = base_url
        self.timeout = timeout

        # Create session with retry strategy
        self.session = requests.Session()
        self.session.auth = auth

        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PATCH", "DELETE"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _clean_params(self, parameters: dict[str, Any] | None) -> dict[str, Any]:
        """Remove trailing underscores from parameter names.

        This allows using Python reserved words like 'from' as parameters
        by naming them 'from_' in the code.

        Args:
            parameters: A dict with parameters to clean.

        Returns:
            A dict with cleaned parameter names.
        """
        if not parameters:
            return {}

        result = {}
        for key, value in parameters.items():
            if key.endswith("_"):
                key = key[:-1]
            result[key] = value
        return result

    def _handle_response(self, response: requests.Response) -> None:
        """Handle response status codes and raise appropriate exceptions.

        Args:
            response: The response object to check.

        Raises:
            AuthenticationError: For 401 responses.
            ForbiddenError: For 403 responses.
            NotFoundError: For 404 responses.
            RateLimitError: For 429 responses.
            ServerError: For 5xx responses.
            APIError: For other error responses.
        """
        if response.ok:
            return

        status_code = response.status_code
        try:
            error_body = response.json()
            message = error_body.get("error", response.reason)
        except (ValueError, KeyError):
            error_body = None
            message = response.reason or f"HTTP {status_code}"

        if status_code == 401:
            raise AuthenticationError(message)
        elif status_code == 403:
            raise ForbiddenError(message)
        elif status_code == 404:
            raise NotFoundError(message)
        elif status_code == 429:
            retry_after = response.headers.get("Retry-After")
            try:
                retry_after_seconds = int(retry_after) if retry_after else None
            except (ValueError, TypeError):
                retry_after_seconds = None
            raise RateLimitError(
                message,
                retry_after=retry_after_seconds,
            )
        elif status_code >= 500:
            raise ServerError(message, status_code)
        else:
            raise APIError(message, status_code, error_body)

    def get(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Perform a GET request.

        Args:
            url: URL path to access (relative to base_url).
            body: Request body (unused for GET, kept for interface consistency).
            headers: Additional headers to send.
            parameters: URL query parameters.

        Returns:
            Response JSON as a dictionary.

        Raises:
            APIError: If the request fails.
        """
        parameters = self._clean_params(parameters)
        response = self.session.get(
            url=urljoin(self.base_url, url),
            params=parameters,
            headers=headers,
            timeout=self.timeout,
        )
        self._handle_response(response)
        return response.json()

    def post(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Perform a POST request.

        Args:
            url: URL path to access (relative to base_url).
            body: Request body as a dictionary (will be sent as JSON).
            headers: Additional headers to send.
            parameters: URL query parameters.

        Returns:
            Response object.

        Raises:
            APIError: If the request fails.
        """
        parameters = self._clean_params(parameters)
        response = self.session.post(
            url=urljoin(self.base_url, url),
            json=body,
            params=parameters,
            headers=headers,
            timeout=self.timeout,
        )
        self._handle_response(response)
        return response

    def patch(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Perform a PATCH request.

        Args:
            url: URL path to access (relative to base_url).
            body: Request body as a dictionary (will be sent as JSON).
            headers: Additional headers to send.
            parameters: URL query parameters.

        Returns:
            Response object.

        Raises:
            APIError: If the request fails.
        """
        parameters = self._clean_params(parameters)
        response = self.session.patch(
            url=urljoin(self.base_url, url),
            json=body,
            params=parameters,
            headers=headers,
            timeout=self.timeout,
        )
        self._handle_response(response)
        return response

    def delete(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Perform a DELETE request.

        Args:
            url: URL path to access (relative to base_url).
            body: Request body (unused for DELETE).
            headers: Additional headers to send.
            parameters: URL query parameters.

        Returns:
            Response object.

        Raises:
            APIError: If the request fails.
        """
        parameters = self._clean_params(parameters)
        response = self.session.delete(
            url=urljoin(self.base_url, url),
            headers=headers,
            params=parameters,
            timeout=self.timeout,
        )
        self._handle_response(response)
        return response


class PaginatedAPI(RESTAPI):
    """REST API client that handles paginated responses.

    This class extends RESTAPI to automatically follow pagination links
    and yield all results across multiple pages. Supports concurrent
    fetching of pages for improved performance.

    Attributes:
        max_workers: Maximum number of threads for concurrent page fetching.
    """

    def __init__(
        self,
        base_url: str,
        auth: BearerAuth,
        retries: int = 3,
        backoff_factor: float = 0.5,
        timeout: float = 30.0,
        max_workers: int = 5,
    ) -> None:
        """Initialize PaginatedAPI with threading configuration.

        Args:
            base_url: The URL to be called, must end with a forward slash.
            auth: Authentication class to be used with requests.
            retries: Number of retries for failed requests.
            backoff_factor: Backoff factor for retry delays.
            timeout: Default timeout for requests in seconds.
            max_workers: Maximum number of threads for concurrent page fetching.
        """
        super().__init__(base_url, auth, retries, backoff_factor, timeout)
        self.max_workers = max_workers

    def get(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """Perform a GET request with automatic pagination and concurrent fetching.

        This method fetches the first page to determine total pages, then
        fetches remaining pages concurrently using a thread pool. Results
        are yielded in page order.

        Args:
            url: URL path to access (relative to base_url).
            body: Request body (unused for GET).
            headers: Additional headers to send.
            parameters: URL query parameters.

        Yields:
            Individual items from the response data array.
        """
        if parameters is None:
            parameters = {}

        # Fetch first page to get pagination info
        data = super().get(url, body, headers, parameters)

        # For single objects, yield and return
        if isinstance(data.get("data"), dict):
            yield data["data"]
            return

        # Yield results from first page
        for item in data.get("data", []):
            yield item

        # Check if there are more pages
        pagination = data.get("pagination", {})
        if not pagination.get("next"):
            return

        # Determine total pages from first response
        # BetterStack API includes pagination info with page counts
        total_pages = self._get_total_pages(pagination)

        if total_pages is None:
            # Fall back to sequential fetching if we can't determine total pages
            yield from self._fetch_pages_sequential(url, headers, parameters, data)
            return

        if total_pages <= 1:
            return

        # Fetch remaining pages concurrently
        pages_data: dict[int, list[dict[str, Any]]] = {}

        # Capture parent's get method before entering executor context
        parent_get = super().get

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(parent_get, url, None, headers, {**parameters, "page": page}): page
                for page in range(2, total_pages + 1)
            }

            for future in as_completed(futures):
                page_num = futures[future]
                page_data = future.result()
                pages_data[page_num] = page_data.get("data", [])

        # Yield results in page order
        for page_num in sorted(pages_data.keys()):
            for item in pages_data[page_num]:
                yield item

    def _get_total_pages(self, pagination: dict[str, Any]) -> int | None:
        """Extract total page count from pagination info.

        Args:
            pagination: Pagination dictionary from API response.

        Returns:
            Total number of pages, or None if not determinable.
        """
        # Try to get last page URL and extract page number
        last_url = pagination.get("last")
        if last_url:
            parsed = urlparse(last_url)
            params = parse_qs(parsed.query)
            if "page" in params:
                try:
                    return int(params["page"][0])
                except (ValueError, IndexError):
                    pass
        return None

    def _fetch_pages_sequential(
        self,
        url: str,
        headers: dict[str, Any] | None,
        parameters: dict[str, Any],
        current_data: dict[str, Any],
    ) -> Generator[dict[str, Any], None, None]:
        """Fetch pages sequentially when total pages is unknown.

        Args:
            url: URL path to access.
            headers: Additional headers to send.
            parameters: Base URL query parameters.
            current_data: Current page data with pagination info.

        Yields:
            Individual items from response data arrays.
        """
        data = current_data
        while data.get("pagination", {}).get("next"):
            next_url = data["pagination"]["next"]
            parsed = urlparse(next_url)
            page_params = parse_qs(parsed.query)
            params = {**parameters}
            params.update({k: v[0] if len(v) == 1 else v for k, v in page_params.items()})

            data = super().get(url, None, headers, params)
            yield from data.get("data", [])


class UptimeAPI(PaginatedAPI):
    """BetterStack Uptime API client.

    This is the main client class for interacting with the BetterStack
    Uptime API. It is pre-configured with the correct base URL and supports
    concurrent fetching of paginated results.

    Example:
        >>> api = UptimeAPI("your-bearer-token")
        >>> monitors = list(Monitor.get_all_instances(api))

    Attributes:
        BETTERSTACK_API_URL: The base URL for the BetterStack Uptime API.
    """

    BETTERSTACK_API_URL = "https://uptime.betterstack.com/api/v2/"

    def __init__(
        self,
        bearer_token: str,
        retries: int = 3,
        backoff_factor: float = 0.5,
        timeout: float = 30.0,
        max_workers: int = 5,
    ) -> None:
        """Initialize UptimeAPI with bearer token authentication.

        Args:
            bearer_token: Bearer token for API authentication.
            retries: Number of retries for failed requests.
            backoff_factor: Backoff factor for retry delays.
            timeout: Default timeout for requests in seconds.
            max_workers: Maximum number of threads for concurrent page fetching.
        """
        super().__init__(
            base_url=self.BETTERSTACK_API_URL,
            auth=BearerAuth(bearer_token),
            retries=retries,
            backoff_factor=backoff_factor,
            timeout=timeout,
            max_workers=max_workers,
        )
