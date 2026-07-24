class BlockmanError(Exception):
    """Base exception for all 3axbat errors."""
    pass

class AuthenticationError(BlockmanError):
    """Raised when login fails or token is invalid/expired."""
    pass

class RateLimitError(BlockmanError):
    """Raised when the API rate limit is exceeded."""
    pass

class NotFoundError(BlockmanError):
    """Raised when a requested resource (user, clan, etc.) is not found."""
    pass

class SignatureError(BlockmanError):
    """Raised when the x-sign signature is rejected by the server."""
    pass