# sendrella/exceptions.py

class SendrellaError(Exception):
    """Base exception for all Sendrella SDK errors."""
    pass


class AuthenticationError(SendrellaError):
    """Raised when the API key is invalid or unauthorized."""
    pass


class RateLimitError(SendrellaError):
    """Raised when the API rate limit is exceeded."""
    pass


class BadRequestError(SendrellaError):
    """Raised when the request is malformed or fails validation."""
    pass


class NotFoundError(SendrellaError):
    """Raised when a resource is not found."""
    pass


class ServerError(SendrellaError):
    """Raised when the server encounters an error (5xx)."""
    pass


class TimeoutError(SendrellaError):
    """Raised when the request exceeds the allowed timeout."""
    pass


class APIConnectionError(SendrellaError):
    """Raised when the SDK cannot connect to the API endpoint."""
    pass
