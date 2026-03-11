"""Custom exceptions for the BetterStack Uptime API."""

from __future__ import annotations


class BetterStackError(Exception):
    """Base exception for all BetterStack errors."""

    pass


class APIError(BetterStackError):
    """Error returned from the BetterStack API."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_body: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        return f"[{self.status_code}] {super().__str__()}"


class AuthenticationError(APIError):
    """401 Unauthorized - Invalid or missing token."""

    def __init__(self, message: str = "Invalid or missing authentication token") -> None:
        super().__init__(message, 401)


class ForbiddenError(APIError):
    """403 Forbidden - Access denied."""

    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message, 403)


class NotFoundError(APIError):
    """404 Not Found - Resource doesn't exist."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, 404)


class RateLimitError(APIError):
    """429 Too Many Requests - Rate limit exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
    ) -> None:
        super().__init__(message, 429)
        self.retry_after = retry_after

    def __str__(self) -> str:
        base = super().__str__()
        if self.retry_after is not None:
            return f"{base} (retry after {self.retry_after}s)"
        return base


class ServerError(APIError):
    """5xx Server Error - Server-side issue."""

    def __init__(self, message: str = "Server error", status_code: int = 500) -> None:
        super().__init__(message, status_code)


class ValidationError(BetterStackError):
    """Local validation error (e.g., invalid parameters)."""

    pass


class ConfigurationError(BetterStackError):
    """Configuration error (e.g., missing required settings)."""

    pass
