from typing import Optional


class RagtasticError(Exception):
    """Base exception for all Ragtastic client errors"""

    pass


class APIError(RagtasticError):
    """Raised when the API returns an error response"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class ValidationError(RagtasticError):
    """Raised when request validation fails"""

    pass


class AuthenticationError(RagtasticError):
    """Raised when authentication fails"""

    pass


class RateLimitError(RagtasticError):
    """Raised when rate limit is exceeded"""

    pass


class ArgumentException(RagtasticError):
    pass
